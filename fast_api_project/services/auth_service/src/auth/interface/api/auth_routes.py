from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.use_cases.register import RegisterUser
from auth.config import get_db
from auth.domain.exceptions import UserAlreadyExistsError
from auth.infrastructure.adapters import BcryptHasher
from auth.infrastructure.database.repositories import SQLAlchemyUserRepository
from auth.interface.api.schemas.register_request import RegisterRequest
from auth.interface.api.schemas.user_response import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def get_register_use_case(db: AsyncSession = Depends(get_db)) -> RegisterUser:
    """Dependency to get the RegisterUser use case."""
    user_repo = SQLAlchemyUserRepository(db)
    hasher = BcryptHasher(cost=12)
    return RegisterUser(user_repo, hasher)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest, use_case: RegisterUser = Depends(get_register_use_case)
):
    """
    Register a new user.
    """
    try:
        user = await use_case.execute(
            username=request.username, email=request.email, password=request.password
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
