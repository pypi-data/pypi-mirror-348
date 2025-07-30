# -*- coding: utf-8 -*-
from pip_services4_components.config import ConfigParams
from pip_services4_components.refer import References, Descriptor

from ..DummyService import DummyService
from ..services.DummyGrpcController import DummyGrpcController
from .DummyGrpcClient import DummyGrpcClient
from .DummyClientFixture import DummyClientFixture

grpc_config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost",
    "connection.port", 3000
)


class TestDummyGrpcClient:
    controller = None
    client = None
    fixture = None

    @classmethod
    def setup_class(cls):
        srv = DummyService()

        cls.controller = DummyGrpcController()
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
        self.client = DummyGrpcClient()
        self.fixture = DummyClientFixture(self.client)

        self.client.configure(grpc_config)
        self.client.set_references(References())
        self.client.open(None)

    def teardown_method(self, method=None):
        self.client.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
