//
//  Generated code. Do not modify.
//  source: protos/dart_vm_service.proto
//
// @dart = 3.3

// ignore_for_file: annotate_overrides, camel_case_types, comment_references
// ignore_for_file: constant_identifier_names, library_prefixes
// ignore_for_file: non_constant_identifier_names, prefer_final_fields
// ignore_for_file: unnecessary_import, unnecessary_this, unused_import

import 'dart:convert' as $convert;
import 'dart:core' as $core;
import 'dart:typed_data' as $typed_data;

@$core.Deprecated('Use connectRequestDescriptor instead')
const ConnectRequest$json = {
  '1': 'ConnectRequest',
  '2': [
    {'1': 'vm_service_uri', '3': 1, '4': 1, '5': 9, '10': 'vmServiceUri'},
  ],
};

/// Descriptor for `ConnectRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List connectRequestDescriptor = $convert.base64Decode(
    'Cg5Db25uZWN0UmVxdWVzdBIkCg52bV9zZXJ2aWNlX3VyaRgBIAEoCVIMdm1TZXJ2aWNlVXJp');

@$core.Deprecated('Use connectResponseDescriptor instead')
const ConnectResponse$json = {
  '1': 'ConnectResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
  ],
};

/// Descriptor for `ConnectResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List connectResponseDescriptor = $convert.base64Decode(
    'Cg9Db25uZWN0UmVzcG9uc2USGAoHc3VjY2VzcxgBIAEoCFIHc3VjY2VzcxIYCgdtZXNzYWdlGA'
    'IgASgJUgdtZXNzYWdl');

@$core.Deprecated('Use emptyRequestDescriptor instead')
const EmptyRequest$json = {
  '1': 'EmptyRequest',
};

/// Descriptor for `EmptyRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List emptyRequestDescriptor = $convert.base64Decode(
    'CgxFbXB0eVJlcXVlc3Q=');

@$core.Deprecated('Use toggleRequestDescriptor instead')
const ToggleRequest$json = {
  '1': 'ToggleRequest',
  '2': [
    {'1': 'enable', '3': 1, '4': 1, '5': 8, '10': 'enable'},
  ],
};

/// Descriptor for `ToggleRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List toggleRequestDescriptor = $convert.base64Decode(
    'Cg1Ub2dnbGVSZXF1ZXN0EhYKBmVuYWJsZRgBIAEoCFIGZW5hYmxl');

@$core.Deprecated('Use toggleResponseDescriptor instead')
const ToggleResponse$json = {
  '1': 'ToggleResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
  ],
};

/// Descriptor for `ToggleResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List toggleResponseDescriptor = $convert.base64Decode(
    'Cg5Ub2dnbGVSZXNwb25zZRIYCgdzdWNjZXNzGAEgASgIUgdzdWNjZXNzEhgKB21lc3NhZ2UYAi'
    'ABKAlSB21lc3NhZ2U=');

@$core.Deprecated('Use viewIdRequestDescriptor instead')
const ViewIdRequest$json = {
  '1': 'ViewIdRequest',
  '2': [
    {'1': 'view_id', '3': 1, '4': 1, '5': 9, '10': 'viewId'},
  ],
};

/// Descriptor for `ViewIdRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List viewIdRequestDescriptor = $convert.base64Decode(
    'Cg1WaWV3SWRSZXF1ZXN0EhcKB3ZpZXdfaWQYASABKAlSBnZpZXdJZA==');

@$core.Deprecated('Use displayRefreshRateResponseDescriptor instead')
const DisplayRefreshRateResponse$json = {
  '1': 'DisplayRefreshRateResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
    {'1': 'refresh_rate', '3': 3, '4': 1, '5': 1, '10': 'refreshRate'},
  ],
};

/// Descriptor for `DisplayRefreshRateResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List displayRefreshRateResponseDescriptor = $convert.base64Decode(
    'ChpEaXNwbGF5UmVmcmVzaFJhdGVSZXNwb25zZRIYCgdzdWNjZXNzGAEgASgIUgdzdWNjZXNzEh'
    'gKB21lc3NhZ2UYAiABKAlSB21lc3NhZ2USIQoMcmVmcmVzaF9yYXRlGAMgASgBUgtyZWZyZXNo'
    'UmF0ZQ==');

