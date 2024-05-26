from concurrent import futures
import random
import json

import grpc

from users_pb2 import (
    UserRequest,
    Status,
    ExistRequest,
)

import users_pb2_grpc


USERS = {
    '1234': '1234', 
    'admin': 'admin'
}


class UsersService(users_pb2_grpc.UsersServicer):

    def UserExist(self, request, context):
        if not (request.username in USERS):
            return ExistRequest(status=Status.NOT_EXIST)
        if USERS[request.username] != request.password:
            return ExistRequest(status=Status.INCORRECT_PASSWORD)
        return ExistRequest(status=Status.EXIST)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
