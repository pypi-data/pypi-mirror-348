# -*- coding: utf-8 -*-

from abc import ABC
from typing import Optional

from pip_services4_components.context import IContext
from pip_services4_data.query import FilterParams, PagingParams, DataPage

from test.Dummy import Dummy


class IDummyClient(ABC):

    def get_dummies(self, context: Optional[IContext], filter: FilterParams, paging: PagingParams) -> DataPage:
        raise NotImplementedError

    def get_dummy_by_id(self, context: Optional[IContext], dummy_id: str) -> Dummy:
        raise NotImplementedError

    def create_dummy(self, context: Optional[IContext], dummy: Dummy) -> Dummy:
        raise NotImplementedError

    def update_dummy(self, context: Optional[IContext], dummy: Dummy) -> Dummy:
        raise NotImplementedError

    def delete_dummy(self, context: Optional[IContext], dummy_id: str) -> Dummy:
        raise NotImplementedError
