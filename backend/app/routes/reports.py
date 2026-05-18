from fastapi import APIRouter, Depends, HTTPException, Query
from app.controllers.report import dailyReportController, weeklyReportController, monthlyReportController
from app.middleware.access_control import require_roles

router = APIRouter(prefix="/api/report", tags=["Platform Reports"])

require_platform_manager = require_roles("PLATFORM_MANAGER")


@router.get("/daily")
def generateDailyReport(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    _: None = Depends(require_platform_manager),
):
    controller = dailyReportController()
    result = controller.generateDailyReport(date)

    if result == "invalid_date":
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    return result


@router.get("/weekly")
def generateWeeklyReport(
    startDate: str = Query(..., description="Week start date in YYYY-MM-DD format"),
    endDate: str = Query(..., description="Week end date in YYYY-MM-DD format"),
    _: None = Depends(require_platform_manager),
):
    controller = weeklyReportController()
    result = controller.generateWeeklyReport(startDate, endDate)

    if result == "invalid_date":
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    return result


@router.get("/monthly")
def generateMonthlyReport(
    month: str = Query(..., description="Month in YYYY-MM format"),
    _: None = Depends(require_platform_manager),
):
    controller = monthlyReportController()
    result = controller.generateMonthlyReport(month)

    if result == "invalid_month":
        raise HTTPException(status_code=400, detail="Invalid month format. Use YYYY-MM.")

    return result
