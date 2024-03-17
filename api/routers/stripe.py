# module imports
from api.dependencies import payment_logic_dependency, authorize_user
from logic.authorization import CRUDOperation, ResourceType
from logic.payment import PaymentLogic
from models.payment import PaymentBase
# third party imports
from fastapi import APIRouter, File, Path, Query, Body, Depends, Security
import stripe
router = APIRouter()

@router.post("", response_model=str)
async def create(auth_info: str = Security(authorize_user, scopes=[f"{CRUDOperation.CREATE.value}:{ResourceType.payment.value}"]),
    payment_logic: PaymentLogic = Depends(payment_logic_dependency), products: PaymentBase = Body(..., title="payment")):
    
    user_email = auth_info
    session = payment_logic.create(products=products, user_email=user_email)
    return session.url
