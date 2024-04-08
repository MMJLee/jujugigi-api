# third party imports
from fastapi import APIRouter, Depends, Security
from fastapi.responses import RedirectResponse

# module imports
from app.api.dependencies import stripe_logic_dependency, authorize_user
from app.logic.stripe import StripeLogic

router = APIRouter()


@router.post("", response_model=RedirectResponse)
async def create(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    stripe_logic: StripeLogic = Depends(stripe_logic_dependency),
):

    user_email = auth_info
    session = await stripe_logic.create(user_email=user_email)
    return RedirectResponse(url=session.url)
