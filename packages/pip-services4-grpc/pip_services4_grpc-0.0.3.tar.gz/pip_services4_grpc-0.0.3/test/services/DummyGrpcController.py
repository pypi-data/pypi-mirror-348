# -*- coding: utf-8 -*-
from typing import Any, Callable

from grpc import ServicerContext
from pip_services4_commons.convert import TypeCode
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_data.query import FilterParams, PagingParams
from pip_services4_data.validate import ObjectSchema, PagingParamsSchema, FilterParamsSchema

from pip_services4_grpc.protos.commandable_pb2 import InvokeRequest
from pip_services4_grpc.controllers.GrpcController import GrpcController
from ..DummySchema import DummySchema
from ..IDummyService import IDummyService
from ..protos import dummies_pb2_grpc


class DummyGrpcController(GrpcController, dummies_pb2_grpc.DummiesServicer):
    __service: IDummyService = None
    __number_of_calls: int = 0

    def add_servicer_to_server(self, server):
        dummies_pb2_grpc.add_DummiesServicer_to_server(self, server)

    def __init__(self):
        self.service_name = 'dummies.Dummies.service'
        super().__init__(self.service_name)
        self._dependency_resolver.put('service',
                                      Descriptor('pip-services', 'service', 'default', '*', '*'))

    def set_references(self, references: IReferences):
        super().set_references(references)
        self.__service = self._dependency_resolver.get_one_required('service')

    def get_number_of_calls(self) -> int:
        return self.__number_of_calls

    def __increment_number_of_calls(self, request: InvokeRequest, context: ServicerContext,
                                    next: Callable[[InvokeRequest, ServicerContext], Any]) -> Any:
        self.__number_of_calls += 1
        return next(request, context)

    def __get_page_by_filter(self, request: InvokeRequest, context: ServicerContext) -> Any:
        filter = FilterParams()
        filter.update(request.filter)
        paging = PagingParams(request.paging.skip, request.paging.take, request.paging.total)

        return self.__service.get_page_by_filter(request.trace_id,
                                                 filter,
                                                 paging)

    def __get_one_by_id(self, request: InvokeRequest, context: ServicerContext):
        return self.__service.get_one_by_id(request.trace_id,
                                            request.dummy_id)

    def __create(self, request: InvokeRequest, context: ServicerContext):
        return self.__service.create(request.trace_id,
                                     request.dummy)

    def __update(self, request: InvokeRequest, context: ServicerContext):
        return self.__service.update(
            request.trace_id,
            request.dummy
        )

    def __delete_by_id(self, request: InvokeRequest, context: ServicerContext):
        return self.__service.delete_by_id(
            request.trace_id,
            request.dummy_id,
        ) or {}

    def register(self):
        self._register_interceptor(self.__increment_number_of_calls)

        self._register_method(
            'get_dummies',
            ObjectSchema(True)
            .with_optional_property("paging", PagingParamsSchema())
            .with_optional_property("filter", FilterParamsSchema()),
            self.__get_page_by_filter
        )

        self._register_method(
            'get_dummy_by_id',
            ObjectSchema(True)
            .with_required_property("dummy_id", TypeCode.String),
            self.__get_one_by_id
        )

        self._register_method(
            'create_dummy',
            ObjectSchema(True)
            .with_required_property("dummy", DummySchema()),
            self.__create
        )

        self._register_method(
            'update_dummy',
            ObjectSchema(True)
            .with_required_property("dummy", DummySchema()),
            self.__update
        )

        self._register_method(
            'delete_dummy_by_id',
            ObjectSchema(True)
            .with_required_property("dummy_id", TypeCode.String),
            self.__delete_by_id
        )
