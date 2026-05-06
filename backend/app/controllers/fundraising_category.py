from app.entities.FundraisingCategory import FundraisingCategory


class createFundraisingCategoryController:
    def createFundraisingCategory(self, name: str, description: str = None):
        return FundraisingCategory.createFundraisingCategory(name, description)


class viewFundraisingCategoryController:
    def viewFundraisingCategory(self, category_id: int):
        return FundraisingCategory.viewFundraisingCategory(category_id)


class updateFundraisingCategoryController:
    def updateFundraisingCategory(self, category_id: int, name: str = None, description: str = None):
        return FundraisingCategory.updateFundraisingCategory(category_id, name, description)


class suspendFundraisingCategoryController:
    def suspendFundraisingCategory(self, category_id: int):
        return FundraisingCategory.suspendFundraisingCategory(category_id)


class searchFundraisingCategoryController:
    def searchFundraisingCategory(self, keyword: str = None):
        return FundraisingCategory.searchFundraisingCategory(keyword)
