from app.entities.Report import Report


class dailyReportController:
    def generateDailyReport(self, date: str):
        return Report.generateDailyReport(date)

class weeklyReportController:
    def generateWeeklyReport(self, week_start: str):
        return Report.generateWeeklyReport(week_start)

class monthlyReportController:
    def generateMonthlyReport(self, month: str):
        return Report.generateMonthlyReport(month)