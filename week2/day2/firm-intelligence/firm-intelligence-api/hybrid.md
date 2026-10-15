# Task: Hybrid Retrieval in the Real World

**Team C: Qdrant**

The assignment investigates how real search systems combine keyword and vector retrieval, compares their choices with our application’s current approach, and asks for one evidence-based recommendation.

This document covers the three core questions, the six Qdrant investigation points and an application comparison.

## Part 1: The Research Questions

### 1. Rank or Score?

There are two families of fusion. Rank-based fusion, such as Reciprocal Rank Fusion, uses only each list’s order. Score-based fusion rescales each list’s scores and adds them. What does each gain, and what does each throw away?

#### Understanding Fusion

Hybrid retrieval combines two ways of finding relevant documents:

- **Semantic or vector retrieval:** Finds documents with similar meanings, even when different words are used.
- **Keyword retrieval:** Finds documents containing relevant words, terms or identifiers.

Each method produces a ranked list of documents. Fusion means combining those lists into one final ranking.

#### Rank-Based Fusion: Reciprocal Rank Fusion (RRF)

RRF uses a document’s position in each list rather than its original similarity score.

For example:

| Document | Semantic Rank | Keyword Rank |
|---|---:|---:|
| A | 1 | 8 |
| B | 2 | 2 |
| C | 6 | 1 |

Document B ranks highly in both lists, so RRF can reward that agreement.

The original RRF formula is commonly written as:

$$
RRF(d) = \sum_r \frac{1}{k + \operatorname{rank}_r(d)}
$$

The original 2009 research by Gordon Cormack, Charles Clarke and Stefan Buettcher established RRF as a method for merging rankings from multiple information retrieval systems. The paper used a rank constant of 60.

**What RRF gains:** It is simple, works across search methods with different score scales, and rewards documents appearing highly in multiple lists.

**What RRF sacrifices:** It discards the original score differences. A document scoring 0.99 instead of 0.60 receives the same rank contribution if both are ranked first in their respective searches.

Source: Original RRF research

#### Score-Based Fusion

Score-based fusion uses retrieval scores after converting them into comparable values.

For example:

| Document | Normalised Semantic Score | Normalised Keyword Score | Total |
|---|---:|---:|---:|
| A | 0.90 | 0.20 | 1.10 |
| B | 0.70 | 0.80 | 1.50 |
| C | 0.30 | 0.90 | 1.20 |

Here, B wins because its combined score is highest.

**What score-based fusion gains:** It retains information about how strongly a document matches each retriever’s query, rather than just its position.

**What score-based fusion sacrifices:** It depends on normalisation and the reliability of the original scores. An unusual or extreme score may disproportionately affect the final ranking.

Weaviate illustrates this difference through its `rankedFusion` and `relativeScoreFusion` algorithms. Its score-based approach became the default in version 1.24, partly because it preserves more information about the original score differences.

Source: Weaviate — Hybrid Search Fusion Algorithms

#### Comparison

| Feature | Rank-Based RRF | Score-Based Fusion |
|---|---|---|
| Uses | Positions | Normalised scores |
| Main benefit | Combines incompatible score scales | Preserves strength of matches |
| Main weakness | Loses score differences | Sensitive to score distributions |
| Best considered when | Score scales are difficult to compare | Scores carry useful, reliable information |

**Answer:** Neither is automatically better. RRF is straightforward and robust to incompatible scores, whereas score-based fusion preserves information about match strength. The choice should be evaluated using actual queries and known-relevant documents.

### 2. Does Hybrid Actually Help?

Find one published comparison with numbers: hybrid against keyword-only or vector-only. Note the dataset, the metric, the size of the gain, and who ran it.

#### Published Comparison: Microsoft Azure AI Search

Microsoft published Azure AI Search: Outperforming Vector Search with Hybrid Retrieval and Reranking in September 2023.

The study compared four configurations:

