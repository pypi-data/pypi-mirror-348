# -*- coding: utf-8 -*-

from concurrent import futures
from typing import Any, List, Optional, Callable

import grpc
from pip_services4_commons.errors import ConnectionException, InvocationException, ErrorDescriptionFactory
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.refer import IReferenceable, IReferences
from pip_services4_components.run import IOpenable
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_data.validate import Schema
from pip_services4_http.connect import HttpConnectionResolver
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger

import pip_services4_grpc.protos.commandable_pb2 as commandable_pb2
import pip_services4_grpc.protos.commandable_pb2_grpc as commandable_pb2_grpc
from pip_services4_grpc.controllers.IRegisterable import IRegisterable


class _CommandableMediator(commandable_pb2_grpc.CommandableServicer):
    def add_servicer_to_server(self, server):
        commandable_pb2_grpc.add_CommandableServicer_to_server(self, server)

    def __init__(self):
        self.__invoke = None

    def invoke(self, request: commandable_pb2.InvokeRequest, context: grpc.ServicerContext):
        if self.__invoke is not None:
            return self.__invoke(request, context)

        return None

    # Sets invoke function
    def invoke_func(self, fn):
        self.__invoke = fn


class GrpcEndpoint(IOpenable, IConfigurable, IReferenceable):
    """
    Used for creating GRPC endpoints. An endpoint is a URL, at which a given service can be accessed by a client.

    ### Configuration parameters ###

    Parameters to pass to the :func:`configure` method for component configuration:

        - connection(s) - the connection resolver's connections:
            - "connection.discovery_key" - the key to use for connection resolving in a discovery service;
            - "connection.protocol" - the connection's protocol;
            - "connection.host" - the target host;
            - "connection.port" - the target port;
            - "connection.uri" - the target URI.
        - credential - the HTTPS credentials:
            - "credential.ssl_key_file" - the SSL private key in PEM
            - "credential.ssl_crt_file" - the SSL certificate in PEM
            - "credential.ssl_ca_file" - the certificate authorities (root cerfiticates) in PEM

    ### References ###
    
    A logger, counters, and a connection resolver can be referenced by passing the
    following references to the object's :func:`set_references` method:

        - logger: **\*:logger:\*:\*:1.0"**;
        - counters: **"\*:counters:\*:\*:1.0"**;
        - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver).

    .. code-block:: python

        def my_method(self, _config, _references):
            endpoint = GrpcEndpoint()
            if self._config:
                endpoint.configure(self._config)
            if self._references:
                endpoint.set_references(self._references)
            ...

            self._endpoint.open(context)
            ...


    """

    __defaultConfig = ConfigParams.from_tuples(
        "connection.protocol", "http",
        "connection.host", "0.0.0.0",
        "connection.port", 3000,

        "credential.ssl_key_file", None,
        "credential.ssl_crt_file", None,
        "credential.ssl_ca_file", None,

        "options.maintenance_enabled", None,
        "options.request_max_size", 1024 * 1024,
        "options.file_max_size", 200 * 1024 * 1024,
        "options.connect_timeout", 60000,
        "options.debug", True
    )

    def __init__(self):
        self.__server: Any = None
        self.__connection_resolver = HttpConnectionResolver()
        self.__logger = CompositeLogger()
        self.__counters = CompositeCounters()
        self.__maintenance_enabled = False
        self.__file_max_size = 200 * 1024 * 1024
        self.__uri: str = None
        self.__registrations: List[IRegisterable] = []
        self.__commandable_methods: Any = None
        self.__commandable_schemas: Any = None
        self.__commandable_service: Any = None

    def configure(self, config: ConfigParams):
        """
        Configures this HttpEndpoint using the given configuration parameters.
        
        ### Configuration parameters ###
            - connection(s) - the connection resolver's connections;
            - "connection.discovery_key" - the key to use for connection resolving in a dis
            - "connection.protocol" - the connection's protocol;
            - "connection.host" - the target host;
            - "connection.port" - the target port;
            - "connection.uri" - the target URI.
            - "credential.ssl_key_file" - SSL private key in PEM
            - "credential.ssl_crt_file" - SSL certificate in PEM
            - "credential.ssl_ca_file" - Certificate authority (root certificate) in PEM

        :param config: configuration parameters, containing a "connection(s)" section.
        """
        config = config.set_defaults(GrpcEndpoint.__defaultConfig)
        self.__connection_resolver.configure(config)

        self.__maintenance_enabled = config.get_as_boolean_with_default('options.maintenance_enabled',
                                                                        self.__maintenance_enabled)
        self.__file_max_size = ConfigParams().get_as_long_with_default(key='options.file_max_size',
                                                                       default_value=self.__file_max_size)

    def set_references(self, references: IReferences):
        """
        Sets references to this endpoint's logger, counters, and connection resolver.

        __References:__
        - logger: **"\*:logger:\*:\*:1.0"**
        - counters: **"\*:counters:\*:\*:1.0"**
        - discovery: **"\*:discovery:\*:\*:1.0"** (for the connection resolver)

        :param references: an IReferences object, containing references to a logger, counters, and a connection resolver.
        """
        self.__logger.set_references(references)
        self.__counters.set_references(references)
        self.__connection_resolver.set_references(references)

    def is_open(self) -> bool:
        """
        :return: whether or not this endpoint is open with an actively listening GRPC server.
        """
        return self.__server is not None

    def open(self, context: Optional[IContext]):
        """
        Opens a connection using the parameters resolved by the referenced connection
        resolver and creates a GRPC server (service) using the set options and parameters.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return

        connection = self.__connection_resolver.resolve(context)
        self.__uri = connection.get_as_string('uri')
        try:
            self.__connection_resolver.register(context)

            credentials = None

            if connection.get_as_string_with_default('protocol', 'http') == 'https':
                ssl_key_file = connection.get_as_nullable_string('ssl_key_file')
                ssl_crt_file = connection.get_as_nullable_string('ssl_crt_file')

                with open(ssl_key_file, 'rb') as file:
                    private_key = file.read()

                with open(ssl_crt_file, 'rb') as file:
                    certificate = file.read()

                ca = None
                ssl_ca_file = connection.get_as_nullable_string('ssl_ca_file')
                if ssl_ca_file is not None:
                    with open(ssl_ca_file, 'rb') as file:
                        ca_text = file.read()
                    while ca_text and len(ca_text.strip()) > 0:
                        crt_index = ca_text.rfind(b'-----BEGIN CERTIFICATE-----')
                        if crt_index > -1:
                            ca = ca_text[crt_index:]
                            ca_text = ca_text[:crt_index]

                credentials = grpc.ssl_server_credentials(((private_key, certificate),), root_certificates=ca)

            # Create instance of express application
            self.__server = grpc.server(futures.ThreadPoolExecutor())

            if credentials:
                self.__server.add_secure_port(str(connection.get_as_string('host')) + ':' +
                                              str(connection.get_as_string('port')), credentials)
            else:
                self.__server.add_insecure_port(
                    str(connection.get_as_string('host')) + ':' + str(connection.get_as_string('port')))

            self.__connection_resolver.register(context)
            self.__logger.debug(context, 'Opened GRPC service at {}'.format(self.__uri))

            # Start operations
            self.__perform_registrations()
            self.__server.start()

        except Exception as ex:
            self.__server = None
            raise ConnectionException(ContextResolver.get_trace_id(context), 'CANNOT_CONNECT',
                                      'Opening GRPC service failed').wrap(
                ex).with_details('url', self.__uri)

    def close(self, context: Optional[IContext]):
        """
        Closes this endpoint and the GRPC server (service) that was opened earlier.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.__server is not None:
            self.__uri = None
            self.__commandable_methods = None
            self.__commandable_schemas = None
            self.__commandable_service = None

            # Eat exceptions
            try:
                self.__server.stop(None)
                self.__logger.debug(context, 'Closed GRPC service at {}'.format(self.__uri))
                self.__server = None
                self.__registrations = []
                self.__connection_resolver = HttpConnectionResolver()
            except Exception as ex:
                self.__logger.warn(context, 'Failed while closing GRPC service: '.format(ex))

    def register(self, registration: IRegisterable):
        """
        Registers a registerable object for dynamic endpoint discovery.

        :param registration: the registration to add.
        """
        if registration is not None:
            self.__registrations.append(registration)

    def unregister(self, registration: IRegisterable):
        """
        Unregisters a registerable object, so that it is no longer used in dynamic
        endpoint discovery.

        :param registration: the registration to remove.
        """
        self.__registrations = list(filter(lambda r: r == registration, self.__registrations))

    def __perform_registrations(self):
        for registration in self.__registrations:
            registration.register()

            # hack for register generated controllers
            if hasattr(registration, '_GrpcController__register_controller') and hasattr(registration,
                                                                                   'add_servicer_to_server'):
                registration._GrpcController__register_controller(registration)

        self.__register_commandable_controller()

    def __register_commandable_controller(self):
        if self.__commandable_methods is None:
            return
        self.__commandable_service = _CommandableMediator()
        self.__commandable_service.invoke_func(self.__invoke_commandable_method)

        self.register_controller(self.__commandable_service)

    def __invoke_commandable_method(self, request: commandable_pb2.InvokeRequest, context: grpc.ServicerContext):
        method = request.method
        action = None if not self.__commandable_methods else self.__commandable_methods[method]
        trace_id = request.trace_id
        response = commandable_pb2.InvokeReply()

        # Handle method not found
        if action is None:
            err = InvocationException(trace_id, 'METHOD_NOT_FOUND',
                                      'Method ' + method + ' was not found').with_details('method', method)

            resp_err = ErrorDescriptionFactory.create(err)
            response.error.category = resp_err.category or ''
            response.error.code = resp_err.code or ''
            response.error.trace_id = resp_err.trace_id or ''
            response.error.status = resp_err.status or 0
            response.error.message = resp_err.message or ''
            response.error.cause = resp_err.cause or ''
            response.error.stack_trace = resp_err.stack_trace or ''
            response.error.details.update(resp_err.details or {})
            response.result_empty = True
            response.result_json = ''

            return response

        return action(request, context)

    def register_controller(self, service: Any):
        """
        Registers a controller with related implementation

        :param service: a GRPC controller object.
        """
        service.add_servicer_to_server(self.__server)

    def _register_commandable_method(self, method: str, schema: Schema,
                                     action: Callable[[Optional[IContext], Any], Any]):
        """
        Registers a commandable method in this objects GRPC server (service) by the given name.

        :param method: the GRPC method name.
        :param schema: the schema to use for parameter validation.
        :param action: the action to perform at the given route.
        """
        self.__commandable_methods = self.__commandable_methods or {}
        self.__commandable_methods[method] = action

        self.__commandable_schemas = self.__commandable_schemas or {}
        self.__commandable_schemas[method] = schema
