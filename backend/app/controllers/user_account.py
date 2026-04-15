from app.entities.UserAccount import UserAccount


class loginController:
    def validateCredentials(self, email: str, password: str):
        return UserAccount.validateCredentials(email, password)


class logoutController:
    def invalidateSession(self, token: str) -> bool:
        return UserAccount.invalidateSession(token)

    
    
    