- Keyword-only BM25.
- Vector-only retrieval using Ada-002 embeddings.
- Hybrid keyword and vector retrieval.
- Hybrid retrieval followed by semantic reranking.

Microsoft conducted the tests using Azure AI Search.

#### Reported Results

Scores below use the publication’s 0–100 NDCG scale.

| Retrieval Method | Customer Datasets NDCG@3 | BEIR NDCG@10 | MIRACL NDCG@10 |
|---|---:|---:|---:|
| Keyword-only | 40.6 | 40.6 | 49.6 |
| Vector-only | 43.8 | 45.0 | 58.3 |
| Hybrid | 48.4 | 48.4 | 58.8 |
| Hybrid + semantic ranker | 60.1 | 50.0 | 72.0 |

#### What Does NDCG Mean?

Normalised Discounted Cumulative Gain evaluates whether a system retrieves relevant documents and ranks the most relevant ones near the top.

- NDCG@3 evaluates the first three results.
- NDCG@10 evaluates the first ten results.
- Higher scores represent better retrieval rankings.

NDCG@3 is particularly relevant to our application because it sends the top three chunks to its language model.

#### Size of the Improvement

| Dataset | Vector-Only | Hybrid | Absolute Improvement | Relative Improvement |
|---|---:|---:|---|---|
| Customer datasets, NDCG@3 | 43.8 | 48.4 | +4.6 points | Approximately 10.5% |
| BEIR, NDCG@10 | 45.0 | 48.4 | +3.4 points | Approximately 7.6% |

These improvements are calculated from Microsoft’s published scores, not separate measurements.

**Who conducted the research?** Microsoft’s Azure AI Search team. This is vendor-conducted evidence, not an independent comparison. The results demonstrate improvements on the tested datasets but do not guarantee improvement on our application.

Source: Microsoft — Original Comparison

### 3. Where Does the Keyword Half Come From?

In production, is it classic BM25 from an inverted index, or a learned sparse model? Find one example of each.

**Answer:** Both approaches are used. The keyword-oriented retriever may use traditional BM25 weighting or learned sparse representations.

#### Example 1: Classic BM25 in Elasticsearch

BM25 ranks documents according to how strongly their words match a query.

Its scoring considers:

- **Term frequency:** How frequently a word appears in a document.
- **Inverse document frequency:** How rare a word is across the documents.
- **Document length:** Adjusts scoring to avoid unfairly favouring longer documents.

An inverted index connects searchable terms to the documents containing them.

A simplified illustration:

| Search Term | Documents Containing It |
|---|---|
| LP-3307 | Document 2, Document 7 |
| Contract | Document 1, Document 2 |
| Revenue | Document 3, Document 5 |

Actual matching depends on how the index tokenises terms and identifiers.

Elasticsearch provides a production example of classic BM25 retrieval. Elastic documents these tuning parameters:

| Parameter | What It Controls | Typical Elastic Default |
|---|---|---:|
| `k1` | How quickly additional occurrences of a word stop contributing much extra score | 1.2 |
| `b` | How strongly document length affects scoring | 0.75 |

Elastic recommends starting with its defaults before adjusting those settings.

Source: Elastic — Practical BM25, Part 3

#### Example 2: Learned Sparse Retrieval with Qdrant and SPLADE

A sparse vector has many possible dimensions, but only a small number contain non-zero values for a particular document.

A learned sparse model uses machine learning to determine which terms receive weight. SPLADE, for example, can assign importance to relevant terms and expand the representation to include related terms.

Qdrant supports learned sparse representations alongside BM25.

Source: Qdrant — Hybrid Search

#### Difference Between the Approaches

| BM25 | Learned Sparse Retrieval |
|---|---|
| Uses established mathematical word-weighting rules | Learns word importance from training data |
| Strong on exact word matches | Can incorporate contextual word relationships |
| Does not require neural inference to generate term weights | Requires a trained model to generate representations |
| Example: Elasticsearch BM25 | Example: Qdrant with SPLADE |

