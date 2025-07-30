from pydantic import BaseModel


class User(BaseModel):
    user_id: str = "0"
    group_id: str = "0"
    nickname: str = "Master"
    avatar: str = "https://localhost:8080/avatar/0.png"
    group_avatar: str = "https://localhost:8080/group_avatar/0.png"
    permission: int = 3


class Event(BaseModel):
    user: User = User()
    to_me: bool = False
    at: list[str] = []
    image_list: list[str] = []
    is_private: bool = False


class Config(BaseModel):
    Bot_Nickname: str = "C酱"
    plugins: list[str] = []
    plugin_dirs: list[str] = []
    master: User = User()


from clovers.config import config as clovers_config

__config__ = Config.model_validate(clovers_config.get("clovers", {}))
clovers_config["clovers"] = __config__.model_dump()
