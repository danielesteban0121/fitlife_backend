class LoginUser:

    def __init__(self, user_repository, password_hasher, jwt_manager):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_manager = jwt_manager

    async def execute(self, email: str, password: str):

        user = await self.user_repository.find_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not self.password_hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")

        access_token, expires_in = self.jwt_manager.create_access_token(
            user_id=str(user.id),
            role=user.role,
        )

        refresh_token = self.jwt_manager.create_refresh_token(
            user_id=str(user.id),
            role=user.role,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
        }
