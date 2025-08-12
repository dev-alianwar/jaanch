from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, require_role
from translation_service import TranslationService
from translation_models import Translation
from pydantic import BaseModel
from typing import Optional, Dict, List

router = APIRouter(prefix="/translations", tags=["translations"])

class TranslationCreate(BaseModel):
    key: str
    locale: str
    value: str
    category: Optional[str] = None
    description: Optional[str] = None

class TranslationUpdate(BaseModel):
    value: str
    description: Optional[str] = None

@router.get("/locale/{locale}")
async def get_translations_by_locale(
    locale: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Get all translations for a specific locale"""
    service = TranslationService(db)
    translations = service.get_translations_by_locale(locale)
    return {"locale": locale, "translations": translations}

@router.get("/admin/all")
async def get_all_translations_admin(
    current_user = Depends(require_role(["superadmin"])),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get all translations for admin management"""
    service = TranslationService(db)
    translations = service.get_all_translations()
    return translations

@router.get("/admin/category/{category}")
async def get_translations_by_category(
    category: str,
    locale: Optional[str] = None,
    current_user = Depends(require_role(["superadmin"])),
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Get translations by category"""
    service = TranslationService(db)
    translations = service.get_translations_by_category(category, locale)
    return translations

@router.post("/admin")
async def create_translation(
    translation_data: TranslationCreate,
    current_user = Depends(require_role(["superadmin"])),
    db: Session = Depends(get_db)
):
    """Create a new translation"""
    service = TranslationService(db)
    
    # Check if translation already exists
    existing = db.query(Translation).filter(
        Translation.key == translation_data.key,
        Translation.locale == translation_data.locale,
        Translation.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation already exists for this key and locale"
        )
    
    translation = service.create_translation(
        key=translation_data.key,
        locale=translation_data.locale,
        value=translation_data.value,
        category=translation_data.category,
        description=translation_data.description
    )
    
    return translation.to_dict()

@router.put("/admin/{translation_id}")
async def update_translation(
    translation_id: str,
    translation_data: TranslationUpdate,
    current_user = Depends(require_role(["superadmin"])),
    db: Session = Depends(get_db)
):
    """Update an existing translation"""
    service = TranslationService(db)
    
    translation = service.update_translation(
        translation_id=translation_id,
        value=translation_data.value,
        description=translation_data.description
    )
    
    if not translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation not found"
        )
    
    return translation.to_dict()

@router.delete("/admin/{translation_id}")
async def delete_translation(
    translation_id: str,
    current_user = Depends(require_role(["superadmin"])),
    db: Session = Depends(get_db)
):
    """Delete a translation"""
    service = TranslationService(db)
    
    success = service.delete_translation(translation_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation not found"
        )
    
    return {"message": "Translation deleted successfully"}

@router.post("/admin/seed")
async def seed_translations(
    current_user = Depends(require_role(["superadmin"])),
    db: Session = Depends(get_db)
):
    """Seed default translations"""
    service = TranslationService(db)
    service.seed_default_translations()
    return {"message": "Default translations seeded successfully"}