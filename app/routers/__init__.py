from fastapi import APIRouter
from .UserRouter import user_router
from .ContactRouter import contact_router
from .AuthRouter import auth_router

router = APIRouter(prefix="/api/v1")
router.include_router(user_router)
router.include_router(contact_router)
router.include_router(auth_router)
