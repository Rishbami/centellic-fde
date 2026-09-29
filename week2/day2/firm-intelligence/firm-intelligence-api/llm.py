# how we call the model... nothing in here knows abt FastAPI

import os
import logging
import time

import anthropic

from anthropic import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)

from pydantic import BaseModel, Field

MODEL = "claude-haiku-4-5-20251001"
INPUT_COST_PER_MILLION = 1.00
OUTPUT_COST_PER_MILLION = 5.00

logger = logging.getLogger(__name__)

# the SDK default are max_retries=2 and a 600-second read timeout
# Both are overriden here deliberately... they are decisions rather than on accident

client = anthropic.Client(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=30.0,
    max_retries=3,
)

# The prompt and where the rules live
# RULES GO IN SYSTEM
# DATA GOES IN USER

SYSTEM_PROMPT = (
    "You are a legal market analyst writing for an institutional audience. "
    "Use British English. Use only the figures given to you. "
    "Never invent numbers, rankings or facts that are not in the data provided."
)


def build_prompt(firm: dict) -> str:
    return (
        f"Summarise this law firm in two short paragraphs.\n\n"
        f"Name: {firm['name']}\n"
        f"Jurisdiction: {firm['jurisdiction']}\n"
        f"Revenue: {firm['revenue_usd_m']}\n"
        f"Lawyers: {firm['lawyers']}\n"
        f"Equity Partners: {firm['equity_partners']}\n"
    )


# def call_with_retry(firm: dict, max_attempts: int = 3):
#     """Call Anthropic with exponential backoff and log the successful call's cost."""
#     retryable_errors = (
#         APIConnectionError,
#         APITimeoutError,
#         InternalServerError,
#         RateLimitError,
#     )

#     for attempt in range(max_attempts):
#         try:
#             response = client.with_options(max_retries=0).messages.create(
#                 model=MODEL,
#                 max_tokens=400,
#                 system=SYSTEM_PROMPT,
#                 messages=[{"role": "user", "content": build_prompt(firm)}],
#             )
#             cost_usd = (
#                 response.usage.input_tokens * INPUT_COST_PER_MILLION
#                 + response.usage.output_tokens * OUTPUT_COST_PER_MILLION
#             ) / 1_000_000
#             logger.info("Anthropic call cost: $%.6f", cost_usd)
#             return response
#         except retryable_errors:
#             if attempt == max_attempts - 1:
#                 raise

#             delay_seconds = 2**attempt
#             logger.warning(
#                 "Anthropic call failed; retrying in %s seconds",
#                 delay_seconds,
#             )
#             time.sleep(delay_seconds)


# The call
def summarise_firm(firm: dict) -> dict:
    # one LLM call... returns the text plus what it costs to get it.
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
    )
    return {
        "id": firm["id"],
        "name": firm["name"],
        "summary": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }


# messages.count_tokens tell you how big a request is WITHOUT SENDING IT.... it's a seperate, much cheaper endpoint
def estimate_input_tokens(firm: dict) -> int:
    """Count tokens BEFORE sending. Costs nothing but tells you what a call will cost"""
    counted = client.messages.count_tokens(
        model=MODEL,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
    )
    return counted.input_tokens


def stream_firm_summary(firm: dict):
    """Yields text chunks as they arrive... rather than waiting for the whole response."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
    ) as stream:
        for text in stream.text_stream:
            yield text


class FirmAnalysis(BaseModel):
    """This is the shape we require back... it is not a suggestion to the model... it is a contract!"""

    tier: str = Field(description="One of: magic circle, national, boutique")
    # strengths
    strengths: list[str] = Field(max_length=3)
    # risks
    risks: list[str] = Field(max_length=3)
    # headcount_efficiency
    headcount_efficiency: str = Field(description="high, medium, or low")


def analyse_firm(firm: dict) -> dict:
    """Structured output. The response is validated against firm FirmAnalysist... or it fails."""
    response = client.messages.parse(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(firm)}],
        output_format=FirmAnalysis,
    )
    analysis = response.content[0].parsed_output

    return {
        # id
        "id": firm["id"],
        # name
        "name": firm["name"],
        # analysis
        "analysis": analysis,
        # input tokens
        "input_tokens": response.usage.input_tokens,
        # output tokens
        "output_tokens": response.usage.output_tokens,
        # stop reason
        "stop_reason": response.stop_reason,
    }


# Add the generative step
# Rtrieval finds documents... RAG's third letter is generate - turn the

GROUNDED_SYSTEM_PROMPT = (
    "Your are a legal marke analyst. Answer using ONLY the context provided. "
    "Cite the document id in square brackets after each claim, like [doc-001]. "
    "If the context does not contain the answer, say exactly: "
    "'The provided documents do not answer that question.' "
    "Never use knowledge from outside the context. Use British English. No em dash characters."
)


# Notice where the context goes...
# rules in system
# data n user
def answer_from_context(question: str, context: str) -> dict:
    """Answer strictly from retrieval context... The G in RAG"""
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=GROUNDED_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Context: \n\n{context}\n\nQuestion: {question}",
            }
        ],
    )
    return {
        "answer": response.content[0].text,
        # input tokens
        "input_tokens": response.usage.input_tokens,
        # output tokens
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }
