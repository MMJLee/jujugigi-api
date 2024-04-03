# third party imports
from fastapi import APIRouter, Body, Depends, Security

# module imports
from app.api.dependencies import payment_logic_dependency, authorize_user
from app.logic.authorization import CRUDOperation, ResourceType
from app.logic.payment import PaymentLogic
from app.models.payment import PaymentBase


router = APIRouter()


@router.post("", response_model=str)
async def create(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.CREATE.value}:{ResourceType.TRANSACTION.value}"],
    ),
    payment_logic: PaymentLogic = Depends(payment_logic_dependency),
    products: PaymentBase = Body(..., title="payment"),
):

    user_email = auth_info
    session = payment_logic.create(products=products, user_email=user_email)
    return session.url