**Conclusion:** BM25 is a sensible baseline for exact identifiers, while learned sparse retrieval may offer more sophisticated term matching. Whether the additional complexity improves results requires testing.

## Part 2: Our System — Qdrant

Qdrant is a vector search engine that supports combining dense semantic vectors with sparse keyword-oriented representations.

Its hybrid query API supports both RRF and Distribution-Based Score Fusion (DBSF).

Source: Qdrant — Hybrid Queries

### Question - It offers two fusion methods. What does the second one do with each list’s scores?

The second method is DBSF.

DBSF examines each retriever’s score distribution independently. It:

- Calculates the average score.
- Calculates the standard deviation, which measures how spread out the scores are.
- Normalises scores using endpoints three standard deviations below and above the average.
- Adds the normalised scores across retrievers.

Unlike RRF, DBSF preserves information about relative score gaps within each list.

| RRF | DBSF |
|---|---|
| Uses rank positions | Uses score values |
| Ignores original score gaps | Retains relative score gaps |
| Supports configurable `k` and weights | Has no equivalent `k` or weight parameters |
| Robust to different raw score scales | Depends on meaningful score distributions |

DBSF calculates its normalisation statistics from the returned candidates, not historical global scores. It has been available since Qdrant v1.11.0.

Source: Qdrant — Hybrid and Multi-Stage Queries

### 1. How Do You Request Hybrid Search?

Qdrant uses the Query API and its `prefetch` mechanism.

Prefetch collects candidate documents through individual searches before combining their results.

A simplified Python example:

```python
from qdrant_client import models

results = client.query_points(
    collection_name="documents",
    prefetch=[
        models.Prefetch(
            query=dense_query_vector,
            using="dense",
            limit=100,
        ),
        models.Prefetch(
            query=sparse_query_vector,
            using="sparse",
            limit=100,
        ),
    ],
    query=models.FusionQuery(
        fusion=models.Fusion.RRF,
    ),
    limit=3,
)
```

**From:** Rishi Ram <rram@spartaglobal.com>  
**Sent:** 14 October 2026 14:35  
**To:** Maryam Ali <mali@spartaglobal.com>  
**Subject:**

# Task: Hybrid Retrieval in the Real World

**Team C: Qdrant**

The assignment investigates how real search systems combine keyword and vector retrieval, compares their choices with our application’s current approach, and asks for one evidence-based recommendation.

This document covers the three core questions, the six Qdrant investigation points and an application comparison.

## Part 1: The Research Questions

### 1. Rank or Score?

There are two families of fusion. Rank-based fusion, such as Reciprocal Rank Fusion, uses only each list’s order. Score-based fusion rescales each list’s scores and adds them. What does each gain, and what does each throw away?

#### Understanding Fusion

Hybrid retrieval combines two ways of finding relevant documents:

- **Semantic or vector retrieval:** Finds documents with similar meanings, even when different words are used.
- **Keyword retrieval:** Finds documents containing relevant words, terms or identifiers.

Each method produces a ranked list of documents. Fusion means combining those lists into one final ranking.

#### Rank-Based Fusion: Reciprocal Rank Fusion (RRF)

RRF uses a document’s position in each list rather than its original similarity score.

For example:

| Document | Semantic Rank | Keyword Rank |
|---|---:|---:|
| A | 1 | 8 |
| B | 2 | 2 |
| C | 6 | 1 |

Document B ranks highly in both lists, so RRF can reward that agreement.

The original RRF formula is commonly written as:

$$
RRF(d) = \sum_r \frac{1}{k + \operatorname{rank}_r(d)}
$$

The original 2009 research by Gordon Cormack, Charles Clarke and Stefan Buettcher established RRF as a method for merging rankings from multiple information retrieval systems. The paper used a rank constant of 60.

**What RRF gains:** It is simple, works across search methods with different score scales, and rewards documents appearing highly in multiple lists.

**What RRF sacrifices:** It discards the original score differences. A document scoring 0.99 instead of 0.60 receives the same rank contribution if both are ranked first in their respective searches.

