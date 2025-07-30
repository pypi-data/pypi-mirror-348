# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import List, Any, Optional, Callable

from grpc import ServicerContext
from pip_services4_commons.errors import InvalidStateException
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_components.refer import IReferenceable, IUnreferenceable, IReferences, DependencyResolver
from pip_services4_components.run import IOpenable
from pip_services4_data.query import FilterParams, PagingParams
from pip_services4_data.validate import Schema
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming

from pip_services4_grpc.protos.commandable_pb2 import InvokeRequest
from .GrpcEndpoint import GrpcEndpoint
from .IRegisterable import IRegisterable


class GrpcController(IOpenable, IConfigurable, IReferenceable, IUnreferenceable, IRegisterable):
    """
    Abstract controller that receives remove calls via GRPC protocol.

    ### Configuration parameters ###
        - dependencies:
          - endpoint:              override for GRPC Endpoint dependency
          - service:            override for Service dependency
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - credential - the HTTPS credentials:
          - ssl_key_file:         the SSL private key in PEM
          - ssl_crt_file:         the SSL certificate in PEM
          - ssl_ca_file:          the certificate authorities (root cerfiticates) in PEM


    .. code-block:: python

        class MyGrpcController(GrpcController, my_data_pb2_grpc.MyDataServicer):
            __service: IMyService
            ...
            def __init__(self):
                suoer().__init__('.. service name ...')
                self._dependency_resolver.put(
                    "controller",
                    Descriptor("mygroup","service","*","*","1.0")
                )

            def add_servicer_to_server(self, server):
                my_data_pb2_grpc.add_MyDataServicer_to_server(self, server)

            def set_references(self, references):
                super().set_references(references)
                self.__service = this._dependency_resolver.get_required("service")

            def __number_of_calls_interceptor(self, request: InvokeRequest, context: ServicerContext,
                                    next: Callable[[InvokeRequest, ServicerContext], Any]) -> Any:
                self.__number_of_calls += 1
                return next(request, context)

            def __method(request: InvokeRequest, context: ServicerContext):
                trace_id = request.trace_id
                id = request.id
                return self.__service.get_my_data(Context.from_trace_id(trace_id), id)

            def register(self):

                self._register_interceptor(self.__number_of_calls_interceptor)
                self._register_method("get_mydata", None, method)
                
                self._register_controller(self)
                ...



        controller = MyGrpcController()
        controller.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))

        controller.set_references(References.from_tuples(
           Descriptor("mygroup","service","default","default","1.0"), service
        ))

        controller.open(Context.from_trace_id("123"))

    """

    __default_config = ConfigParams.from_tuples("dependencies.endpoint", "*:endpoint:grpc:*:1.0")

    def __init__(self, service_name: str = None):
        """
        Creates a new instance of the service.

        :param service_name: a service name.
        """
        self.__config: ConfigParams = None
        self.__references: IReferences = None
        self.__local_endpoint: bool = None
        self.__implementation: Any = {}
        self.__interceptors: List[Any] = []
        self.__opened: bool = None

        # The GRPC endpoint that exposes this service.
        self._endpoint: GrpcEndpoint = None

        # The dependency resolver.
        self._dependency_resolver = DependencyResolver(GrpcController.__default_config)

        # The logger.
        self._logger = CompositeLogger()

        # The performance counters.
        self._counters = CompositeCounters()

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

        self.__service_name: str = service_name
        self.__registrable = lambda implementation: self.__register_controller(implementation)

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.
        :param config: configuration parameters to be set.
        """

        config = config.set_defaults(GrpcController.__default_config)
        self.__config = config
        self._dependency_resolver.configure(config)

    def set_references(self, references: IReferences):
        """
        Sets references to this endpoint's logger, counters, and connection resolver.
        
        ### References ###
            - logger: **"\*:logger:\*:\*:1.0"**
            - counters: **"\*:counters:\*:\*:1.0"**
            - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver)

        :param references: an IReferences object, containing references to a logger, counters, and a connection resolver.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._tracer.set_references(references)
        self._dependency_resolver.set_references(references)

        # Get endpoint
        self._endpoint = self._dependency_resolver.get_one_optional('endpoint')

        # Or create a local one
        if self._endpoint is None:
            self._endpoint = self.__create_endpoint()
            self.__local_endpoint = True
        else:
            self.__local_endpoint = False

        #  Add registration callback to the endpoint
        self._endpoint.register(self)  # TODO check this

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        # Remove registration callback from endpoint
        if self._endpoint is not None:
            self._endpoint.unregister(self)  # TODO check this
            self._endpoint = None

    def __create_endpoint(self) -> GrpcEndpoint:
        endpoint = GrpcEndpoint()

        if self.__config:
            endpoint.configure(self.__config)
        if self.__references:
            endpoint.set_references(self.__references)

        return endpoint

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: CounterTiming object to end the time measurement.
        """
        self._logger.trace(context, 'Executing {} method'.format(name))
        self._counters.increment_one(name + '.exec_time')

        counter_timing = self._counters.begin_timing(name + '.exec_time')
        trace_timing = self._tracer.begin_trace(context, name, None)
        return InstrumentTiming(context, name, 'exec', self._logger, self._counters, counter_timing,
                                trace_timing)

    def _instrument_error(self, context: Optional[IContext], name: str, err: Exception, reerror=False):
        """
        Adds instrumentation to error handling.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :param err: an occured error
        :param reerror: if true - throw error
        """
        if err is not None:
            self._logger.error(context, err, 'Failed to execute {} method'.format(name))
            self._counters.increment_one(name + '.exec_errors')

        if reerror:
            raise err

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self.__opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """

        if self.__opened:
            return None

        if self._endpoint is None:
            self._endpoint = self.__create_endpoint()
            self._endpoint.register(self)
            self.__local_endpoint = True

        if self.__local_endpoint:
            try:
                self._endpoint.open(context)
                self.__opened = True
            except Exception as ex:
                self.__opened = False
                raise ex
        else:
            self.__opened = True

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if not self.__opened:
            return None

        if self._endpoint is None:
            raise InvalidStateException(ContextResolver.get_trace_id(context), 'NO_ENDPOINT',
                                        'GRPC endpoint is missing')

        if self.__local_endpoint:
            self._endpoint.close(context)

        self.__opened = False

    def __register_controller(self, implementation: 'GrpcController'):
        # self.register()
        implementation.__dict__.update(self.__implementation)
        if self._endpoint is not None:
            self._endpoint.register_controller(implementation)

    def _apply_validation(self, schema: Schema, action: Callable[[InvokeRequest, ServicerContext], Any]) -> Callable[
        [InvokeRequest, ServicerContext], Any]:
        # Create an action function
        def action_wrapper(request: InvokeRequest, context: ServicerContext):
            # Validate object
            if schema and request:
                value = request
                if hasattr(value, 'to_object') and callable(value.to_object):
                    value = value.to_object()

                # Hack validation for filter and paging params
                validate_object = {}
                if hasattr(value, 'filter'):
                    validate_object['filter'] = FilterParams()
                    validate_object['filter'].update(value.filter)
                if hasattr(value, 'paging'):
                    validate_object['paging'] = PagingParams(value.paging.skip,
                                                             value.paging.take,
                                                             value.paging.total)
                if validate_object:
                    validate_object = type('ValidObject', (object,), validate_object)

                # Perform validation
                trace_id = value.trace_id
                schema.validate_and_throw_exception(trace_id, validate_object or value, False)

            return action(request, context)

        return action_wrapper

    def _apply_interceptors(self, action: Callable[[InvokeRequest, ServicerContext], Any]) -> Callable[
        [InvokeRequest, ServicerContext], Any]:
        action_wrapper = action

        for index in reversed(range(len(self.__interceptors))):
            interceptor = self.__interceptors[index]
            wrap = lambda action: lambda request, context: interceptor(request, context, action)
            action_wrapper = wrap(action_wrapper)

        return action_wrapper

    def _register_method(self, name: str, schema: Schema, action: Callable[[InvokeRequest, ServicerContext], Any]):
        """
        Registers a method in GRPC service.

        :param name: a method name
        :param schema: a validation schema to validate received parameters.
        :param action: an action function that is called when operation is invoked.
        """
        if self.__implementation is None: return

        action_wrapper = self._apply_validation(schema, action)
        action_wrapper = self._apply_interceptors(action_wrapper)

        # Assign method implementation
        self.__implementation[name] = lambda request, context: action_wrapper(request, context)

    def _register_method_with_auth(self, name: str, schema: Schema,
                                   authorize: Callable[[InvokeRequest, ServicerContext, Callable], Any],
                                   action: Callable[[InvokeRequest, ServicerContext, Callable], Any]):
        """
        Registers a method with authorization.

        :param name: a method name
        :param schema: a validation schema to validate received parameters.
        :param authorize: an authorization interceptor
        :param action: an action function that is called when operation is invoked.
        """

        action_wrapper = self._apply_validation(schema, action)
        # Add authorization just before validation
        action_wrapper = lambda request, context: authorize(request, context, action_wrapper)
        action_wrapper = self._apply_interceptors(action_wrapper)

        # Assign method implementation
        self.__implementation[name] = lambda request, context: action_wrapper(request, context)

    def _register_interceptor(self, action: Callable[[InvokeRequest, ServicerContext, Callable], Any]):
        """
        Registers a middleware for methods in GRPC endpoint.

        :param action: an action function that is called when middleware is invoked.
        """
        if self._endpoint is not None:
            self.__interceptors.append(lambda request, context, next: action(request, context, next))

    @abstractmethod
    def register(self):
        """
        Registers all service routes in Grpc endpoint.
        This method is called by the service and must be overriden
        in child classes.
        """
