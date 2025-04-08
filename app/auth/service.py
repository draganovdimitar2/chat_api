from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.auth.utils import get_password_hash, verify_password
from app.auth.schemas import UserRegistrationModel, ChangeUserPassword
from app.db.models import User


class UserService:
    async def get_user_by_credential(self, credential: str,
                                     session: AsyncSession) -> User | None:
        """
        Fetch a user from the database based on provided credentials (email or username).

        Args:
            credential (str): The user's email or username.
            session (AsyncSession): The database session.

        Returns:
            User | None: The retrieved user instance if found, otherwise None.
        """
        statement = select(User).where((User.username == credential) | (User.email == credential))

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_registration(self, user_data: UserRegistrationModel, session: AsyncSession) -> User:
        """
        Registers a new user in the database.

        Args:
            user_data (UserRegistrationModel): The user registration data.
            session (AsyncSession): The database session.

        Returns:
            User: The newly created user instance.
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

        Args:
            credentials (str): The user's email or username.
            session (AsyncSession): The database session.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user = await self.get_user_by_credential(credentials, session)

        return True if user is not None else False

    async def authenticate_user(self, credential: str, password: str, session: AsyncSession) -> User | None:
        """
        Authenticates a user based on provided credentials and password.

        Args:
            credential (str): The user's email or username.
            password (str): The user's plain text password.
            session (AsyncSession): The database session.

        Returns:
            User | None: The authenticated user instance if successful, otherwise None.
        """
        user = await self.get_user_by_credential(credential, session)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    async def change_user_password(self, new_password: ChangeUserPassword, credential: dict, session: AsyncSession):
        """
        Changes the password for the authenticated user.

        Args:
            new_password (ChangeUserPassword): The old and new passwords.
            credential (dict): The user's credentials (e.g., username).
            session (AsyncSession): The database session.

        Raises:
            HTTPException:
                - 404: If the user is not found.
                - 403: If the old password is incorrect.

        Returns:
            dict: A success message indicating the password was changed successfully.
        """
        current_user = await self.get_user_by_credential(credential.get('username'), session)
        if not current_user:
            raise HTTPException(status_code=404, detail='User not found!')
        if not verify_password(new_password.old_password, current_user.password_hash):
            raise HTTPException(status_code=403, detail="Old password doesn't match!")

        current_user.password_hash = get_password_hash(new_password.new_password)
        await session.commit()
        return {'message': 'Password changed successfully!'}
