# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: service.proto
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
    'service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\tmyservice\"\x1e\n\x0eRequestMessage\x12\x0c\n\x04name\x18\x01 \x01(\t\"\"\n\x0fResponseMessage\x12\x0f\n\x07message\x18\x01 \x01(\t2N\n\tMyService\x12\x41\n\x08SayHello\x12\x19.myservice.RequestMessage\x1a\x1a.myservice.ResponseMessageb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REQUESTMESSAGE']._serialized_start=28
  _globals['_REQUESTMESSAGE']._serialized_end=58
  _globals['_RESPONSEMESSAGE']._serialized_start=60
  _globals['_RESPONSEMESSAGE']._serialized_end=94
  _globals['_MYSERVICE']._serialized_start=96
  _globals['_MYSERVICE']._serialized_end=174
# @@protoc_insertion_point(module_scope)
