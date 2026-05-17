from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.access_control import require_roles
from app.schemas.fundraising_category import (
    FundraisingCategoryCreate,
    FundraisingCategoryUpdate,
    FundraisingCategoryResponse,
    FundraisingCategorySearchResponse,
)
from app.controllers.fundraising_category import (
    createCategoryController,
    viewFundraisingCategoryController,
    updateCategoryController,
    suspendCategoryController,
    searchFundraisingCategoryController,
)

router = APIRouter(prefix="/api/category", tags=["Fundraising Categories"])

require_platform_manager = require_roles("PLATFORM_MANAGER")
require_platform_fundraiser_or_donee = require_roles("PLATFORM_MANAGER", "FUNDRAISER", "DONEE")


@router.post("/", response_model=FundraisingCategoryResponse, status_code=201)
def createFundraisingCategory(
    payload: FundraisingCategoryCreate,
    _: None = Depends(require_platform_manager),
):
    controller = createCategoryController()
    result = controller.createFundraisingCategory(payload.name, payload.description)

    if result == "category_not_found":
        raise HTTPException(status_code=400, detail="Category not found or inactive")

    if result == "duplicate_name":
        raise HTTPException(status_code=400, detail="A category with that name already exists")

    return result


@router.get("/", response_model=FundraisingCategorySearchResponse)
def searchCategory(
    keyword: str | None = Query(default=None),
    _: None = Depends(require_platform_fundraiser_or_donee),
):
    controller = searchFundraisingCategoryController()
    categories = controller.searchCategory(keyword)

    return {"total": len(categories), "data": categories}


@router.get("/{category_id}", response_model=FundraisingCategoryResponse)
def getCategory(
    category_id: int,
    _: None = Depends(require_platform_manager),
):
    controller = viewFundraisingCategoryController()
    result = controller.getCategory(category_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Category not found")

    return result


@router.patch("/{category_id}", response_model=FundraisingCategoryResponse)
def updateCategory(
    category_id: int,
    payload: FundraisingCategoryUpdate,
    _: None = Depends(require_platform_manager),
):
    controller = updateCategoryController()
    result = controller.updateCategory(category_id, payload.name, payload.description)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Category not found")

    if result == "duplicate_name":
        raise HTTPException(status_code=400, detail="A category with that name already exists")

    return result


@router.patch("/{category_id}/suspend")
def suspendCategory(
    category_id: int,
    _: None = Depends(require_platform_manager),
):
    controller = suspendCategoryController()
    success = controller.suspendCategory(category_id)

    if not success:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"success": True}
