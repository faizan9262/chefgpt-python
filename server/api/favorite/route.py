from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.schema import AddFavorite, RemoveFavorite
from .controller import add_to_favorite, get_favorites, remove_from_favorite
from utils.dependencies import get_current_user
from api.auth.models import User

router = APIRouter()

@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add(
    dish_data: AddFavorite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await add_to_favorite(dish_data, db, current_user)


@router.post('/remove', status_code=status.HTTP_200_OK)
async def remove(
    dish_data: RemoveFavorite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await remove_from_favorite(dish_data, db, current_user)


@router.get('/get-all', status_code=status.HTTP_200_OK)
async def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_favorites(db, current_user)
