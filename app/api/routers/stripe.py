# third party imports
from fastapi import APIRouter, Depends, Path, Request, Security, Header

# module imports
from app.api.dependencies import stripe_logic_dependency, authorize_user
from app.logic.authorization import CRUDOperation, ResourceType
from app.logic.stripe import StripeLogic
from app.models.response import DeleteResponse, UpdateResponse
from app.models.stripe import StripeResponse


router = APIRouter()


async def parse_body(request: Request):
    data: bytes = await request.body()
    return data


@router.get("", response_model=StripeResponse)
async def read(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    stripe_logic: StripeLogic = Depends(stripe_logic_dependency),
):

    user_email = auth_info
    stripe_url = await stripe_logic.read(user_email=user_email)
    return StripeResponse(url=stripe_url)


@router.post("/webhook", response_model=UpdateResponse)
async def webhook(
    stripe_logic: StripeLogic = Depends(stripe_logic_dependency),
    stripe_response_header: str = Header(..., alias="stripe-signature"),
    stripe_response_body: bytes = Depends(parse_body),
):
    updated = await stripe_logic.webhook(stripe_response_header=stripe_response_header, stripe_response_body=stripe_response_body)
    return UpdateResponse(updated=updated)


@router.delete("/{stripe_id}", response_model=DeleteResponse)
async def delete(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.DELETE.value}:{ResourceType.STRIPE.value}"],
    ),
    stripe_logic: StripeLogic = Depends(stripe_logic_dependency),
    stripe_id: int = Path(..., title="stripe id"),
):

    _ = auth_info
    deleted = await stripe_logic.delete(stripe_id=stripe_id)
    return DeleteResponse(deleted=deleted)
