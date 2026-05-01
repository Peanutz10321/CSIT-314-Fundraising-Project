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

    def viewUserAccount(self, accountID: int):
        return UserAccount.viewUserAccount(accountID)

class updateUserAccountController:

    def updateUserAccount(self, accountID: int, name: str = None, password: str = None, user_profile: str = None, phone_no: str = None, address: str = None, dob: str = None, status: str = None):
        return UserAccount.updateUserAccount(accountID, name, password, user_profile, phone_no, address, dob, status)

class suspendUserAccountController:

    def suspendUserAccount(self, profileID: int):
        return UserAccount.suspendUserAccount(profileID)

class searchUserAccountController:
    
    def searchUserAccount(self, keyword: str):
        return UserAccount.searchUserAccount(keyword)

    
    
    