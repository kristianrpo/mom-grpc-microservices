# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: multiplication_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'multiplication_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cmultiplication_service.proto\x12\x16multiplication_service\"B\n\x16MultiplyNumbersRequest\x12\x13\n\x0bparameter_a\x18\x01 \x01(\x01\x12\x13\n\x0bparameter_b\x18\x02 \x01(\x01\")\n\x17MultiplyNumbersResponse\x12\x0e\n\x06result\x18\x01 \x01(\t2\x8d\x01\n\x15MultiplicationService\x12t\n\x0fMultiplyNumbers\x12..multiplication_service.MultiplyNumbersRequest\x1a/.multiplication_service.MultiplyNumbersResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'multiplication_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MULTIPLYNUMBERSREQUEST']._serialized_start=56
  _globals['_MULTIPLYNUMBERSREQUEST']._serialized_end=122
  _globals['_MULTIPLYNUMBERSRESPONSE']._serialized_start=124
  _globals['_MULTIPLYNUMBERSRESPONSE']._serialized_end=165
  _globals['_MULTIPLICATIONSERVICE']._serialized_start=168
  _globals['_MULTIPLICATIONSERVICE']._serialized_end=309
# @@protoc_insertion_point(module_scope)