@$core.Deprecated('Use listViewsResponseDescriptor instead')
const ListViewsResponse$json = {
  '1': 'ListViewsResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
    {'1': 'views', '3': 3, '4': 3, '5': 9, '10': 'views'},
  ],
};

/// Descriptor for `ListViewsResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List listViewsResponseDescriptor = $convert.base64Decode(
    'ChFMaXN0Vmlld3NSZXNwb25zZRIYCgdzdWNjZXNzGAEgASgIUgdzdWNjZXNzEhgKB21lc3NhZ2'
    'UYAiABKAlSB21lc3NhZ2USFAoFdmlld3MYAyADKAlSBXZpZXdz');

@$core.Deprecated('Use doubleValueRequestDescriptor instead')
const DoubleValueRequest$json = {
  '1': 'DoubleValueRequest',
  '2': [
    {'1': 'value', '3': 1, '4': 1, '5': 1, '10': 'value'},
  ],
};

/// Descriptor for `DoubleValueRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List doubleValueRequestDescriptor = $convert.base64Decode(
    'ChJEb3VibGVWYWx1ZVJlcXVlc3QSFAoFdmFsdWUYASABKAFSBXZhbHVl');

@$core.Deprecated('Use boolValueRequestDescriptor instead')
const BoolValueRequest$json = {
  '1': 'BoolValueRequest',
  '2': [
    {'1': 'value', '3': 1, '4': 1, '5': 8, '10': 'value'},
  ],
};

/// Descriptor for `BoolValueRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List boolValueRequestDescriptor = $convert.base64Decode(
    'ChBCb29sVmFsdWVSZXF1ZXN0EhQKBXZhbHVlGAEgASgIUgV2YWx1ZQ==');

@$core.Deprecated('Use stringValueRequestDescriptor instead')
const StringValueRequest$json = {
  '1': 'StringValueRequest',
  '2': [
    {'1': 'value', '3': 1, '4': 1, '5': 9, '10': 'value'},
  ],
};

/// Descriptor for `StringValueRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List stringValueRequestDescriptor = $convert.base64Decode(
    'ChJTdHJpbmdWYWx1ZVJlcXVlc3QSFAoFdmFsdWUYASABKAlSBXZhbHVl');

@$core.Deprecated('Use genericResponseDescriptor instead')
const GenericResponse$json = {
  '1': 'GenericResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
    {'1': 'data', '3': 3, '4': 1, '5': 9, '10': 'data'},
  ],
};

/// Descriptor for `GenericResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List genericResponseDescriptor = $convert.base64Decode(
    'Cg9HZW5lcmljUmVzcG9uc2USGAoHc3VjY2VzcxgBIAEoCFIHc3VjY2VzcxIYCgdtZXNzYWdlGA'
    'IgASgJUgdtZXNzYWdlEhIKBGRhdGEYAyABKAlSBGRhdGE=');

@$core.Deprecated('Use stringListRequestDescriptor instead')
const StringListRequest$json = {
  '1': 'StringListRequest',
  '2': [
    {'1': 'values', '3': 1, '4': 3, '5': 9, '10': 'values'},
  ],
};

/// Descriptor for `StringListRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List stringListRequestDescriptor = $convert.base64Decode(
    'ChFTdHJpbmdMaXN0UmVxdWVzdBIWCgZ2YWx1ZXMYASADKAlSBnZhbHVlcw==');

@$core.Deprecated('Use stringListResponseDescriptor instead')
const StringListResponse$json = {
  '1': 'StringListResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
    {'1': 'values', '3': 3, '4': 3, '5': 9, '10': 'values'},
  ],
};

/// Descriptor for `StringListResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List stringListResponseDescriptor = $convert.base64Decode(
    'ChJTdHJpbmdMaXN0UmVzcG9uc2USGAoHc3VjY2VzcxgBIAEoCFIHc3VjY2VzcxIYCgdtZXNzYW'
    'dlGAIgASgJUgdtZXNzYWdlEhYKBnZhbHVlcxgDIAMoCVIGdmFsdWVz');

