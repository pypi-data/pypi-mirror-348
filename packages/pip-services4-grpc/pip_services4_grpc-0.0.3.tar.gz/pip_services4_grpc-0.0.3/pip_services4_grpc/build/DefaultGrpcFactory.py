# -*- coding: utf-8 -*-

from pip_services4_components.build.Factory import Factory
from pip_services4_components.refer import Descriptor

from ..controllers.GrpcEndpoint import GrpcEndpoint


class DefaultGrpcFactory(Factory):
    """
    Creates GRPC components by their descriptors.

    See :class:`Factory <pip_services4_components.build.Factory.Factory>`, :class:`GrpcEndpoint <pip_services4_grpc.controllers.GrpcEndpoint.GrpcEndpoint>`, :class:`HeartbeatGrpcController <pip_services4_grpc.controllers.HeartbeatGrpcController.HeartbeatGrpcController>`, :class:`StatusGrpcController <pip_services4_grpc.controllers.StatusGrpcController.StatusGrpcController>`
    """
    GrpcEndpointDescriptor = Descriptor("pip-services", "endpoint", "grpc", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultGrpcFactory.GrpcEndpointDescriptor, GrpcEndpoint)
