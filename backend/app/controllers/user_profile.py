from app.entities.UserProfile import UserProfile

class createUserProfileController:

    def createUserProfile(self, name: str, description: str, status: str = "ACTIVE"):
        return UserProfile.createUserProfile(name, description, status)

class viewUserProfileController:

    def getUserProfileByID(self, profileID: int):
        return UserProfile.getUserProfileByID(profileID)

class updateUserProfileController:

    def updateUserProfile(self, profileID: int, name: str, description: str, status: str | None = None):
        return UserProfile.updateUserProfile(profileID, name, description, status)

class suspendUserProfileController:

    def suspendUserProfile(self, profileID: int):
        return UserProfile.suspendUserProfile(profileID)

class searchUserProfileController:

    def searchUserProfile(self, keyword: str | None):
        return UserProfile.searchUserProfile(keyword)
   
    
    

    
    
    
    