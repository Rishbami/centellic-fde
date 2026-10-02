from fastapi import APIRouter, Depends, HTTPException

from data import ACCOUNTS
from models import Account


router = APIRouter(prefix="/accounts", tags=["accounts"])
