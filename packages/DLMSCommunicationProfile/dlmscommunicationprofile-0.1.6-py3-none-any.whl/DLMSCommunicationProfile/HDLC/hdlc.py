"""DLMS UA 1000-2 Ed. 10"""
from dataclasses import dataclass, field
from DLMS_SPODES.types.implementations import enums
from ..base import CommunicationProfile, Parameters
from .. import limit
from .negotiation import Negotiation
from ..osi import OSI


window_size_values = limit.MinMax(
    name="window size",
    min=1,
    max=7
)
info_field_length_values = limit.MinMax(
    name="info field length",
    min=32,
    max=2030
)


@dataclass
class HDLCParameters(Parameters):
    """8.4 Protocol specification for the MAC sublayer"""
    comm_speed: int = 9600
    window_size_transmit: int = 1
    window_size_receive: int = 1
    max_info_field_length_transmit: int = 128
    max_info_field_length_receive: int = 128
    inter_octet_time_out: int = 25
    inactivity_time_out: int = 120
    device_address: int | None = 0x10
    """physical address from HDLC setup, lower address in HDLC frame"""

    def validate(self):
        """RuntimeError :raise if not valid"""
        x = enums.CommSpeed(self.comm_speed)
        window_size_values.validate(self.window_size_transmit)
        window_size_values.validate(self.window_size_receive)
        info_field_length_values.validate(self.max_info_field_length_transmit)
        info_field_length_values.validate(self.max_info_field_length_receive)


@dataclass
class HDLC(CommunicationProfile):
    """10.2 The 3-layer, connection-oriented, HDLC based communication profile"""
    parameters: HDLCParameters = field(default_factory=HDLCParameters)
    negotiation: Negotiation = field(init=False)  # todo: temporary need refactoring

    def __post_init__(self):
        self.negotiation = Negotiation(
            max_info_receive=self.parameters.max_info_field_length_receive,
            max_info_transmit=self.parameters.max_info_field_length_transmit,
            window_receive=self.parameters.window_size_receive,
            window_transmit=self.parameters.window_size_transmit
        )

    # async def connect(self, from_: OSI = OSI.NONE, to_: OSI = OSI.APPLICATION):
    #     pass
    #
    # async def physical(self, c: Client):
    #     if OSI.PHYSICAL not in c.level:
    #         if not c.media.is_open():
    #             await c.media.open()
    #         c.level = OSI.PHYSICAL
    #         c.set_error(Transmit.OK, "Open port")
    #         c.log(logL.INFO, F"Open port communication channel: {c.media}")
    #         # todo: replace to <data_link>
    #         if (
    #             c.objects is None
    #             and not isinstance(self, InitType)
    #         ):
    #             await init_type.data_link(c)
    #             await c.close()  # todo: change to DiscRequest, or make not closed
    #         ret = await self.data_link(c)
    #         await c.close()  # todo: change to DiscRequest
    #         return ret
    #
    # async def disconnect(self, from_: OSI = OSI.APPLICATION, to_: OSI = OSI.NONE):
    #     pass