Source: Original RRF research

#### Score-Based Fusion

Score-based fusion uses retrieval scores after converting them into comparable values.

For example:

| Document | Normalised Semantic Score | Normalised Keyword Score | Total |
|---|---:|---:|---:|
| A | 0.90 | 0.20 | 1.10 |
| B | 0.70 | 0.80 | 1.50 |
| C | 0.30 | 0.90 | 1.20 |

Here, B wins because its combined score is highest.

**What score-based fusion gains:** It retains information about how strongly a document matches each retriever’s query, rather than just its position.

**What score-based fusion sacrifices:** It depends on normalisation and the reliability of the original scores. An unusual or extreme score may disproportionately affect the final ranking.

Weaviate illustrates this difference through its `rankedFusion` and `relativeScoreFusion` algorithms. Its score-based approach became the default in version 1.24, partly because it preserves more information about the original score differences.

Source: Weaviate — Hybrid Search Fusion Algorithms

#### Comparison

| Feature | Rank-Based RRF | Score-Based Fusion |
|---|---|---|
| Uses | Positions | Normalised scores |
| Main benefit | Combines incompatible score scales | Preserves strength of matches |
| Main weakness | Loses score differences | Sensitive to score distributions |
| Best considered when | Score scales are difficult to compare | Scores carry useful, reliable information |

**Answer:** Neither is automatically better. RRF is straightforward and robust to incompatible scores, whereas score-based fusion preserves information about match strength. The choice should be evaluated using actual queries and known-relevant documents.

### 2. Does Hybrid Actually Help?

Find one published comparison with numbers: hybrid against keyword-only or vector-only. Note the dataset, the metric, the size of the gain, and who ran it.

#### Published Comparison: Microsoft Azure AI Search

Microsoft published Azure AI Search: Outperforming Vector Search with Hybrid Retrieval and Reranking in September 2023.

The study compared four configurations:

- Keyword-only BM25.
- Vector-only retrieval using Ada-002 embeddings.
- Hybrid keyword and vector retrieval.
- Hybrid retrieval followed by semantic reranking.

Microsoft conducted the tests using Azure AI Search.

#### Reported Results

Scores below use the publication’s 0–100 NDCG scale.

| Retrieval Method | Customer Datasets NDCG@3 | BEIR NDCG@10 | MIRACL NDCG@10 |
|---|---:|---:|---:|
| Keyword-only | 40.6 | 40.6 | 49.6 |
| Vector-only | 43.8 | 45.0 | 58.3 |
| Hybrid | 48.4 | 48.4 | 58.8 |
| Hybrid + semantic ranker | 60.1 | 50.0 | 72.0 |

#### What Does NDCG Mean?

Normalised Discounted Cumulative Gain evaluates whether a system retrieves relevant documents and ranks the most relevant ones near the top.

- NDCG@3 evaluates the first three results.
- NDCG@10 evaluates the first ten results.
- Higher scores represent better retrieval rankings.

NDCG@3 is particularly relevant to our application because it sends the top three chunks to its language model.

#### Size of the Improvement

| Dataset | Vector-Only | Hybrid | Absolute Improvement | Relative Improvement |
|---|---:|---:|---|---|
| Customer datasets, NDCG@3 | 43.8 | 48.4 | +4.6 points | Approximately 10.5% |
| BEIR, NDCG@10 | 45.0 | 48.4 | +3.4 points | Approximately 7.6% |

These improvements are calculated from Microsoft’s published scores, not separate measurements.

**Who conducted the research?** Microsoft’s Azure AI Search team. This is vendor-conducted evidence, not an independent comparison. The results demonstrate improvements on the tested datasets but do not guarantee improvement on our application.

Source: Microsoft — Original Comparison

### 3. Where Does the Keyword Half Come From?

In production, is it classic BM25 from an inverted index, or a learned sparse model? Find one example of each.

