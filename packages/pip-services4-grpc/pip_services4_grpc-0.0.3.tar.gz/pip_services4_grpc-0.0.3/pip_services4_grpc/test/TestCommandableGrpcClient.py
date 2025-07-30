# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services4_grpc.clients.CommandableGrpcClient import CommandableGrpcClient


class TestCommandableGrpcClient(CommandableGrpcClient):
    """
    Creates a new instance of the client.
    """

    def __init__(self, name: str):
        """
        Creates a new instance of the client.

        :param name: a service name.
        """
        super().__init__(name)

    def call_command(self, name: str, context: Optional[str], params: dict) -> Any:
        """
        Calls a remote method via GRPC commadable protocol.
        The call is made via Invoke method and all parameters are sent in args object.
        The complete route to remote method is defined as serviceName + "." + name.

        :param name: a name of the command to call.
        :param context: (optional) transaction id to trace execution through call chain.
        :param params: command parameters.
        :return: the received result.
        """
        return super().call_command(name, context, params)
