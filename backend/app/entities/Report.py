from datetime import datetime, timedelta
from sqlalchemy import func
from app.database import SessionLocal
from app.entities.FundraisingActivity import FundraisingActivity
from app.entities.UserAccount import UserAccount


class Report:

    @staticmethod
    def _build_report(start_date, end_date, period: str):
        db = SessionLocal()

        try:
            period_filter = [
                FundraisingActivity.date_created >= start_date,
                FundraisingActivity.date_created < end_date,
            ]

            total_raised = (
                db.query(func.coalesce(func.sum(FundraisingActivity.current_amount), 0))
                .filter(*period_filter)
                .scalar()
            )

            active_activities = (
                db.query(FundraisingActivity)
                .filter(FundraisingActivity.status == "ACTIVE")
                .filter(*period_filter)
                .count()
            )

            completed_activities = (
                db.query(FundraisingActivity)
                .filter(FundraisingActivity.status == "COMPLETED")
                .filter(*period_filter)
                .count()
            )

            views = (
                db.query(func.coalesce(func.sum(FundraisingActivity.view_count), 0))
                .filter(*period_filter)
                .scalar()
            )

            active_users = (
                db.query(UserAccount)
                .filter(UserAccount.status == "ACTIVE")
                .count()
            )

            from app.entities.FundraisingCategory import FundraisingCategory

            raised_by_category_rows = (
                db.query(
                    FundraisingCategory.name,
                    func.coalesce(func.sum(FundraisingActivity.current_amount), 0),
                    func.count(FundraisingActivity.id),
                )
                .join(FundraisingCategory, FundraisingActivity.category_id == FundraisingCategory.id)
                .filter(*period_filter)
                .group_by(FundraisingCategory.name)
                .all()
            )

            raised_by_category = [
                {
                    "category": category or "Uncategorised",
                    "total_raised": float(total_raised_by_category or 0),
                    "activity_count": int(activity_count or 0),
                }
                for category, total_raised_by_category, activity_count in raised_by_category_rows
            ]

            most_viewed_rows = (
                db.query(FundraisingActivity)
                .filter(*period_filter)
                .order_by(FundraisingActivity.view_count.desc())
                .limit(5)
                .all()
            )

            most_viewed_activities = [
                {
                    "id": activity.id,
                    "title": activity.title,
                    "views": activity.view_count or 0,
                }
                for activity in most_viewed_rows
            ]

            return {
                "period": period,
                "start_date": start_date.date().isoformat(),
                "end_date": end_date.date().isoformat(),

                "summary": {
                    "total_raised": float(total_raised or 0),
                    "active_activities": active_activities,
                    "completed_activities": completed_activities,
                    "views": int(views or 0),
                    "active_users": active_users,
                },

                "raised_by_category": raised_by_category,
                "most_viewed_activities": most_viewed_activities,
            }

        finally:
            db.close()

    @staticmethod
    def generateDailyReport(date: str):
        try:
            start_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return "invalid_date"

        end_date = start_date + timedelta(days=1)
        return Report._build_report(start_date, end_date, "daily")

    @staticmethod
    def generateWeeklyReport(week_start: str):
        try:
            start_date = datetime.strptime(week_start, "%Y-%m-%d")
        except ValueError:
            return "invalid_date"

        end_date = start_date + timedelta(days=7)
        return Report._build_report(start_date, end_date, "weekly")

    @staticmethod
    def generateMonthlyReport(month: str):
        try:
            start_date = datetime.strptime(month, "%Y-%m")
        except ValueError:
            return "invalid_month"

        if start_date.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1)

        return Report._build_report(start_date, end_date, "monthly")