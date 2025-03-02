from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.auth.utils import get_password_hash, verify_password
from app.auth.schemas import UserRegistrationModel
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