@$core.Deprecated('Use enterTextRequestDescriptor instead')
const EnterTextRequest$json = {
  '1': 'EnterTextRequest',
  '2': [
    {'1': 'key_value', '3': 1, '4': 1, '5': 9, '10': 'keyValue'},
    {'1': 'text', '3': 2, '4': 1, '5': 9, '10': 'text'},
  ],
};

/// Descriptor for `EnterTextRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List enterTextRequestDescriptor = $convert.base64Decode(
    'ChBFbnRlclRleHRSZXF1ZXN0EhsKCWtleV92YWx1ZRgBIAEoCVIIa2V5VmFsdWUSEgoEdGV4dB'
    'gCIAEoCVIEdGV4dA==');

@$core.Deprecated('Use ancestorDescendantRequestDescriptor instead')
const AncestorDescendantRequest$json = {
  '1': 'AncestorDescendantRequest',
  '2': [
    {'1': 'ancestor_type', '3': 1, '4': 1, '5': 9, '10': 'ancestorType'},
    {'1': 'descendant_type', '3': 2, '4': 1, '5': 9, '10': 'descendantType'},
  ],
};

/// Descriptor for `AncestorDescendantRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List ancestorDescendantRequestDescriptor = $convert.base64Decode(
    'ChlBbmNlc3RvckRlc2NlbmRhbnRSZXF1ZXN0EiMKDWFuY2VzdG9yX3R5cGUYASABKAlSDGFuY2'
    'VzdG9yVHlwZRInCg9kZXNjZW5kYW50X3R5cGUYAiABKAlSDmRlc2NlbmRhbnRUeXBl');

@$core.Deprecated('Use treeDumpResponseDescriptor instead')
const TreeDumpResponse$json = {
  '1': 'TreeDumpResponse',
  '2': [
    {'1': 'success', '3': 1, '4': 1, '5': 8, '10': 'success'},
    {'1': 'message', '3': 2, '4': 1, '5': 9, '10': 'message'},
    {'1': 'tree_dump', '3': 3, '4': 1, '5': 9, '10': 'treeDump'},
  ],
};

/// Descriptor for `TreeDumpResponse`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List treeDumpResponseDescriptor = $convert.base64Decode(
    'ChBUcmVlRHVtcFJlc3BvbnNlEhgKB3N1Y2Nlc3MYASABKAhSB3N1Y2Nlc3MSGAoHbWVzc2FnZR'
    'gCIAEoCVIHbWVzc2FnZRIbCgl0cmVlX2R1bXAYAyABKAlSCHRyZWVEdW1w');

@$core.Deprecated('Use objectGroupRequestDescriptor instead')
const ObjectGroupRequest$json = {
  '1': 'ObjectGroupRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
  ],
};

/// Descriptor for `ObjectGroupRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List objectGroupRequestDescriptor = $convert.base64Decode(
    'ChJPYmplY3RHcm91cFJlcXVlc3QSIQoMb2JqZWN0X2dyb3VwGAEgASgJUgtvYmplY3RHcm91cA'
    '==');

@$core.Deprecated('Use selectedWidgetRequestDescriptor instead')
const SelectedWidgetRequest$json = {
  '1': 'SelectedWidgetRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
    {'1': 'previous_selection_id', '3': 2, '4': 1, '5': 9, '10': 'previousSelectionId'},
  ],
};

/// Descriptor for `SelectedWidgetRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List selectedWidgetRequestDescriptor = $convert.base64Decode(
    'ChVTZWxlY3RlZFdpZGdldFJlcXVlc3QSIQoMb2JqZWN0X2dyb3VwGAEgASgJUgtvYmplY3RHcm'
    '91cBIyChVwcmV2aW91c19zZWxlY3Rpb25faWQYAiABKAlSE3ByZXZpb3VzU2VsZWN0aW9uSWQ=');

@$core.Deprecated('Use selectionByIdRequestDescriptor instead')
const SelectionByIdRequest$json = {
  '1': 'SelectionByIdRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
    {'1': 'object_id', '3': 2, '4': 1, '5': 9, '10': 'objectId'},
  ],
};

/// Descriptor for `SelectionByIdRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List selectionByIdRequestDescriptor = $convert.base64Decode(
    'ChRTZWxlY3Rpb25CeUlkUmVxdWVzdBIhCgxvYmplY3RfZ3JvdXAYASABKAlSC29iamVjdEdyb3'
    'VwEhsKCW9iamVjdF9pZBgCIAEoCVIIb2JqZWN0SWQ=');

