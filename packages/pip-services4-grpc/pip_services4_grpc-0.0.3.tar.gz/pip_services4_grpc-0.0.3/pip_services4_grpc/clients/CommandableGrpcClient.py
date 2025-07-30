# -*- coding: utf-8 -*-

import json
from typing import Any, Optional

from pip_services4_commons.errors.ApplicationExceptionFactory import ApplicationExceptionFactory
from pip_services4_components.context import IContext, ContextResolver
from pip_services4_data.query import DataPage

from .GrpcClient import GrpcClient
from ..protos import commandable_pb2
from ..protos import commandable_pb2_grpc


class CommandableGrpcClient(GrpcClient):
    """
    Abstract client that calls commandable GRPC service.

    Commandable controllers are generated automatically for :class:`ICommandable <pip_services4_rpc.commands.ICommandable.ICommandable>`.
    Each command is exposed as Invoke method that receives all parameters as args.

    ### Configuration parameters ###
        - connection(s):
          - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>`
          - protocol:              connection protocol: http or https
          - host:                  host name or IP address
          - port:                  port number
          - uri:                   resource URI or connection string with all parameters in it
        - options:
          - retries:               number of retries (default: 3)
          - connect_timeout:       connection timeout in milliseconds (default: 10 sec)
          - timeout:               invocation timeout in milliseconds (default: 10 sec)

    ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_observability.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services4_observability.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>` controllers to resolve connection

    .. code-block:: python

        class MyCommandableGrpcClient(CommandableGrpcClient, IMyClient):
            def __init__(self):
                super().__init__('my_data')
            ...
            def get_data(self, context, id):

                return self.call_command(
                            "get_data",
                            context,
                            { 'id': id }
                        )

        client = new MyCommandableGrpcClient()
        client.configure(ConfigParams.from_tuples(
            "connection.protocol", "http",
            "connection.host", "localhost",
            "connection.port", 8080
        ))
        result = client.get_data(Context.from_trace_id("123"), "1")

    """

    def __init__(self, name: str):
        """
        Creates a new instance of the client.

        :param name: a service name.
        """
        super().__init__(commandable_pb2_grpc.CommandableStub, 'commandable.Commandable')
        # The service name
        self._name = name
        # Instance of client

    def call_command(self, name: str, context: Optional[IContext], params: dict) -> Any:
        """
        Calls a remote method via GRPC commadable protocol.
        The call is made via Invoke method and all parameters are sent in args object.
        The complete route to remote method is defined as serviceName + '.' + name.

        :param name: a name of the command to call.
        :param context: (optional) context execution through call chain.
        :param params: command parameters.
        :return: Future that receives result
        """

        method = self._name + '.' + name
        timing = self._instrument(context, method)

        request = commandable_pb2.InvokeRequest()

        request.method = method
        request.trace_id = ContextResolver.get_trace_id(context)
        request.args_empty = params is None

        for key in params.keys():
            if hasattr(params[key], '__dict__'):
                params.update({key: params[key].__dict__})

        request.args_json = json.dumps(params) if params is not None else ''

        try:
            response = self._call('invoke', context, request)

            # Handle error response
            if response.error and response.error.code != '':
                raise ApplicationExceptionFactory.create(response.error)

            # Handle empty response
            if response.result_empty or response.result_empty == '' or response.result_empty is None:
                return None

            # Handle regular response
            json_response: dict = json.loads(response.result_json)

            if json_response.get('data'):
                page = DataPage(data=[], total=int(json_response.get('total')))

                for item in json_response['data']:
                    page.data.append(type('object', (object,), item))

                return page

            plain_object = type('object', (object,), json_response)
            return plain_object

        except Exception as ex:
            timing.end_failure(ex)
            raise ex
        finally:
            timing.end_success()
