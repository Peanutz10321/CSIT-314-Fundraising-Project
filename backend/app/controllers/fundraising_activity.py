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

    def viewFundraisingActivity(self, activityID: int):
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

    def searchCompletedActivity(self, fundraiserID: int = None, query: str = None):
        return FundraisingActivity.searchCompletedActivity(fundraiserID)

class viewCompletedActivityController:

    def getCompletedActivities(self, activityID: int):
        return FundraisingActivity.getCompletedActivities(activityID)
