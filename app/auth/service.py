from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete
from app.auth.utils import get_password_hash, verify_password
from app.auth.schemas import UserRegistrationModel, ChangeUserPassword, UserDetailsResponse
from app.db.models import User


class UserService:
    async def get_user_by_credential(self, credential: str,
                                     session: AsyncSession) -> User | None:
        """
        Fetch a user from the database based on provided credentials (email or username).
        """
        statement = select(User).where((User.username == credential) | (User.email == credential))

        result = await session.exec(statement)

        user = result.first()
        return user

    async def user_registration(self, user_data: UserRegistrationModel, session: AsyncSession) -> User:
        """
        Registers a new user in the database.
        """
        user_data_dict = user_data.model_dump()  # convert the model into dict

        new_user = User(
            **user_data_dict
        )
        new_user.password_hash = get_password_hash(user_data_dict['password'])  # to add the hashed password to the db
        session.add(new_user)
        await session.commit()
        return new_user

    async def user_exists(self, credentials: str, session: AsyncSession) -> bool:
        """
        Checks whether a user exists in the database based on credentials (email or username).
        """
        user = await self.get_user_by_credential(credentials, session)

        return True if user is not None else False

    async def authenticate_user(self, credential: str, password: str, session: AsyncSession) -> User | None:
        """
        Authenticates a user based on provided credentials and password.
        """
        user = await self.get_user_by_credential(credential, session)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    async def change_user_password(self, new_password: ChangeUserPassword, credential: dict, session: AsyncSession):
        """
        Changes the password for the authenticated user.
        """
        current_user = await self.get_user_by_credential(credential.get('username'), session)
        if not current_user:
            raise HTTPException(status_code=404, detail='User not found!')
        if not verify_password(new_password.old_password, current_user.password_hash):
            raise HTTPException(status_code=403, detail="Old password doesn't match!")

        current_user.password_hash = get_password_hash(new_password.new_password)
        await session.commit()
        return {'message': 'Password changed successfully!'}

    async def get_user_details(self, credentials: dict, session: AsyncSession) -> UserDetailsResponse:
        """
        Retrieves the user details for a given username.
        """
        user = await self.get_user_by_credential(credentials.get('username'), session)
        if not user:
            raise HTTPException(status_code=404, detail='User not found!')
        return UserDetailsResponse(**user.__dict__)  # convert ORM model instance to dict and then unpack it

    async def delete_user(self, credentials: dict, session: AsyncSession) -> dict:
        """
        Deletes user from db.
        """
        user = await self.get_user_by_credential(credentials.get('username'), session)
        if not user:
            raise HTTPException(status_code=404, detail='User not found!')
        await session.delete(user)
        await session.commit()
        return {"message": "User deleted successfully!"}
