# -*- coding: utf-8 -*-

import grpc
from pip_services4_components.config import ConfigParams
from pip_services4_components.refer import References, Descriptor

from .DummyGrpcController import DummyGrpcController
from ..Dummy import Dummy
from ..DummyService import DummyService
from ..protos import dummies_pb2
from ..protos import dummies_pb2_grpc

port = 3000
grpc_config = ConfigParams.from_tuples(
    'connection.protocol',
    'http',
    'connection.host',
    'localhost',
    'connection.port',
    port
)

DUMMY1 = Dummy('', 'Key 1', 'Content 1')
DUMMY2 = Dummy('2', 'Key 2', 'Content 2')


class TestDummyGrpcController:
    references = None
    srv = None
    controller = None
    client = None
    chanel = None

    @classmethod
    def setup_class(cls):
        cls.srv = DummyService()

        cls.controller = DummyGrpcController()
        cls.controller.configure(grpc_config)

        cls.references = References.from_tuples(
            Descriptor('pip-services', 'service', 'default', 'default', '1.0'), cls.srv,
            Descriptor('pip-services', 'controller', 'grpc', 'default', '1.0'), cls.controller
        )

        cls.controller.set_references(cls.references)
        cls.controller.open(None)

        cls.chanel = grpc.insecure_channel('localhost:' + str(port))
        cls.client = dummies_pb2_grpc.DummiesStub(cls.chanel)

    @classmethod
    def teardown_class(cls, method=None):
        cls.chanel.close()
        cls.controller.close(None)

    def test_crud_operations(self):
        # Create one dummy
        request = dummies_pb2.DummyObjectRequest()

        request.dummy.id = DUMMY1.id
        request.dummy.key = DUMMY1.key
        request.dummy.content = DUMMY1.content

        dummy = self.client.create_dummy(request)

        assert dummy is not None
        assert dummy.content == DUMMY1.content
        assert dummy.key == DUMMY1.key

        # Create another dummy
        request = dummies_pb2.DummyObjectRequest()
        request.dummy.id = DUMMY2.id
        request.dummy.key = DUMMY2.key
        request.dummy.content = DUMMY2.content

        dummy = self.client.create_dummy(request)

        assert dummy is not None
        assert dummy.content == DUMMY2.content
        assert dummy.key == DUMMY2.key

        # Get all dummies
        request = dummies_pb2.DummiesPageRequest()
        dummies = self.client.get_dummies(request)

        assert dummies is not None
        assert len(dummies.data) == 2

        # Get dummy by id
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = DUMMY2.id

        dummy = self.client.get_dummy_by_id(request)

        assert dummy.id == DUMMY2.id
        assert dummy.key == DUMMY2.key
        assert dummy.content == DUMMY2.content

        # Update the dummy
        request = dummies_pb2.DummyObjectRequest()
        request.dummy.id = DUMMY2.id
        request.dummy.key = DUMMY2.key
        request.dummy.content = 'Updated Content 2'

        dummy = self.client.update_dummy(request)

        assert dummy is not None
        assert dummy.content == 'Updated Content 2'
        assert dummy.key == DUMMY2.key

        # Delete the dummy
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = DUMMY2.id
        dummy = self.client.delete_dummy_by_id(request)

        # Try to get deleted dummy
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = DUMMY2.id
        dummy = self.client.get_dummy_by_id(request)
        assert dummy.id is ''
        assert dummy.key is ''
        assert dummy.content is ''
