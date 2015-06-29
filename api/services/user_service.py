from models.base import db
from models.user import User


class UserService(object):
    def init():
        pass

    def find_by(self, field, value):
        user = User.query.filter(getattr(User, field) == value).first()

        return user

    def create(self, username, password):
        existing_user = self.find_by('username', username)

        if existing_user:
            return False

        new_user = User(username, password)

        db.session.add(new_user)
        db.session.commit()

        return new_user
