import pydantic
from flask import request as fk_request

from lib.settings import Session
from lib.models import UserModel
from lib.errosCls import HttpErrors


class UserValidator(pydantic.BaseModel):
    user_name: str
    password: str
    email: str

    @pydantic.validator('password')
    def strong_pass(cls, value):
        if len(value) < 9:
            raise ValueError('password length must be more than 9 characters')
        return value

    @pydantic.validator('user_name')
    def user_exist(cls, value):
        current_session = Session()
        input_data = dict(fk_request.json)
        user_data = current_session.query(UserModel).filter(UserModel.user_name == input_data['user_name']).first()
        if user_data:
            raise HttpErrors(400, f"a user with the same name ({input_data['user_name']}) already exists")
        return value

    @pydantic.validator('email')
    def email_exist(cls, value):
        current_session = Session()
        input_data = dict(fk_request.json)
        user_data = current_session.query(UserModel).filter(UserModel.email == input_data['email']).first()
        if user_data:
            raise HttpErrors(400, f"a user with the same email ({input_data['email']}) already exists")
        return value


class AdvertisementValidate(pydantic.BaseModel):
    title: str
    description: str
    owner: int

    @pydantic.validator('owner')
    def user_is_authorized(cls, value):
        current_session = Session()
        input_data = dict(fk_request.json)
        user_data = current_session.query(UserModel).filter(UserModel.id == input_data['owner']).first()

        if user_data.is_authorized == False:
            raise HttpErrors(400, f" user ({user_data.user_name}) not authorized!")
        return value

