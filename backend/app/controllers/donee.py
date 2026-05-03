from app.entities.FundraisingActivity import FundraisingActivity
from app.entities.FavoriteList import FavoriteList

class doneeSearchFundraisingActivityController:

    def searchFundraisingActivity(self, keyword: str):
        return FundraisingActivity.searchFundraisingActivity(keyword=keyword)

class doneeViewFundraisingActivityController:

    def doneeViewFundraisingActivity(self, activityID: int):
        return FundraisingActivity.doneeViewFundraisingActivity(activityID)
    
class saveFundraisingActivityController:

    def saveFundraisingActivity(self, doneeID: int, activityID: int):
        return FavoriteList.saveFundraisingActivity(doneeID, activityID)
    
class searchFavoriteListController:

    def searchFavoriteList(self, doneeID: int, keyword: str = None):
        return FavoriteList.searchFavoriteList(doneeID, keyword)

class doneeSearchCompletedActivitiesController:

    def searchCompletedActivity(self, query: str = None):
        return FundraisingActivity.searchCompletedActivity(query=query)
    
class doneeViewCompletedController:
    def doneeGetCompletedActivities(self, activityID: int):
        return FundraisingActivity.getCompletedActivities(activityID)
    
