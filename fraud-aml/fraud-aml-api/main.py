from fastapi import FastAPI

from routers import accounts, alerts, analysts, insights, knowledge


app = FastAPI(title="Fraud AML API")

app.include_router(alerts.router)
app.include_router(accounts.router)
app.include_router(analysts.router)
app.include_router(knowledge.router)
app.include_router(insights.router)


@app.get("/health")
def health():
    return {"status": "ok"}