**Answer:** Both approaches are used. The keyword-oriented retriever may use traditional BM25 weighting or learned sparse representations.

#### Example 1: Classic BM25 in Elasticsearch

BM25 ranks documents according to how strongly their words match a query.

Its scoring considers:

- **Term frequency:** How frequently a word appears in a document.
- **Inverse document frequency:** How rare a word is across the documents.
- **Document length:** Adjusts scoring to avoid unfairly favouring longer documents.

An inverted index connects searchable terms to the documents containing them.

A simplified illustration:

| Search Term | Documents Containing It |
|---|---|
| LP-3307 | Document 2, Document 7 |
| Contract | Document 1, Document 2 |
| Revenue | Document 3, Document 5 |

Actual matching depends on how the index tokenises terms and identifiers.

Elasticsearch provides a production example of classic BM25 retrieval. Elastic documents these tuning parameters:

| Parameter | What It Controls | Typical Elastic Default |
|---|---|---:|
| `k1` | How quickly additional occurrences of a word stop contributing much extra score | 1.2 |
| `b` | How strongly document length affects scoring | 0.75 |

Elastic recommends starting with its defaults before adjusting those settings.

Source: Elastic — Practical BM25, Part 3

#### Example 2: Learned Sparse Retrieval with Qdrant and SPLADE

A sparse vector has many possible dimensions, but only a small number contain non-zero values for a particular document.

A learned sparse model uses machine learning to determine which terms receive weight. SPLADE, for example, can assign importance to relevant terms and expand the representation to include related terms.

Qdrant supports learned sparse representations alongside BM25.

Source: Qdrant — Hybrid Search

#### Difference Between the Approaches

| BM25 | Learned Sparse Retrieval |
|---|---|
| Uses established mathematical word-weighting rules | Learns word importance from training data |
| Strong on exact word matches | Can incorporate contextual word relationships |
| Does not require neural inference to generate term weights | Requires a trained model to generate representations |
| Example: Elasticsearch BM25 | Example: Qdrant with SPLADE |

**Conclusion:** BM25 is a sensible baseline for exact identifiers, while learned sparse retrieval may offer more sophisticated term matching. Whether the additional complexity improves results requires testing.

## Part 2: Our System — Qdrant

Qdrant is a vector search engine that supports combining dense semantic vectors with sparse keyword-oriented representations.

Its hybrid query API supports both RRF and Distribution-Based Score Fusion (DBSF).

Source: Qdrant — Hybrid Queries

### Question - It offers two fusion methods. What does the second one do with each list’s scores?

The second method is DBSF.

DBSF examines each retriever’s score distribution independently. It:

- Calculates the average score.
- Calculates the standard deviation, which measures how spread out the scores are.
- Normalises scores using endpoints three standard deviations below and above the average.
- Adds the normalised scores across retrievers.

Unlike RRF, DBSF preserves information about relative score gaps within each list.

| RRF | DBSF |
|---|---|
| Uses rank positions | Uses score values |
| Ignores original score gaps | Retains relative score gaps |
| Supports configurable `k` and weights | Has no equivalent `k` or weight parameters |
| Robust to different raw score scales | Depends on meaningful score distributions |

DBSF calculates its normalisation statistics from the returned candidates, not historical global scores. It has been available since Qdrant v1.11.0.

Source: Qdrant — Hybrid and Multi-Stage Queries

### 1. How Do You Request Hybrid Search?

Qdrant uses the Query API and its `prefetch` mechanism.

Prefetch collects candidate documents through individual searches before combining their results.

A simplified Python example:

```python
from qdrant_client import models

results = client.query_points(
    collection_name="documents",
    prefetch=[
        models.Prefetch(
            query=dense_query_vector,
            using="dense",
            limit=100,
        ),
        models.Prefetch(
            query=sparse_query_vector,
            using="sparse",
            limit=100,
        ),
    ],
    query=models.FusionQuery(
        fusion=models.Fusion.RRF,
    ),
    limit=3,
)
```