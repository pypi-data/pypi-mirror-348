"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'api/nodes/application.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bapi/nodes/application.proto\x12\x07synapse"%\n\x15ApplicationNodeConfig\x12\x0c\n\x04name\x18\x01 \x01(\t"6\n\x15ApplicationNodeStatus\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07running\x18\x02 \x01(\x08b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.nodes.application_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_APPLICATIONNODECONFIG']._serialized_start = 40
    _globals['_APPLICATIONNODECONFIG']._serialized_end = 77
    _globals['_APPLICATIONNODESTATUS']._serialized_start = 79
    _globals['_APPLICATIONNODESTATUS']._serialized_end = 133