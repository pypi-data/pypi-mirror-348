# -*- coding: utf-8 -*-
from pip_services4_components.context import Context
from pip_services4_data.query import FilterParams, PagingParams

from .IDummyClient import IDummyClient
from ..Dummy import Dummy


class DummyClientFixture:
    __client = None

    def __init__(self, client):
        self.__client = client

    def test_crud_operations(self):
        DUMMY1 = Dummy('1', 'Key 1', 'Content 1')
        DUMMY2 = Dummy('', 'Key 2', 'Content 2')

        # Create one dummy
        dummy = self.__client.create_dummy(Context.from_trace_id('123'), DUMMY1)
        assert dummy is not None
        assert dummy.content == DUMMY1.content
        assert dummy.key == DUMMY1.key

        # Create another dummy
        dummy = self.__client.create_dummy(Context.from_trace_id('123'), DUMMY2)
        assert dummy is not None
        assert dummy.content == DUMMY2.content
        assert dummy.key == DUMMY2.key

        # Get all dummies
        dummies = self.__client.get_dummies(Context.from_trace_id('123'), FilterParams(), PagingParams(0, 5, False))
        assert dummies is not None
        assert len(dummies.data) == 2

        # Update the dummy
        dummy1 = DUMMY1
        dummy1.content = 'Updated Content 1'
        dummy = self.__client.update_dummy(Context.from_trace_id('123'), dummy1)
        assert dummy is not None
        assert dummy.key == dummy1.key
        assert dummy.content == dummy1.content

        # Delete dummy
        self.__client.delete_dummy(Context.from_trace_id('123'), dummy1.id)

        # Try to get delete dummy
        dummy = self.__client.get_dummy_by_id(Context.from_trace_id('123'), dummy1.id)
        assert dummy is None
