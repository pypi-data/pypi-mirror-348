from __future__ import annotations
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict, PrivateAttr

if TYPE_CHECKING:
    from brivo.brivo_client import BaseBrivoClient


class BaseBrivoModel(BaseModel):
    model_config = ConfigDict(
        extra='allow'
    )
    _client: BaseBrivoClient | None = PrivateAttr()

    def attach_client(self, client: BaseBrivoClient) -> Self:
        """
        Attach the BrivoClient instance to the model.
        """
        self.__setattr__('_client', client)
        return self
