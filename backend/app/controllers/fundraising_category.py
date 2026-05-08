from app.entities.FundraisingCategory import FundraisingCategory


class createCategoryController:
    def createFundraisingCategory(self, name: str, description: str = None):
        return FundraisingCategory.createFundraisingCategory(name, description)


class viewFundraisingCategoryController:
    def getCategory(self, categoryID: int):
        return FundraisingCategory.getCategory(categoryID)


class updateCategoryController:
    def updateCategory(self, categoryID: int, name: str = None, description: str = None):
        return FundraisingCategory.updateCategory(categoryID, name, description)


class suspendCategoryController:
    def suspendCategory(self, categoryID: int):
        return FundraisingCategory.suspendCategory(categoryID)


class searchFundraisingCategoryController:
    def searchCategory(self, keyword: str = None):
        return FundraisingCategory.searchCategory(keyword)
