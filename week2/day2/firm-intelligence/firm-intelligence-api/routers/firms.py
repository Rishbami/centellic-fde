from fastapi import HTTPException, Depends, APIRouter, Header
from data import FIRMS

from pydantic import BaseModel, Field

router = APIRouter(prefix="/firms", tags=["firms"])

_seen_keys: dict[str, dict] = {}


# Everything so far has been read only... now sombody sends you data and you have no idea what it is
# First we need to decribe what we are going to accept (Shape)
class NewFirm(BaseModel):
    # Name, Juristication, revenue, lawyers, equity_partners
    name: str = Field(min_length=1)
    jurisdiction: str = Field(min_length=2, max_length=5)
    revenue_usd_m: float = Field(gt=0)
    lawyers: int = Field(gt=0)
    equity_partners: int = Field(gt=0)


def get_firm_or_404(firm_id: int) -> dict:
    for firm in FIRMS:
        if firm["id"] == firm_id:
            return firm
    raise HTTPException(status_code=404, detail="Firm not found")


@router.get("")
def list_firms(jurisdiction: str | None = None, min_revenue: float | None = None):
    results = FIRMS
    if jurisdiction is not None:
        results = [f for f in results if f["jurisdiction"] == jurisdiction]
    if min_revenue is not None:
        results = [f for f in results if f["revenue_usd_m"] >= min_revenue]
    return results


# get one firm
@router.get("/{firm_id}")
def get_firm(firm: dict = Depends(get_firm_or_404)):
    return firm


# Compute revenue per lawyer is total revenue divided by fee-earner headcount
# Property per equity partner assumes a 35% margin, then divide by the number of equity partners
# Both are pretty standard law firms benchmarks... the kind of things Centellic platforms provides
@router.get("/{firm_id}/benchmarks")
def get_benchmark(firm: dict = Depends(get_firm_or_404)):
    revenue = firm["revenue_usd_m"]
    return {
        # id
        "id": firm["id"],
        # name
        "name": firm["name"],
        # rev per partner
        "revenue_per_lawyer_usd": round(
            revenue * 1_000_000 / firm["lawyers"],
        ),
        # profit per ep
        "profit_per_equity_partner_usd": round(
            revenue * 1_000_000 * 0.35 / firm["equity_partners"],
        ),
    }


# A parameter annotated with pydantic model means body
# A plain int or str means a URL or query parameter


# post
# /firms


@router.post("", status_code=201)
def add_firm(new: NewFirm, idempotent_key: str | None = Header(default=None)):
    if idempotent_key is not None and idempotent_key in _seen_keys:
        return _seen_keys[idempotent_key]

    new_id = max(firm["id"] for firm in FIRMS) + 1
    firm = {
        "id": new_id,
        "name": new.name,
        "jurisdiction": new.jurisdiction,
        "revenue_usd_m": new.revenue_usd_m,
        "lawyers": new.lawyers,
        "equity_partners": new.equity_partners,
    }

    FIRMS.append(firm)
    if idempotent_key is not None:
        _seen_keys[idempotent_key] = firm
    return firm


@router.put("/{firm_id}")
def update_firm(updated: NewFirm, firm: dict = Depends(get_firm_or_404)):
    firm.update(updated.model_dump())
    return firm


@router.delete("/{firm_id}")
def delete_firm(firm: dict = Depends(get_firm_or_404)):
    FIRMS.remove(firm)
    return firm
