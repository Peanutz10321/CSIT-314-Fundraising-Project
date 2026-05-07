from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.access_control import require_roles
from app.schemas.fundraising_category import (
    FundraisingCategoryCreate,
    FundraisingCategoryUpdate,
    FundraisingCategoryResponse,
    FundraisingCategorySearchResponse,
)
from app.controllers.fundraising_category import (
    createFundraisingCategoryController,
    viewFundraisingCategoryController,
    updateFundraisingCategoryController,
    suspendFundraisingCategoryController,
    searchFundraisingCategoryController,
)

router = APIRouter(prefix="/api/category", tags=["Fundraising Categories"])

require_platform_manager = require_roles("PLATFORM_MANAGER")
require_platform_fundraiser_or_donee = require_roles("PLATFORM_MANAGER", "FUNDRAISER", "DONEE")


@router.post("/", response_model=FundraisingCategoryResponse, status_code=201)
def create_category(
    payload: FundraisingCategoryCreate,
    _: None = Depends(require_platform_manager),
):
    controller = createFundraisingCategoryController()
    result = controller.createFundraisingCategory(payload.name, payload.description)

    if result == "duplicate_name":
        raise HTTPException(status_code=400, detail="A category with that name already exists")

    return result


@router.get("/", response_model=FundraisingCategorySearchResponse)
def search_categories(
    keyword: str | None = Query(default=None),
    _: None = Depends(require_platform_fundraiser_or_donee),
):
    controller = searchFundraisingCategoryController()
    categories = controller.searchFundraisingCategory(keyword)

    return {"total": len(categories), "data": categories}


@router.get("/{category_id}", response_model=FundraisingCategoryResponse)
def get_category(
    category_id: int,
    _: None = Depends(require_platform_manager),
):
    controller = viewFundraisingCategoryController()
    result = controller.viewFundraisingCategory(category_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Category not found")

    return result


@router.patch("/{category_id}", response_model=FundraisingCategoryResponse)
def update_category(
    category_id: int,
    payload: FundraisingCategoryUpdate,
    _: None = Depends(require_platform_manager),
):
    controller = updateFundraisingCategoryController()
    result = controller.updateFundraisingCategory(category_id, payload.name, payload.description)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Category not found")

    if result == "duplicate_name":
        raise HTTPException(status_code=400, detail="A category with that name already exists")

    return result


@router.patch("/{category_id}/suspend")
def suspend_category(
    category_id: int,
    _: None = Depends(require_platform_manager),
):
    controller = suspendFundraisingCategoryController()
    success = controller.suspendFundraisingCategory(category_id)

    if not success:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"success": True}
