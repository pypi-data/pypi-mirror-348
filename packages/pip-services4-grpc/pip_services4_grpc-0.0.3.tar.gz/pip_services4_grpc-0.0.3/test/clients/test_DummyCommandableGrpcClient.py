# -*- coding: utf-8 -*-
from pip_services4_components.config import ConfigParams
from pip_services4_components.refer import References, Descriptor

from .DummyClientFixture import DummyClientFixture
from .DummyCommandableGrpcClient import DummyCommandableGrpcClient
from ..DummyService import DummyService
from ..services.DummyCommandableGrpcController import DummyCommandableGrpcController

grpc_config = ConfigParams.from_tuples(
    'connection.protocol',
    'http',
    'connection.host',
    'localhost',
    'connection.port',
    3002
)


class TestDummyCommandableGrpcClient:
    controller = None
    client = None
    fixture = None

    @classmethod
    def setup_class(cls):
        srv = DummyService()

        cls.controller = DummyCommandableGrpcController()
        cls.controller.configure(grpc_config)

        references = References.from_tuples(
            Descriptor(
                'pip-services', 'service', 'default', 'default', '1.0'),
            srv,
            Descriptor('pip-services', 'controller', 'grpc', 'default', '1.0'),
            cls.controller
        )

        cls.controller.set_references(references)
        cls.controller.open(None)

    @classmethod
    def teardown_class(cls):
        cls.controller.close(None)

    def setup_method(self, method=None):
        self.client = DummyCommandableGrpcClient()
        self.fixture = DummyClientFixture(self.client)

        self.client.configure(grpc_config)
        self.client.set_references(References())
        self.client.open(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
