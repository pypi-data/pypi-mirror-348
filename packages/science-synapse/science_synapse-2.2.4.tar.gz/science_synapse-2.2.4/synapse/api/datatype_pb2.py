"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'api/datatype.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12api/datatype.proto\x12\x07synapse"\x86\x03\n\x06Tensor\x12\x14\n\x0ctimestamp_ns\x18\x01 \x01(\x04\x12\r\n\x05shape\x18\x02 \x03(\x05\x12$\n\x05dtype\x18\x03 \x01(\x0e2\x15.synapse.Tensor.DType\x12.\n\nendianness\x18\x04 \x01(\x0e2\x1a.synapse.Tensor.Endianness\x12\x0c\n\x04data\x18\x05 \x01(\x0c"\xb3\x01\n\x05DType\x12\x0e\n\nDT_INVALID\x10\x00\x12\x0c\n\x08DT_FLOAT\x10\x01\x12\r\n\tDT_DOUBLE\x10\x02\x12\x0c\n\x08DT_UINT8\x10\x03\x12\r\n\tDT_UINT16\x10\x04\x12\r\n\tDT_UINT32\x10\x05\x12\r\n\tDT_UINT64\x10\x06\x12\x0b\n\x07DT_INT8\x10\x07\x12\x0c\n\x08DT_INT16\x10\x08\x12\x0c\n\x08DT_INT32\x10\t\x12\x0c\n\x08DT_INT64\x10\n\x12\x0b\n\x07DT_BOOL\x10\x0b"=\n\nEndianness\x12\x18\n\x14TENSOR_LITTLE_ENDIAN\x10\x00\x12\x15\n\x11TENSOR_BIG_ENDIAN\x10\x01"k\n\x0eBroadbandFrame\x12\x14\n\x0ctimestamp_ns\x18\x01 \x01(\x04\x12\x17\n\x0fsequence_number\x18\x02 \x01(\x04\x12\x12\n\nframe_data\x18\x03 \x03(\x11\x12\x16\n\x0esample_rate_hz\x18\x04 \x01(\r"~\n\nTimeseries\x12\n\n\x02id\x18\x01 \x01(\r\x121\n\ndatapoints\x18\x02 \x03(\x0b2\x1d.synapse.Timeseries.Datapoint\x1a1\n\tDatapoint\x12\x14\n\x0ctimestamp_ns\x18\x01 \x01(\x04\x12\x0e\n\x06sample\x18\x02 \x01(\x11*x\n\x08DataType\x12\x14\n\x10kDataTypeUnknown\x10\x00\x12\x08\n\x04kAny\x10\x01\x12\x0e\n\nkBroadband\x10\x02\x12\x0f\n\x0bkSpiketrain\x10\x03\x12\x0f\n\x0bkTimestamps\x10\x04\x12\n\n\x06kImage\x10\x05\x12\x0e\n\nkWaveforms\x10\x06b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.datatype_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_DATATYPE']._serialized_start = 661
    _globals['_DATATYPE']._serialized_end = 781
    _globals['_TENSOR']._serialized_start = 32
    _globals['_TENSOR']._serialized_end = 422
    _globals['_TENSOR_DTYPE']._serialized_start = 180
    _globals['_TENSOR_DTYPE']._serialized_end = 359
    _globals['_TENSOR_ENDIANNESS']._serialized_start = 361
    _globals['_TENSOR_ENDIANNESS']._serialized_end = 422
    _globals['_BROADBANDFRAME']._serialized_start = 424
    _globals['_BROADBANDFRAME']._serialized_end = 531
    _globals['_TIMESERIES']._serialized_start = 533
    _globals['_TIMESERIES']._serialized_end = 659
    _globals['_TIMESERIES_DATAPOINT']._serialized_start = 610
    _globals['_TIMESERIES_DATAPOINT']._serialized_end = 659