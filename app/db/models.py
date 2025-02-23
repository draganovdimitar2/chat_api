from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Field(primary_key=True, index=True)
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)
    password_hash: str = Field(nullable=False, exclude=True)

    # a user can send many messages and receive many messages
    sent_messages: List["Message"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"}
    )
    received_messages: List["Message"] = Relationship(
        back_populates="recipient",
        sa_relationship_kwargs={"foreign_keys": "[Message.recipient_id]"}
    )


class Message(SQLModel, table=True):
    __tablename__ = 'messages'
    id: int = Field(primary_key=True, index=True)
    recipient_id: int = Field(foreign_key='users.id')
    sender_id: int = Field(foreign_key='users.id')
    content: str = Field(nullable=False)

    # Relationships to User
    sender: Optional[User] = Relationship(
        back_populates="sent_messages",
        sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"}
    )
    recipient: Optional[User] = Relationship(
        back_populates="received_messages",
        sa_relationship_kwargs={"foreign_keys": "[Message.recipient_id]"}
    )
