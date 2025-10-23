from pydantic import BaseModel, EmailStr, model_validator, ConfigDict


class CreateUserPost(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    re_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.re_password:
            raise ValueError("Passwords don't match")
        return self
    

class LoginUserPost(BaseModel):
    email: EmailStr
    password: str


class UserToDB(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserFromDB(BaseModel):
    email: EmailStr
    password: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
