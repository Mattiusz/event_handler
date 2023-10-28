from pydantic import BaseModel

UserId = int


class User(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserWithId(User):
    id: UserId


class UserKey(BaseModel):
    id: UserId