@$core.Deprecated('Use disposeIdRequestDescriptor instead')
const DisposeIdRequest$json = {
  '1': 'DisposeIdRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
    {'1': 'object_id', '3': 2, '4': 1, '5': 9, '10': 'objectId'},
  ],
};

/// Descriptor for `DisposeIdRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List disposeIdRequestDescriptor = $convert.base64Decode(
    'ChBEaXNwb3NlSWRSZXF1ZXN0EiEKDG9iamVjdF9ncm91cBgBIAEoCVILb2JqZWN0R3JvdXASGw'
    'oJb2JqZWN0X2lkGAIgASgJUghvYmplY3RJZA==');

@$core.Deprecated('Use widgetRequestDescriptor instead')
const WidgetRequest$json = {
  '1': 'WidgetRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
    {'1': 'widget_id', '3': 2, '4': 1, '5': 9, '10': 'widgetId'},
  ],
};

/// Descriptor for `WidgetRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List widgetRequestDescriptor = $convert.base64Decode(
    'Cg1XaWRnZXRSZXF1ZXN0EiEKDG9iamVjdF9ncm91cBgBIAEoCVILb2JqZWN0R3JvdXASGwoJd2'
    'lkZ2V0X2lkGAIgASgJUgh3aWRnZXRJZA==');

@$core.Deprecated('Use detailSubtreeRequestDescriptor instead')
const DetailSubtreeRequest$json = {
  '1': 'DetailSubtreeRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
    {'1': 'widget_id', '3': 2, '4': 1, '5': 9, '10': 'widgetId'},
    {'1': 'subtree_depth', '3': 3, '4': 1, '5': 5, '10': 'subtreeDepth'},
  ],
};

/// Descriptor for `DetailSubtreeRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List detailSubtreeRequestDescriptor = $convert.base64Decode(
    'ChREZXRhaWxTdWJ0cmVlUmVxdWVzdBIhCgxvYmplY3RfZ3JvdXAYASABKAlSC29iamVjdEdyb3'
    'VwEhsKCXdpZGdldF9pZBgCIAEoCVIId2lkZ2V0SWQSIwoNc3VidHJlZV9kZXB0aBgDIAEoBVIM'
    'c3VidHJlZURlcHRo');

@$core.Deprecated('Use screenshotRequestDescriptor instead')
const ScreenshotRequest$json = {
  '1': 'ScreenshotRequest',
  '2': [
    {'1': 'widget_id', '3': 1, '4': 1, '5': 9, '10': 'widgetId'},
    {'1': 'width', '3': 2, '4': 1, '5': 1, '10': 'width'},
    {'1': 'height', '3': 3, '4': 1, '5': 1, '10': 'height'},
    {'1': 'margin', '3': 4, '4': 1, '5': 1, '10': 'margin'},
    {'1': 'max_pixel_ratio', '3': 5, '4': 1, '5': 1, '10': 'maxPixelRatio'},
    {'1': 'debug_paint', '3': 6, '4': 1, '5': 8, '10': 'debugPaint'},
  ],
};

/// Descriptor for `ScreenshotRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List screenshotRequestDescriptor = $convert.base64Decode(
    'ChFTY3JlZW5zaG90UmVxdWVzdBIbCgl3aWRnZXRfaWQYASABKAlSCHdpZGdldElkEhQKBXdpZH'
    'RoGAIgASgBUgV3aWR0aBIWCgZoZWlnaHQYAyABKAFSBmhlaWdodBIWCgZtYXJnaW4YBCABKAFS'
    'Bm1hcmdpbhImCg9tYXhfcGl4ZWxfcmF0aW8YBSABKAFSDW1heFBpeGVsUmF0aW8SHwoLZGVidW'
    'dfcGFpbnQYBiABKAhSCmRlYnVnUGFpbnQ=');

