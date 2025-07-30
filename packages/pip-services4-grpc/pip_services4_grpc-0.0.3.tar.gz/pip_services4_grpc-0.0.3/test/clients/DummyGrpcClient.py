# -*- coding: utf-8 -*-

from typing import Optional

from pip_services4_components.context import IContext, ContextResolver
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from pip_services4_grpc.clients.GrpcClient import GrpcClient
from .IDummyClient import IDummyClient
from ..Dummy import Dummy
from ..protos import dummies_pb2
from ..protos import dummies_pb2_grpc


class DummyGrpcClient(GrpcClient, IDummyClient):

    def __init__(self):
        super().__init__(dummies_pb2_grpc.DummiesStub, 'dummies.Dummies')

    def get_dummies(self, context: Optional[IContext], filter: FilterParams, paging: PagingParams) -> DataPage:
        request = dummies_pb2.DummiesPageRequest()
        request.trace_id = ContextResolver.get_trace_id(context)

        if filter is not None:
            request.filter.update(filter)

        if paging is not None:
            request.paging.total = paging.total
            request.paging.skip += paging.skip
            request.paging.take = paging.take

        self._instrument(context, 'dummy.get_page_by_filter')
        response = self._call('get_dummies', context, request)
        items = []
        for item in response.data:
            items.append(item)

        return DataPage(items, int(response.total))

    def get_dummy_by_id(self, context: Optional[IContext], dummy_id: str) -> Optional[Dummy]:
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = dummy_id

        self._instrument(context, 'dummy.get_one_by_id')
        response = self._call('get_dummy_by_id', context, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response

    def create_dummy(self, context: Optional[IContext], dummy: Dummy) -> Optional[Dummy]:
        request = dummies_pb2.DummyObjectRequest()
        request.trace_id = ContextResolver.get_trace_id(context)

        request.dummy.id = dummy.id
        request.dummy.key = dummy.key
        request.dummy.content = dummy.content

        self._instrument(context, 'dummy.create')

        response = self._call('create_dummy', context, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response

    def update_dummy(self, context: Optional[IContext], dummy: Dummy) -> Optional[Dummy]:
        request = dummies_pb2.DummyObjectRequest()
        request.trace_id = ContextResolver.get_trace_id(context)

        request.dummy.id = dummy.id
        request.dummy.key = dummy.key
        request.dummy.content = dummy.content

        self._instrument(context, 'dummy.update')

        response = self._call('update_dummy', context, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response

    def delete_dummy(self, context: Optional[IContext], dummy_id: str) -> Optional[Dummy]:
        request = dummies_pb2.DummyIdRequest()
        request.dummy_id = dummy_id

        self._instrument(context, 'dummy.delete')

        response = self._call('delete_dummy_by_id', context, request)

        if response is not None and response.id == '' and response.key == '':
            response = None

        return response
