# -*- coding: utf-8 -*-
from abc import ABC
from typing import List, Callable, Optional, Any

from grpc import ServicerContext
from pip_services4_commons.convert import JsonConverter
from pip_services4_commons.errors import InvocationException, ErrorDescriptionFactory
from pip_services4_components.context import IContext
from pip_services4_data.validate import Schema
from pip_services4_rpc.commands import CommandSet, ICommand
from pip_services4_components.exec import Parameters

from pip_services4_grpc.protos import commandable_pb2
from pip_services4_grpc.protos.commandable_pb2 import InvokeReply, InvokeRequest
from .GrpcController import GrpcController


class CommandableGrpcController(GrpcController, ABC):
    """
    Abstract service that receives commands via GRPC protocol
    to operations automatically generated for commands defined in :class:`ICommandable <pip_services4_rpc.commands.ICommandable.ICommandable>`.
    Each command is exposed as invoke method that receives command name and parameters.

    Commandable controllers require only 3 lines of code to implement a robust external
    GRPC-based remote interface.

     ### Configuration parameters ###
    - dependencies:
        - endpoint:              override for HTTP Endpoint dependency
        - service:            override for Service dependency
    - connection(s):
        - discovery_key:         (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>`
        - protocol:              connection protocol: http or https
        - host:                  host name or IP address
        - port:                  port number
        - uri:                   resource URI or connection string with all parameters in it

        ### References ###
        - `*:logger:*:*:1.0`           (optional) :class:`ILogger <pip_services4_observability.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`         (optional) :class:`ICounters <pip_services4_observability.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`        (optional) :class:`IDiscovery <pip_services4_config.connect.IDiscovery.IDiscovery>` controllers to resolve connection
        - `*:endpoint:grpc:*:1.0`      (optional) :class:`GrpcEndpoint <pip_services4_grpc.controllers.GrpcEndpoint.GrpcEndpoint` reference

    See :class:`CommandableGrpcClient <pip_services4_grpc.clients.CommandableGrpcClient.CommandableGrpcClient`,
    :class:`GrpcController <pip_services4_grpc.controllers.GrpcController.GrpcController`

    .. code-block:: python

        class MyCommandableGrpcController(CommandableGrpcController):
           def __init__(self):
              super().__init__('service name')

              self._dependency_resolver.put(
                    "service",
                    Descriptor("mygroup","service","*","*","1.0")
              )

        controller = MyCommandableGrpcController()
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

    def __init__(self, name: str):
        """
        Creates a new instance of the service.

        :param name: a service name.
        """
        super().__init__(None)
        self.__name = name
        self.__command_set: CommandSet = None
        self._dependency_resolver.put('controller', 'none')

    def __apply_command(self, schema: Schema,
                        action: Callable[[Optional[str], Any], Any]) -> Callable[[InvokeRequest, ServicerContext], Any]:

        def action_wrapper(request: InvokeRequest, context: ServicerContext) -> InvokeReply:
            method = request.method
            trace_id = request.trace_id
            response = commandable_pb2.InvokeReply()

            try:
                # Convert arguments
                args_empty = request.args_empty
                args_json = request.args_json
                args = Parameters.from_json(args_json) if not args_empty and args_json else Parameters()

                # Call command action
                try:
                    result = action(trace_id, args)
                    response.result_empty = result is None
                    response.result_json = JsonConverter.to_json(result) or ''

                    # TODO: Validate schema
                    if schema:
                        pass

                    return response

                except Exception as ex:
                    # Process result and generate response
                    response = self.__set_error_response(response, ex)
                    return response

            except Exception as ex:
                # Handle unexpected exception
                err = InvocationException(trace_id, 'METHOD_FAILED', 'Method ' + method + ' failed').wrap(
                    ex).with_details('method', method)

                response = self.__set_error_response(response, err)
                return response

        return action_wrapper

    def __set_error_response(self, response: InvokeReply, error: Exception):
        resp_err = ErrorDescriptionFactory.create(error)
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

    def _register_commandable_method(self, method: str, schema: Optional[Schema],
                                     action: Callable[[Optional[IContext], Any], Any]):
        """
        Registers a commandable method in this objects GRPC server (service) by the given name.

        :param method: the GRPC method name.
        :param schema: the schema to use for parameter validation.
        :param action: the action to perform at the given route.
        """
        action_wrapper = self.__apply_command(schema, action)
        action_wrapper = self._apply_interceptors(action_wrapper)

        self._endpoint._register_commandable_method(method, schema, action_wrapper)

    def register(self):
        """
        Registers all controller routes in gRPC endpoint.
        Call automaticaly in open component procedure

        """
        service = self._dependency_resolver.get_one_required('service')
        self.__command_set = service.get_command_set()

        commands: List[ICommand] = self.__command_set.get_commands()

        for index in range(len(commands)):
            command = commands[index]
            method = '' + self.__name + '.' + command.get_name()

            def context_wrap(command, method):
                def inner(context, args):
                    timing = self._instrument(context, method)
                    try:
                        return command.execute(context, args)
                    except Exception as e:
                        timing.end_failure(e)
                        raise e
                    finally:
                        timing.end_timing()

                return inner

            self._register_commandable_method(method, None, context_wrap(command, method))
