from typing import Annotated

from annotated_types import Gt
from pydantic import BaseModel, Field

_POSITIVE_INT = Annotated[int, Gt(0)]


class BcpOptions(BaseModel):
    batch_size: _POSITIVE_INT | None = Field(default=None,
                                             description="The number of rows per batch of downloaded data")
    packet_size: _POSITIVE_INT | None = Field(
        default=None,
        description="the number of bytes, per network packet, sent to and from the server"
    )

    @property
    def command_options(self) -> dict[str, str | None]:
        command_options: dict[str, str] = {}
        if self.batch_size is not None:
            command_options["-b"] = str(self.batch_size)
        if self.packet_size is not None:
            command_options["-a"] = str(self.packet_size)
        return command_options
