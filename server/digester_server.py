import hashlib
import time
from concurrent import futures

import grpc

import digestor_pb2
import digestor_pb2_grpc


class DigestorServicer(digestor_pb2_grpc.DigestorServicer):

    def __init__(self, *args, **kwargs):
        self.server_port = 46001

    def GetDigestor(self, request, context):
        """
        Implementation of the rpc GetDigest declared in the proto
        file above.
        """

        # get the string from the incoming request.
        to_be_digested = request.ToDigest
        print(f'String to be digest received: {to_be_digested}')

        # digest and get the string representation
        # from the digestor.
        hasher = hashlib.sha256()
        hasher.update(to_be_digested.encode())
        digested = hasher.hexdigest()

        result = {'Digested': digested, 'WasDigested': True}
        return digestor_pb2.DigestedMessage(**result)

    def start_server(self):
        digestor_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        digestor_pb2_grpc.add_DigestorServicer_to_server(DigestorServicer(), digestor_server)

        digestor_server.add_insecure_port(f'[::]:{self.server_port}')

        digestor_server.start()
        print('Digestor server running')

        try:
            # need an infinite loop since the above
            # code is non blocking, and if I don't do this
            # the program will exit.
            while True:
                time.sleep(60 * 60 * 60)
        except KeyboardInterrupt:
            digestor_server.stop(0)
            print('Digestor Server Stopped ...')


if __name__ == '__main__':
    curr_server = DigestorServicer()
    curr_server.start_server()
