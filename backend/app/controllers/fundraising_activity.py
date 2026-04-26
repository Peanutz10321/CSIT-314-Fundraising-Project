from app.entities.FundraisingActivity import FundraisingActivity

class createFundraisingActivityController:
    
    def createFundraisingActivity(
        self,
        fundraiserID: int,
        title: str,
        currency: str,
        goal_amount: float,
        category: str,
        description: str = None,
        location: str = None,
        beneficiaryName: str = None,
        fundraiserName: str = None,
        deadline: str = None,
    ):
        return FundraisingActivity.createFundraisingActivity(
            fundraiserID, title, currency, goal_amount,
            category, description, location,
            beneficiaryName, fundraiserName, deadline,
        )
    
class viewFundraisingActivityController:

    def viewFundraisingActivity(self, activityID: str):
        return FundraisingActivity.viewFundraisingActivity(activityID)

class updateFundraisingActivityController:

    def updateFundraisingActivity(
        self,
        activityID: int,
        title: str = None,
        currency: str = None,
        goal_amount: float = None,
        category: str = None,
        description: str = None,
        location: str = None,
        beneficiaryName: str = None,
        fundraiserName: str = None,
        deadline: str = None,
    ):
        return FundraisingActivity.updateFundraisingActivity(
            activityID, title, currency, goal_amount,
            category, description, location,
            beneficiaryName, fundraiserName, deadline,
        )
    
class suspendFundraisingActivityController:

    def suspendFundraisingActivity(self, activityID: int):
        return FundraisingActivity.suspendFundraisingActivity(activityID)

class searchFundraisingActivityController:

    def searchFundraisingActivities(self, fundraiserID: int = None, keyword: str = None):
        return FundraisingActivity.searchFundraisingActivities(fundraiserID, keyword)

class searchCompletedActivitiesController:

    def searchCompletedActivities(self, fundraiserID: int = None):
        return FundraisingActivity.searchCompletedActivities(fundraiserID)

class viewCompletedActivityController:

    def viewCompletedActivity(self, activityID: int):
        return FundraisingActivity.viewCompletedActivity(activityID)

class getViewCountController:

    def getViewCount(self, activityID: int):
        return FundraisingActivity.getViewCount(activityID)
    
class getShortlistCountController:

    def getShortlistCount(self, activityID: int):
        return FundraisingActivity.getShortlistCount(activityID)
