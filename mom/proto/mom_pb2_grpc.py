# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import proto.mom_pb2 as mom__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in mom_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class MOMServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SavePendingService = channel.unary_unary(
                '/mom.MOMService/SavePendingService',
                request_serializer=mom__pb2.SavePendingServiceParameters.SerializeToString,
                response_deserializer=mom__pb2.SavePendingServiceResponse.FromString,
                _registered_method=True)
        self.RetrievePendingService = channel.unary_unary(
                '/mom.MOMService/RetrievePendingService',
                request_serializer=mom__pb2.RetrievePendingServiceParameters.SerializeToString,
                response_deserializer=mom__pb2.RetrievePendingServiceResponse.FromString,
                _registered_method=True)


class MOMServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SavePendingService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrievePendingService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MOMServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SavePendingService': grpc.unary_unary_rpc_method_handler(
                    servicer.SavePendingService,
                    request_deserializer=mom__pb2.SavePendingServiceParameters.FromString,
                    response_serializer=mom__pb2.SavePendingServiceResponse.SerializeToString,
            ),
            'RetrievePendingService': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrievePendingService,
                    request_deserializer=mom__pb2.RetrievePendingServiceParameters.FromString,
                    response_serializer=mom__pb2.RetrievePendingServiceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mom.MOMService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('mom.MOMService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MOMService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SavePendingService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mom.MOMService/SavePendingService',
            mom__pb2.SavePendingServiceParameters.SerializeToString,
            mom__pb2.SavePendingServiceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RetrievePendingService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/mom.MOMService/RetrievePendingService',
            mom__pb2.RetrievePendingServiceParameters.SerializeToString,
            mom__pb2.RetrievePendingServiceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
