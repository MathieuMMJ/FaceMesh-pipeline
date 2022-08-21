# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import component_pb2 as component__pb2


class OpenPoseEstimatorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.estimate = channel.unary_unary(
                '/OpenPoseEstimator/estimate',
                request_serializer=component__pb2.Image.SerializeToString,
                response_deserializer=component__pb2.Poses.FromString,
                )
        self.estimateImg = channel.unary_unary(
                '/OpenPoseEstimator/estimateImg',
                request_serializer=component__pb2.Image.SerializeToString,
                response_deserializer=component__pb2.Image.FromString,
                )


class OpenPoseEstimatorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def estimate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def estimateImg(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OpenPoseEstimatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'estimate': grpc.unary_unary_rpc_method_handler(
                    servicer.estimate,
                    request_deserializer=component__pb2.Image.FromString,
                    response_serializer=component__pb2.Poses.SerializeToString,
            ),
            'estimateImg': grpc.unary_unary_rpc_method_handler(
                    servicer.estimateImg,
                    request_deserializer=component__pb2.Image.FromString,
                    response_serializer=component__pb2.Image.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'OpenPoseEstimator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OpenPoseEstimator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def estimate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OpenPoseEstimator/estimate',
            component__pb2.Image.SerializeToString,
            component__pb2.Poses.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def estimateImg(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OpenPoseEstimator/estimateImg',
            component__pb2.Image.SerializeToString,
            component__pb2.Image.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
