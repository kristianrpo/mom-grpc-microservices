# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: microservice.proto
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
    'microservice.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12microservice.proto\"@\n\x14SumNumbersParameters\x12\x13\n\x0bparameter_a\x18\x01 \x01(\x05\x12\x13\n\x0bparameter_b\x18\x02 \x01(\x05\"$\n\x12SumNumbersResponse\x12\x0e\n\x06result\x18\x01 \x01(\t2M\n\x11\x43\x61lculatorService\x12\x38\n\nSumNumbers\x12\x15.SumNumbersParameters\x1a\x13.SumNumbersResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'microservice_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SUMNUMBERSPARAMETERS']._serialized_start=22
  _globals['_SUMNUMBERSPARAMETERS']._serialized_end=86
  _globals['_SUMNUMBERSRESPONSE']._serialized_start=88
  _globals['_SUMNUMBERSRESPONSE']._serialized_end=124
  _globals['_CALCULATORSERVICE']._serialized_start=126
  _globals['_CALCULATORSERVICE']._serialized_end=203
# @@protoc_insertion_point(module_scope)
