from fastapi import APIRouter

from app.controller.v1.products_controller import router as product_router
from app.core.security import router as security_router

router = APIRouter()

router.include_router(product_router)
router.include_router(security_router)