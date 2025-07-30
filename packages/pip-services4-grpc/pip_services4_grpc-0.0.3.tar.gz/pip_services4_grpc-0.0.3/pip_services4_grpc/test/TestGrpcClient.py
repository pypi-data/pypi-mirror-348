# -*- coding: utf-8 -*-

from typing import Any

from pip_services4_grpc.clients.GrpcClient import GrpcClient


class TestGrpcClient(GrpcClient):
    """
    GRPC client used for automated testing.
    """

    def __init__(self, client_name: str):
        super().__init__(client_name)

    def _call(self, method: str, client: Any, request: Any) -> Any:
        """
        Calls a remote method via GRPC protocol.

        :param method: a method name to called
        :param client: current client
        :param request: (optional) request object.
        :return: the received result.
        """
        return super(TestGrpcClient, self)._call(method, client, request)
