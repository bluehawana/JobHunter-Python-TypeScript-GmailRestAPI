from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.services.user_service import UserService
from app.api.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user
    """
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    user_update: dict,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends()
):
    """
    Update current user
    """
    updated_user = await user_service.update_user(current_user.id, user_update)
    return updated_user