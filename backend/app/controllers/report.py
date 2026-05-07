from app.entities.Report import Report


class ReportController:
    def get_daily_report(self, date: str):
        return Report.generate_daily_report(date)

    def get_weekly_report(self, week_start: str):
        return Report.generate_weekly_report(week_start)

    def get_monthly_report(self, month: str):
        return Report.generate_monthly_report(month)