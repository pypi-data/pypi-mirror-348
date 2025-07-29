from typing import Any, Dict

from fakts_next.fakts import Fakts
from mikro_next.datalayer import DataLayer
from pydantic import BaseModel


class DataLayerFakt(BaseModel):
    endpoint_url: str


class FaktsDataLayer(DataLayer):
    """A fakts implementation of the datalayer. This will allow you to connect to a datalayer
    that is defined asnychronously in fakts. This is useful for connecting to a datalayer that
    is not known at compile time. Will get the server configuration from fakts and connect to the
    datalayer."""

    fakts_group: str
    fakts: Fakts

    _old_fakt: Dict[str, Any] = {}
    _configured = False

    def configure(self, fakt: DataLayerFakt) -> None:
        self.endpoint_url = fakt.endpoint_url

    async def get_endpoint_url(self):
        if self._configured:
            return self.endpoint_url
        else:
            await self.aconnect()
            return self.endpoint_url

    async def aconnect(self):
        fakt = await self.fakts.aget(self.fakts_group)
        self.configure(DataLayerFakt(**fakt))

        self._configured = True
