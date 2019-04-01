import grpc
import digestor_pb2
import digestor_pb2_grpc


class DigestorClient(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 46001

        # communication channel instance.
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

        self.stub = digestor_pb2_grpc.DigestorStub(self.channel)

    def get_digest(self, message: str):
        result = digestor_pb2.DigestMessage(ToDigest=message)
        return self.stub.GetDigestor(result)


if __name__ == '__main__':
    client = DigestorClient()
    result = client.get_digest('hello world grpc!')
    print(result)
