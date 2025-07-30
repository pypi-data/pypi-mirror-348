# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor

from pip_services4_grpc.controllers.CommandableGrpcController import CommandableGrpcController


class DummyCommandableGrpcController(CommandableGrpcController):

    def __init__(self):
        super().__init__('dummy')
        self._dependency_resolver.put('service', Descriptor('pip-services', 'service', '*', '*', '*'))
