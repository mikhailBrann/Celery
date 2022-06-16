import flask
import pydantic
from hashlib import md5
from flask import request as fk_request
from flask.views import MethodView

from lib.settings import Session
from lib.models import UserModel, AdvertisementModel
from lib.validators import UserValidator, AdvertisementValidate
from lib.errosCls import HttpErrors
from celery.result import AsyncResult

from lib.celeryCls import celery_app


@celery_app.task()
def get_user():
    current_session = Session()
    users_data = current_session.query(UserModel).all()
    result = dict()
    for user in users_data:
        result[user.id] = {
            "id": user.id,
            "user_name": user.user_name,
            "is_authorized": user.is_authorized
        }

    return flask.jsonify(result)


class UserView(MethodView):
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery_app)
        return flask.jsonify({'status': task.status, 'result': task.result})

    def post(self):
        # валидация
        try:
            input_data = UserValidator(**fk_request.json).dict()
        except pydantic.ValidationError as err:
            raise HttpErrors(400, err.errors())

        # хешируем пароль
        input_data['password'] = str(md5(input_data['password'].encode()).hexdigest())

        new_user = UserModel(**input_data)
        current_session = Session()

        current_session.add(new_user)
        current_session.commit()

        return flask.jsonify({
            'id': new_user.id,
            'user_name': new_user.user_name
        })

    def patch(self):
        current_session = Session()
        input_data = dict(fk_request.json)
        check_password = str(md5(input_data['password'].encode()).hexdigest())
        user_data = current_session.query(UserModel).filter(
            UserModel.user_name == input_data['user_name'],
            UserModel.password == check_password
        ).first()

        if user_data:
            user_data.is_authorized = True
            current_session.commit()
            return flask.jsonify({user_data.id: user_data.is_authorized})
        else:
            raise HttpErrors(400, 'user_name or password uncorrected')


class AdvertisementView(MethodView):
    def get(self):
        current_session = Session()
        advertisement_data = current_session.query(AdvertisementModel).all()
        result = dict()
        for advertisement in advertisement_data:
            result[advertisement.id] = {
                "id": advertisement.id,
                "title": advertisement.title,
                "owner": advertisement.owner
            }

        return flask.jsonify(result)

    def post(self):
        # валидация
        try:
            input_data = AdvertisementValidate(**fk_request.json).dict()
        except pydantic.ValidationError as err:
            raise HttpErrors(400, err.errors())

        current_session = Session()
        new_adv = AdvertisementModel(**input_data)

        current_session.add(new_adv)
        current_session.commit()

        return flask.jsonify({
            'id': new_adv.id,
            'title': new_adv.title
        })

    def patch(self):
        current_session = Session()
        input_data = dict(fk_request.json)
        adv_data = current_session.query(AdvertisementModel).filter(
            AdvertisementModel.id == input_data['id'],
            AdvertisementModel.owner == input_data['owner']
        ).first()

        if adv_data:
            if 'title' in input_data:
                adv_data.title = input_data['title']
            if 'description' in input_data:
                adv_data.description = input_data['description']
            current_session.commit()
        else:
            raise HttpErrors(400, f"invalid input data")

        return flask.jsonify({'result': f"Advertisement №{adv_data.id} successfully changed!"})

    def delete(self):
        current_session = Session()
        input_data = dict(fk_request.json)
        adv_data = current_session.query(AdvertisementModel).filter(
            AdvertisementModel.id == input_data['id'],
            AdvertisementModel.owner == input_data['owner']
        ).first()

        if adv_data:
            current_session.delete(adv_data)
            current_session.commit()

            return flask.jsonify({'result': f"Advertisement №{input_data['id']} successfully delete!"})
        else:
            raise HttpErrors(400, f"invalid input data")