class BaseNotificationMessage:
    username = None
    avatar = None
    des_name = None
    des_image = None

    @classmethod
    def create_new(cls, username="", avatar="", des_name="", des_image=""):
        return cls(
            username=username,
            avatar=avatar,
            des_name=des_name,
            des_image=des_image,
        )

    def to_dict(self):
        return {
            "username": self.username,
            "avatar": self.avatar,
            "desName": self.des_name,
            "desImage": self.des_image,
        }


class UserNotificationMessage(BaseNotificationMessage):
    pass
