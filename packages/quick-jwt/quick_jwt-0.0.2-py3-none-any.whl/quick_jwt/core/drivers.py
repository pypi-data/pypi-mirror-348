from typing import Any, Type, Unpack

from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from pydantic import BaseModel

from quick_jwt.core._function_args import ModelValidateKwargs
from quick_jwt.core.abc import IDecodeDriverJWT, BaseJWT, IEncodeDriverJWT
from quick_jwt.dto import JWTTokensDTO


class PyJWTDecodeDriverJWT(IDecodeDriverJWT, BaseJWT):

    def _get_payload(
            self,
            bearer_token: HTTPAuthorizationCredentials | None,
            cookie_token: str | None
    ) -> Any:
        self._validate_call_function_is_called()
        self._validate_driver()

        token = None
        if bearer_token is not None and bearer_token.credentials is not None:
            token = bearer_token.credentials
        if cookie_token is not None:
            token = cookie_token
        if token is None:
            raise self._config.build_unauthorized_http_exception()

        try:
            payload = self._config.driver.decode(token, **self._config.build_decode_params())
        except InvalidTokenError:
            raise self._config.build_unauthorized_http_exception()

        return payload

    def _get_payload_optional(
            self,
            bearer_token: HTTPAuthorizationCredentials | None,
            cookie_token: str | None,
    ) -> Any | None:
        self._validate_call_function_is_called()
        self._validate_driver()

        token = None
        if bearer_token is not None and bearer_token.credentials is not None:
            token = bearer_token.credentials
        if cookie_token is not None:
            token = cookie_token
        if token is None:
            return None

        try:
            payload = self._config.driver.decode(token, **self._config.build_decode_params())
        except InvalidTokenError:
            return None

        return payload

    def _validate_driver(self):
        self._validate_call_function_is_called()

        if hasattr(self._config.driver, 'decode') is False or hasattr(self._config.driver, 'encode') is False:
            raise Exception(
                """
                QuickJWTConfig.driver received invalid driver. 
                Driver should have decode function.
                Default driver: PyJWT()
                """
            )


class PyJWTEncodeDriverJWT(IEncodeDriverJWT, BaseJWT):

    def __init__(
            self,
            access_payload: Type[BaseModel],
            refresh_payload: Type[BaseModel],
            **model_validate_kwargs: Unpack[ModelValidateKwargs],
    ):
        self._access_payload = access_payload
        self._refresh_payload = refresh_payload
        self._model_validate_kwargs = model_validate_kwargs

        super().__init__()

    async def create_jwt_tokens(
            self,
            access_payload: BaseModel,
            refresh_payload: BaseModel,
    ) -> JWTTokensDTO:
        access_token = await self.create_access_token(access_payload)
        refresh_token = await self.create_refresh_token(refresh_payload)

        return JWTTokensDTO(
            access=access_token,
            refresh=refresh_token,
        )

    async def create_access_token(self, access_payload: BaseModel) -> str:
        self._validate_call_function_is_called()
        self._validate_driver()

        access_payload = self._access_payload.model_validate(
            access_payload,
            **self._model_validate_kwargs
        )
        access_token = self._config.driver.encode(
            access_payload.model_dump(mode='json'),
            **self._config.build_encode_params()
        )
        self._response.set_cookie(value=access_token, **self._config.build_access_token_params())
        return access_token

    async def create_refresh_token(self, refresh_payload: BaseModel) -> str:
        self._validate_call_function_is_called()
        self._validate_driver()

        refresh_payload = self._refresh_payload.model_validate(
            refresh_payload,
            **self._model_validate_kwargs
        )
        refresh_token = self._config.driver.encode(
            refresh_payload.model_dump(mode='json'),
            **self._config.build_encode_params()
        )
        self._response.set_cookie(value=refresh_token, **self._config.build_refresh_token_params())
        return refresh_token

    def _validate_driver(self):
        self._validate_call_function_is_called()

        if hasattr(self._config.driver, 'decode') is False or hasattr(self._config.driver, 'encode') is False:
            raise Exception(
                """
                QuickJWTConfig.driver received invalid driver. 
                Driver should have decode function.
                Default driver: PyJWT()
                """
            )
