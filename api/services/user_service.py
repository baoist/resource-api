from models.base import db
from models.user import User


class UserService(object):
    def init():
        pass


    def find_by(self, field, value):
        user = User.query.filter(getattr(User, field) == value).first()

        return user
