# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: subtraction_service.proto
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
    'subtraction_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19subtraction_service.proto\x12\x13subtraction_service\"B\n\x16SubtractNumbersRequest\x12\x13\n\x0bparameter_a\x18\x01 \x01(\x01\x12\x13\n\x0bparameter_b\x18\x02 \x01(\x01\")\n\x17SubtractNumbersResponse\x12\x0e\n\x06result\x18\x01 \x01(\t2\x84\x01\n\x12SubtractionService\x12n\n\x0fSubtractNumbers\x12+.subtraction_service.SubtractNumbersRequest\x1a,.subtraction_service.SubtractNumbersResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'subtraction_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SUBTRACTNUMBERSREQUEST']._serialized_start=50
  _globals['_SUBTRACTNUMBERSREQUEST']._serialized_end=116
  _globals['_SUBTRACTNUMBERSRESPONSE']._serialized_start=118
  _globals['_SUBTRACTNUMBERSRESPONSE']._serialized_end=159
  _globals['_SUBTRACTIONSERVICE']._serialized_start=162
  _globals['_SUBTRACTIONSERVICE']._serialized_end=294
# @@protoc_insertion_point(module_scope)