@$core.Deprecated('Use layoutExplorerRequestDescriptor instead')
const LayoutExplorerRequest$json = {
  '1': 'LayoutExplorerRequest',
  '2': [
    {'1': 'object_group', '3': 1, '4': 1, '5': 9, '10': 'objectGroup'},
    {'1': 'widget_id', '3': 2, '4': 1, '5': 9, '10': 'widgetId'},
    {'1': 'subtree_depth', '3': 3, '4': 1, '5': 5, '10': 'subtreeDepth'},
  ],
};

/// Descriptor for `LayoutExplorerRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List layoutExplorerRequestDescriptor = $convert.base64Decode(
    'ChVMYXlvdXRFeHBsb3JlclJlcXVlc3QSIQoMb2JqZWN0X2dyb3VwGAEgASgJUgtvYmplY3RHcm'
    '91cBIbCgl3aWRnZXRfaWQYAiABKAlSCHdpZGdldElkEiMKDXN1YnRyZWVfZGVwdGgYAyABKAVS'
    'DHN1YnRyZWVEZXB0aA==');

@$core.Deprecated('Use flexFitRequestDescriptor instead')
const FlexFitRequest$json = {
  '1': 'FlexFitRequest',
  '2': [
    {'1': 'widget_id', '3': 1, '4': 1, '5': 9, '10': 'widgetId'},
    {'1': 'flex_fit', '3': 2, '4': 1, '5': 9, '10': 'flexFit'},
  ],
};

/// Descriptor for `FlexFitRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List flexFitRequestDescriptor = $convert.base64Decode(
    'Cg5GbGV4Rml0UmVxdWVzdBIbCgl3aWRnZXRfaWQYASABKAlSCHdpZGdldElkEhkKCGZsZXhfZm'
    'l0GAIgASgJUgdmbGV4Rml0');

@$core.Deprecated('Use flexFactorRequestDescriptor instead')
const FlexFactorRequest$json = {
  '1': 'FlexFactorRequest',
  '2': [
    {'1': 'widget_id', '3': 1, '4': 1, '5': 9, '10': 'widgetId'},
    {'1': 'flex_factor', '3': 2, '4': 1, '5': 5, '10': 'flexFactor'},
  ],
};

/// Descriptor for `FlexFactorRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List flexFactorRequestDescriptor = $convert.base64Decode(
    'ChFGbGV4RmFjdG9yUmVxdWVzdBIbCgl3aWRnZXRfaWQYASABKAlSCHdpZGdldElkEh8KC2ZsZX'
    'hfZmFjdG9yGAIgASgFUgpmbGV4RmFjdG9y');

@$core.Deprecated('Use flexPropertiesRequestDescriptor instead')
const FlexPropertiesRequest$json = {
  '1': 'FlexPropertiesRequest',
  '2': [
    {'1': 'widget_id', '3': 1, '4': 1, '5': 9, '10': 'widgetId'},
    {'1': 'main_axis_alignment', '3': 2, '4': 1, '5': 9, '10': 'mainAxisAlignment'},
    {'1': 'cross_axis_alignment', '3': 3, '4': 1, '5': 9, '10': 'crossAxisAlignment'},
  ],
};

/// Descriptor for `FlexPropertiesRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List flexPropertiesRequestDescriptor = $convert.base64Decode(
    'ChVGbGV4UHJvcGVydGllc1JlcXVlc3QSGwoJd2lkZ2V0X2lkGAEgASgJUgh3aWRnZXRJZBIuCh'
    'NtYWluX2F4aXNfYWxpZ25tZW50GAIgASgJUhFtYWluQXhpc0FsaWdubWVudBIwChRjcm9zc19h'
    'eGlzX2FsaWdubWVudBgDIAEoCVISY3Jvc3NBeGlzQWxpZ25tZW50');

@$core.Deprecated('Use screenItemsRequestDescriptor instead')
const ScreenItemsRequest$json = {
  '1': 'ScreenItemsRequest',
  '2': [
    {'1': 'max_depth', '3': 1, '4': 1, '5': 5, '10': 'maxDepth'},
  ],
};

/// Descriptor for `ScreenItemsRequest`. Decode as a `google.protobuf.DescriptorProto`.
final $typed_data.Uint8List screenItemsRequestDescriptor = $convert.base64Decode(
    'ChJTY3JlZW5JdGVtc1JlcXVlc3QSGwoJbWF4X2RlcHRoGAEgASgFUghtYXhEZXB0aA==');

