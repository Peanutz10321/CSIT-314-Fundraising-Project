from app.entities.UserProfile import UserProfile


class createUserProfileController:
    def createUserProfile(self, name_of_role: str, description: str, status: str = "ACTIVE"):
        return UserProfile.createUserProfile(name_of_role, description, status)


class viewUserProfileController:
    def getUserProfileByID(self, profile_id: int):
        return UserProfile.getUserProfileByID(profile_id)


class updateUserProfileController:
    def updateUserProfile(self, profile_id: int, name: str, description: str, status: str = "ACTIVE"):
        return UserProfile.updateUserProfile(profile_id, name, description, status)


class suspendUserProfileController:
    def suspendUserProfile(self, profile_id: int):
        return UserProfile.suspendUserProfile(profile_id)


class searchUserProfileController:
    def searchUserProfile(self, keyword: str | None):
        return UserProfile.searchUserProfile(keyword)
   
    
    

    
    
    
    