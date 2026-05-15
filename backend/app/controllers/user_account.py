from app.entities.UserAccount import UserAccount


class loginController:

    def validateCredentials(self, email: str, password: str):
        return UserAccount.validateCredentials(email, password)

class logoutController:

    def invalidateSession(self, token: str) -> bool:
        return UserAccount.invalidateSession(token)

class createUserAccountController:

    def createUserAccount(self, name: str, email: str, password: str, userProfile: str, phoneNo: str = None, address: str = None, dob: str = None, status: str = "ACTIVE"):
        return UserAccount.createUserAccount(name, email, password, userProfile, phoneNo, address, dob, status)

class viewUserAccountController:

    def viewUserAccount(self, accountID: int):
        return UserAccount.viewUserAccount(accountID)

class updateUserAccountController:

    def updateUserAccount(self, accountID: int, name: str = None, password: str = None, phone_no: str = None, address: str = None, dob: str = None, userProfile: str = None,  status: str = None):
        return UserAccount.updateUserAccount(accountID, name, password, phone_no, address, dob, userProfile, status)

class suspendUserAccountController:

    def suspendUserAccount(self, accountID: int):
        return UserAccount.suspendUserAccount(accountID)

class searchUserAccountController:
    
    def searchUserAccount(self, keyword: str):
        return UserAccount.searchUserAccount(keyword)

    
    
    