from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from utils.dependencies import get_current_user
from database import get_db
from schemas.schema import AddFavorite, RemoveFavorite
from .models import Favorite
from utils.uploader import upload_from_url_or_base64


async def add_to_favorite(
    dish_data: AddFavorite,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    image_url = dish_data.image

    final_url = None
    if image_url:
        # Case 1: Already Cloudinary hosted → use directly
        if "res.cloudinary.com" in image_url:
            final_url = image_url
        # Case 2: StableHorde (or any http url) → re-upload to Cloudinary
        elif image_url.startswith("http"):
            final_url = upload_from_url_or_base64(image_url)
        # Case 3: base64 string → re-upload to Cloudinary
        elif image_url.startswith("data:image"):
            final_url = upload_from_url_or_base64(image_url)

    favorite = Favorite(
        name=dish_data.name,
        description=dish_data.description,
        recipe=dish_data.recipe,
        image=final_url,
        user_id=current_user.id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


async def get_favorites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id)\
        .order_by(Favorite.created_at.desc()).all()
    return favorites


async def remove_from_favorite(
    dish_data: RemoveFavorite,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(
        Favorite.id == dish_data.id,
        Favorite.user_id == current_user.id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Removed From Favorites."}
