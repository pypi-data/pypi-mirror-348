"""Набор конфигураций."""
from typing import TYPE_CHECKING
from typing import Dict
from typing import Union

from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.utils import import_string

from .auth import AbstractAuth
from .auth import AuthDisabled


if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr


class BaseConfig(BaseModel):
    """Общие параметры издателя и подписчика."""

    bootstrap__servers: str

    auth: AbstractAuth = AuthDisabled()

    class Config:
        fields = {  # Aliases
            'bootstrap__servers': 'bootstrap.servers',
        }

    def set_auth(self, auth: Dict) -> AbstractAuth:
        auth_cls = import_string(auth['BACKEND'])
        assert issubclass(auth_cls, AbstractAuth)
        self.auth = auth_cls(**auth['OPTIONS'])
        return self.auth

    def dict(
        self, *args, exclude: Union['AbstractSetIntStr', None] = None, **kwargs
    ) -> dict:
        """Возвращает пареметры, пригодные для передачи в низкоуровневый пакет взаимодействия."""
        self_dict = super().dict(*args, exclude=(exclude or set()) | {'auth'}, **kwargs)
        auth_dict = self.auth.dict(by_alias=True)
        return self_dict | auth_dict


class PublishConfig(BaseConfig):

    class Config(BaseConfig.Config):
        fields = {
            **BaseConfig.Config.fields
        }


class SubscribeConfig(BaseConfig):

    group__id: str
    auto__offset__reset: str = Field('earliest', const=True)

    class Config(BaseConfig.Config):
        fields = {
            'auto__offset__reset': 'auto.offset.reset',
            'group__id': 'group.id',
            **BaseConfig.Config.fields
        }
