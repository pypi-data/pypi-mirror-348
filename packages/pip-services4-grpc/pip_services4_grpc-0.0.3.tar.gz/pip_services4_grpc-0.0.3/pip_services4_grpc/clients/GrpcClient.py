# -*- coding: utf-8 -*-
from typing import Optional, Any

import grpc
from pip_services4_commons.errors import ConnectionException
from pip_services4_components.config import IConfigurable, ConfigParams
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_components.refer import IReferenceable, IReferences
from pip_services4_components.run import IOpenable
from pip_services4_http.connect import HttpConnectionResolver
from pip_services4_observability.count import CompositeCounters
from pip_services4_observability.log import CompositeLogger
from pip_services4_observability.trace import CompositeTracer
from pip_services4_rpc.trace import InstrumentTiming


class GrpcClient(IOpenable, IReferenceable, IConfigurable):
    """
    Abstract client that calls remove endpoints using GRPC protocol.

    ### Configuration parameters ###
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :func:`link`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - options:
          - retries:               number of retries (default: 3)
          - connect_timeout:       connection timeout in milliseconds (default: 10 sec)
          - timeout:               invocation timeout in milliseconds (default: 10 sec)

    .. code-block:: python

        class MyGrpcClient(GrpcClient, IMyClient):
            def __init__(self):
                super().__init__(my_data_pb2_grpc.MyDataStub, 'my_data_v1')
            ...
            def get_data(self, context, id ):
                timing = self.instrument(context, 'myclient.get_data')
                result = self._call("get_data", context, { id: id })
                timing.end_timing()
                return result
            ...

        client = MyGrpcClient()
        client.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))
        result = client.get_data(Context.from_trace_id("123"), "1")
    """

    _default_config = ConfigParams.from_tuples(
        "connection.protocol", "http",
        "connection.host", "0.0.0.0",
        "connection.port", 3000,

        "options.request_max_size", 1024 * 1024,
        "options.connect_timeout", 10000,
        "options.timeout", 10000,
        "options.retries", 3,
        "options.debug", True
    )

    def __init__(self, service_client: Any, client_name: str = None):
        """
        Creates a new instance of the client.

        :param service_client: service client class
        :param client_name: a client name.
        """
        self.__client = service_client
        self.__client_name = client_name

        # The GRPC client channel
        self._channel: grpc.Channel = None

        # The connection resolver.
        self._connection_resolver: HttpConnectionResolver = HttpConnectionResolver()

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()

        # The performance counters.
        self._counters: CompositeCounters = CompositeCounters()

        # The configuration options.
        self._options: ConfigParams = ConfigParams()

        # The connection timeout in milliseconds.
        self._connection_timeout: int = 100000

        # The invocation timeout in milliseconds.
        self._timeout: int = 100000

        # The remote service uri which is calculated on open.
        self._uri: str = None

        # The tracer.
        self._tracer: CompositeTracer = CompositeTracer()

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        config = config.set_defaults(GrpcClient._default_config)
        self._connection_resolver.configure(config)
        self._options = self._options.override(config.get_section('options'))

        self._connection_timeout = config.get_as_integer_with_default('options.connect_timeout',
                                                                      self._connection_timeout)
        self._timeout = config.get_as_integer_with_default('options.timeout', self._timeout)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._tracer.set_references(references)
        self._connection_resolver.set_references(references)

    def _instrument(self, context: Optional[IContext], name: str) -> InstrumentTiming:
        """
        Adds instrumentation to log calls and measure call time.
        It returns a CounterTiming object that is used to end the time measurement.

        :param context: (optional) transaction id to trace execution through call chain.
        :param name: a method name.
        :return: CounterTiming object to end the time measurement.
        """
        self._logger.trace(context, 'Executing {} method'.format(name))
        self._counters.increment_one(name + '.call_time')

        counter_timing = self._counters.begin_timing(name + ".call_time")
        tracer_timing = self._tracer.begin_trace(context, name, None)
        return InstrumentTiming(context, name, 'exec', self._logger,
                                self._counters, counter_timing, tracer_timing)

    # def _instrument_error(self, context: Optional[str], name: str, err: Exception, reerror=False):
    #     """
    #     Adds instrumentation to error handling.
    #
    #     :param context: (optional) transaction id to trace execution through call chain.
    #     :param name: a method name.
    #     :param err: an occured error
    #     :param reerror: if true - throw error
    #     """
    #     if err is not None:
    #         self._logger.error(context, err, 'Failed to call {} method'.format(name))
    #         self._counters.increment_one(name + '.call_errors')
    #         if reerror is not None and reerror is True:
    #             raise err

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: Returns true if the component has been opened and false otherwise.
        """
        return self._channel is not None

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self.is_open():
            return None

        try:
            connection = self._connection_resolver.resolve(context)
            self._uri = connection.get_as_string('uri')

            options = [('grpc.max_connection_idle_ms', self._connection_timeout),
                       ('grpc.client_idle_timeout_ms', self._timeout)]

            if connection.get_as_string_with_default('protocol', 'http') == 'https':
                ssl_ca_file = connection.get_as_nullable_string('ssl_ca_file')
                with open(ssl_ca_file, 'rb') as file:
                    trusted_root = file.read()
                credentials = grpc.ssl_channel_credentials(trusted_root)
                channel = grpc.secure_channel(str(connection.get_as_string('host')) + ':' +
                                              str(connection.get_as_string('port')), credentials=credentials,
                                              options=options)
            else:
                channel = grpc.insecure_channel(str(connection.get_as_string('host')) + ':' +
                                                str(connection.get_as_string('port')), options=options)

            self._channel = channel
            self.__client = self.__client(channel)

        except Exception as ex:
            raise ConnectionException(
                context, 'CANNOT_CONNECT', 'Opening GRPC client failed'
            ).wrap(ex).with_details('url', self._uri)

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._channel is not None:
            # Eat exceptions
            try:
                self._logger.debug(context, 'Closed GRPC service at {}'.format(self._uri))
            except Exception as ex:
                self._logger.warn(context, 'Failed while closing GRPC service: {}'.format(ex))
            # if self._client is not None:
            #     self._client = None
            self._channel.close()
            self._channel = None
            self._uri = None
            GrpcClient._connection_resolver = HttpConnectionResolver()

    def _call(self, method: str, context: Optional[IContext], request: Any) -> Any:
        """
        Calls a remote method via GRPC protocol.

        :param method: name of the calling method
        :param context: (optional) context execution through call chain.
        :param request: (optional) request object.
        :return: (optional) that receives result object or error.
        """
        if context and hasattr(request, 'context'):
            request.trace_id = ContextResolver.get_trace_id(context)

        return self.__client.__dict__[method](request)
