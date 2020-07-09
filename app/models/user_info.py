class UserInfo:
    user_id: int
    username: str
    password: str

    def __init__(self, user_id, username, pwd):
        self.username = username
        self.password = pwd
        self.user_id = user_id
