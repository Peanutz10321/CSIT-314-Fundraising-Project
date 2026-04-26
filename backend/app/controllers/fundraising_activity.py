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
    pass

class searchFundraisingActivityController:
    pass

class getViewCountController:

    def getViewCount(self, activityID: int):
        return FundraisingActivity.getViewCount(activityID)
    
class getShortlistCountController:

    def getShortlistCount(self, activityID: int):
        return FundraisingActivity.getShortlistCount(activityID)
