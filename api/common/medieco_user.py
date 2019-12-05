class MediecoUser():
    ums_medieco_user = {}
    upgrade_mode = ''

    def __init__(self,dict_medieco_user):
        self.ums_medieco_user = dict_medieco_user

    def is_active(self):
        return self.ums_medieco_user['is_active'] == 1

    @property
    def id(self):
        return self.ums_medieco_user['id']

    @property
    def username(self):
        return self.ums_medieco_user['username']

    @property
    def avatar(self):
        return self.ums_medieco_user['avatar']

    @property
    def uuid(self):
        return self.ums_medieco_user['uuid']

    @property
    def email(self):
        return self.ums_medieco_user['email']

    def _dict_(self):
        return self.ums_medieco_user
