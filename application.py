from lib.views import UserView, AdvertisementView
from lib.settings import Base, application, engine


# проверка миграций
Base.metadata.create_all(engine)


# подключение роутинга
application.add_url_rule(
    '/user/<task_id>',
    view_func=UserView.as_view('check_user'),
    methods=['GET']
)
application.add_url_rule(
    '/user/',
    view_func=UserView.as_view('create_user'),
    methods=['POST', 'PATCH']
)

# подключение роутинга
application.add_url_rule(
    '/advertisement/',
    view_func=AdvertisementView.as_view('create_advertisement'),
    methods=['GET', 'POST', 'PATCH', 'DELETE']
)


