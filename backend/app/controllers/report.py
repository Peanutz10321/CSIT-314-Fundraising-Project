from app.entities.Report import Report


class dailyReportController:
    def generateDailyReport(self, date: str):
        return Report.generateDailyReport(date)

class weeklyReportController:
    def generateWeeklyReport(self, startDate: str, endDate: str):
        return Report.generateWeeklyReport(startDate, endDate)

class monthlyReportController:
    def generateMonthlyReport(self, month: str):
        return Report.generateMonthlyReport(month)