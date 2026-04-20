from app.entities.UserAccount import UserAccount


class loginController:
    def validateCredentials(self, email: str, password: str):
        return UserAccount.validateCredentials(email, password)


class logoutController:
    def invalidateSession(self, token: str) -> bool:
        return UserAccount.invalidateSession(token)

class createUserAccountController:
    def createUserAccount(self, name: str, email: str, password: str, user_profile: str, phone_no: str = None, address: str = None, dob: str = None, status: str = "ACTIVE"):
        return UserAccount.createUserAccount(name, email, password, user_profile, phone_no, address, dob, status)

class viewUserAccountController:
    def viewUserAccount(self, user_id: int):
        return UserAccount.viewUserAccount(user_id)

class updateUserAccountController:
    def updateUserAccount(self, user_id: int, name: str = None, email: str = None, password: str = None, user_profile: str = None, phone_no: str = None, address: str = None, dob: str = None, status: str = None):
        return UserAccount.updateUserAccount(user_id, name, email, password, user_profile, phone_no, address, dob, status)

class suspendUserAccountController:
    def suspendUserAccount(self, user_id: int):
        return UserAccount.suspendUserAccount(user_id)

class searchUserAccountController:
    def searchUserAccount(self, keyword: str):
        return UserAccount.searchUserAccount(keyword)

    
    
    