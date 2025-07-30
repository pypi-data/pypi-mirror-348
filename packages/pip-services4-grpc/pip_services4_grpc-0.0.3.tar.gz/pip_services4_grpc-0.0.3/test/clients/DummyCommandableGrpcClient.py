# -*- coding: utf-8 -*-

from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from pip_services4_grpc.clients.CommandableGrpcClient import CommandableGrpcClient
from .IDummyClient import IDummyClient
from ..Dummy import Dummy


class DummyCommandableGrpcClient(CommandableGrpcClient, IDummyClient):

    def __init__(self):
        super().__init__('dummy')

    def get_dummies(self, context: Optional[IContext], filter: FilterParams, paging: PagingParams) -> DataPage:
        return self.call_command('get_dummies', context, {'filter': filter, 'paging': paging})

    def get_dummy_by_id(self, context: Optional[IContext], dummy_id) -> Dummy:
        return self.call_command('get_dummy_by_id', context, {'dummy_id': dummy_id})

    def create_dummy(self, context: Optional[IContext], dummy) -> Dummy:
        return self.call_command('create_dummy', context, {'dummy': dummy})

    def update_dummy(self, context: Optional[IContext], dummy) -> Dummy:
        return self.call_command('update_dummy', context, {'dummy': dummy})

    def delete_dummy(self, context: Optional[IContext], dummy_id: str) -> Dummy:
        return self.call_command('delete_dummy', context, {'dummy_id': dummy_id})
