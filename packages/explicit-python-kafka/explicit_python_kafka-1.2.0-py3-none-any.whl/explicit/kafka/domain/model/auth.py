"""Параметры аутентификации."""
from typing import Final
from typing import Literal

from pydantic.main import BaseModel


SASL_PLAINTEXT: Final = 'SASL_PLAINTEXT'
SASL_SSL: Final = 'SASL_SSL'

SASL_PROTOCOLS = [SASL_PLAINTEXT, SASL_SSL]


class AbstractAuth(BaseModel):
    """Параметры аутентификации.

    Может нести параметры по-умолчанию и доп. валидацию.
    """


class AuthDisabled(AbstractAuth):
    """Аутентификация отключена."""


class SASLPlainAuth(AbstractAuth):

    sasl_username: str
    sasl_password: str
    sasl_mechanism: str = 'PLAIN'
    security_protocol: Literal['SASL_PLAINTEXT'] = SASL_PLAINTEXT

    class Config:
        allow_population_by_field_name = True
        fields = {
            'sasl_username': 'sasl.username',
            'sasl_password': 'sasl.password',
            'sasl_mechanism': 'sasl.mechanism',
            'security_protocol': 'security.protocol'
        }
