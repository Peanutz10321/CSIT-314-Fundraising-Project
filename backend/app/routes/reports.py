from fastapi import APIRouter, Depends, HTTPException, Query
from app.controllers.report import dailyReportController, weeklyReportController, monthlyReportController
from app.middleware.access_control import require_roles

router = APIRouter(prefix="/api/report", tags=["Platform Reports"])

require_platform_manager = require_roles("PLATFORM_MANAGER")


@router.get("/daily")
def get_daily_report(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    _: None = Depends(require_platform_manager),
):
    controller = dailyReportController()
    result = controller.generateDailyReport(date)

    if result == "invalid_date":
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    return result


@router.get("/weekly")
def get_weekly_report(
    week_start: str = Query(..., description="Week start date in YYYY-MM-DD format"),
    _: None = Depends(require_platform_manager),
):
    controller = weeklyReportController()
    result = controller.generateWeeklyReport(week_start)

    if result == "invalid_date":
        raise HTTPException(status_code=400, detail="Invalid week_start format. Use YYYY-MM-DD.")

    return result


@router.get("/monthly")
def get_monthly_report(
    month: str = Query(..., description="Month in YYYY-MM format"),
    _: None = Depends(require_platform_manager),
):
    controller = monthlyReportController()
    result = controller.generateMonthlyReport(month)

    if result == "invalid_month":
        raise HTTPException(status_code=400, detail="Invalid month format. Use YYYY-MM.")

    return result

'''
from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta

from app.middleware.access_control import require_roles
from app.database import SessionLocal
from app.entities.FundraisingActivity import FundraisingActivity
from app.entities.UserAccount import UserAccount
from app.entities.FundraisingCategory import FundraisingCategory

router = APIRouter(prefix="/api/reports", tags=["Reports"])

require_platform_manager = require_roles("PLATFORM_MANAGER")


def _get_period_start(period: str) -> datetime:
    now = datetime.now()
    if period == "daily":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "weekly":
        return (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    return (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)


@router.get("/")
def get_reports(
    period: str = Query(default="daily", pattern="^(daily|weekly|monthly)$"),
    _: None = Depends(require_platform_manager),
):
    db = SessionLocal()
    try:
        period_start = _get_period_start(period)

        all_activities = db.query(FundraisingActivity).all()
        period_activities = [a for a in all_activities if a.date_created >= period_start]

        raised = sum(a.current_amount or 0 for a in period_activities)
        active_activities = sum(1 for a in all_activities if a.status == "ACTIVE")
        completed_activities = sum(1 for a in all_activities if a.status == "COMPLETED")
        views = sum(a.view_count or 0 for a in period_activities)
        active_users = db.query(UserAccount).filter(UserAccount.status == "ACTIVE").count()

        categories = db.query(FundraisingCategory).all()
        raised_by_category = []
        for cat in categories:
            cat_raised = sum(
                a.current_amount or 0
                for a in all_activities
                if a.category == cat.name and a.date_created >= period_start
            )
            raised_by_category.append({"name": cat.name, "amount": cat_raised})

        top_activities = sorted(all_activities, key=lambda a: a.view_count or 0, reverse=True)[:5]
        most_viewed = [
            {"title": a.title, "view_count": a.view_count or 0}
            for a in top_activities
        ]

        return {
            "period": period,
            "raised": raised,
            "active_activities": active_activities,
            "completed_activities": completed_activities,
            "views": views,
            "active_users": active_users,
            "raised_by_category": raised_by_category,
            "most_viewed_activities": most_viewed,
        }
    finally:
        db.close()
'''