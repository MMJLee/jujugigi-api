# third party imports
from fastapi import APIRouter, Depends, Security

# module imports
from app.api.dependencies import stripe_logic_dependency, authorize_user
from app.logic.stripe import StripeLogic
from app.models.stripe import StripeResponse

router = APIRouter()


@router.post("", response_model=StripeResponse)
async def create(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    stripe_logic: StripeLogic = Depends(stripe_logic_dependency),
):

    user_email = auth_info
    stripe_url = await stripe_logic.create(user_email=user_email)
    return StripeResponse(url=stripe_url)
