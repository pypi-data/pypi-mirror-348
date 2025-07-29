//
//  Generated code. Do not modify.
//  source: dart_vm_service.proto
//
// @dart = 3.3

// ignore_for_file: annotate_overrides, camel_case_types, comment_references
// ignore_for_file: constant_identifier_names, library_prefixes
// ignore_for_file: non_constant_identifier_names, prefer_final_fields
// ignore_for_file: unnecessary_import, unnecessary_this, unused_import

import 'dart:async' as $async;
import 'dart:core' as $core;

import 'package:grpc/service_api.dart' as $grpc;
import 'package:protobuf/protobuf.dart' as $pb;

import 'dart_vm_service.pb.dart' as $0;

export 'dart_vm_service.pb.dart';

@$pb.GrpcServiceName('dart_vm_service.DartVmService')
class DartVmServiceClient extends $grpc.Client {
  static final _$connect = $grpc.ClientMethod<$0.ConnectRequest, $0.ConnectResponse>(
      '/dart_vm_service.DartVmService/Connect',
      ($0.ConnectRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ConnectResponse.fromBuffer(value));
  static final _$toggleDebugPaint = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleDebugPaint',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleRepaintRainbow = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleRepaintRainbow',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$togglePerformanceOverlay = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/TogglePerformanceOverlay',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleBaselinePainting = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleBaselinePainting',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleDebugBanner = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleDebugBanner',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleStructuredErrors = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleStructuredErrors',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleOversizedImages = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleOversizedImages',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleDisablePhysicalShapeLayers = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleDisablePhysicalShapeLayers',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleDisableOpacityLayers = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleDisableOpacityLayers',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleProfileWidgetBuilds = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleProfileWidgetBuilds',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleProfileUserWidgetBuilds = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleProfileUserWidgetBuilds',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleProfileRenderObjectPaints = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleProfileRenderObjectPaints',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleProfileRenderObjectLayouts = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleProfileRenderObjectLayouts',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleProfilePlatformChannels = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleProfilePlatformChannels',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleInspector = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleInspector',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleTrackRebuildWidgets = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleTrackRebuildWidgets',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$toggleTrackRepaintWidgets = $grpc.ClientMethod<$0.ToggleRequest, $0.ToggleResponse>(
      '/dart_vm_service.DartVmService/ToggleTrackRepaintWidgets',
      ($0.ToggleRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ToggleResponse.fromBuffer(value));
  static final _$getDisplayRefreshRate = $grpc.ClientMethod<$0.ViewIdRequest, $0.DisplayRefreshRateResponse>(
      '/dart_vm_service.DartVmService/GetDisplayRefreshRate',
      ($0.ViewIdRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.DisplayRefreshRateResponse.fromBuffer(value));
  static final _$listViews = $grpc.ClientMethod<$0.EmptyRequest, $0.ListViewsResponse>(
      '/dart_vm_service.DartVmService/ListViews',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.ListViewsResponse.fromBuffer(value));
  static final _$dumpWidgetTree = $grpc.ClientMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
      '/dart_vm_service.DartVmService/DumpWidgetTree',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.TreeDumpResponse.fromBuffer(value));
  static final _$dumpLayerTree = $grpc.ClientMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
      '/dart_vm_service.DartVmService/DumpLayerTree',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.TreeDumpResponse.fromBuffer(value));
  static final _$dumpRenderTree = $grpc.ClientMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
      '/dart_vm_service.DartVmService/DumpRenderTree',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.TreeDumpResponse.fromBuffer(value));
  static final _$dumpSemanticsTreeInTraversalOrder = $grpc.ClientMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
      '/dart_vm_service.DartVmService/DumpSemanticsTreeInTraversalOrder',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.TreeDumpResponse.fromBuffer(value));
  static final _$dumpSemanticsTreeInInverseHitTestOrder = $grpc.ClientMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
      '/dart_vm_service.DartVmService/DumpSemanticsTreeInInverseHitTestOrder',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.TreeDumpResponse.fromBuffer(value));
  static final _$dumpFocusTree = $grpc.ClientMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
      '/dart_vm_service.DartVmService/DumpFocusTree',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.TreeDumpResponse.fromBuffer(value));
  static final _$setTimeDilation = $grpc.ClientMethod<$0.DoubleValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetTimeDilation',
      ($0.DoubleValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$didSendFirstFrameEvent = $grpc.ClientMethod<$0.BoolValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/DidSendFirstFrameEvent',
      ($0.BoolValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$didSendFirstFrameRasterizedEvent = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/DidSendFirstFrameRasterizedEvent',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$evictAssets = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EvictAssets',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$reassemble = $grpc.ClientMethod<$0.EmptyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/Reassemble',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$exitApp = $grpc.ClientMethod<$0.EmptyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ExitApp',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setVmServiceUri = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetVmServiceUri',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setDevToolsServerAddress = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetDevToolsServerAddress',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setPlatformOverride = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetPlatformOverride',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setBrightnessOverride = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetBrightnessOverride',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setPubRootDirectories = $grpc.ClientMethod<$0.StringListRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetPubRootDirectories',
      ($0.StringListRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$addPubRootDirectories = $grpc.ClientMethod<$0.StringListRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/AddPubRootDirectories',
      ($0.StringListRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$removePubRootDirectories = $grpc.ClientMethod<$0.StringListRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/RemovePubRootDirectories',
      ($0.StringListRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getPubRootDirectories = $grpc.ClientMethod<$0.EmptyRequest, $0.StringListResponse>(
      '/dart_vm_service.DartVmService/GetPubRootDirectories',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.StringListResponse.fromBuffer(value));
  static final _$tapWidgetByKey = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/TapWidgetByKey',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$tapWidgetByText = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/TapWidgetByText',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$tapWidgetByType = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/TapWidgetByType',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$tapWidgetByTooltip = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/TapWidgetByTooltip',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$tapWidgetByAncestorAndDescendant = $grpc.ClientMethod<$0.AncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/TapWidgetByAncestorAndDescendant',
      ($0.AncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$enterText = $grpc.ClientMethod<$0.EnterTextRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EnterText',
      ($0.EnterTextRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$enterTextByKey = $grpc.ClientMethod<$0.EnterTextKeyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EnterTextByKey',
      ($0.EnterTextKeyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$enterTextByType = $grpc.ClientMethod<$0.EnterTextTypeRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EnterTextByType',
      ($0.EnterTextTypeRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$enterTextByText = $grpc.ClientMethod<$0.EnterTextTextRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EnterTextByText',
      ($0.EnterTextTextRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$enterTextByTooltip = $grpc.ClientMethod<$0.EnterTextTooltipRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EnterTextByTooltip',
      ($0.EnterTextTooltipRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$enterTextByAncestorAndDescendant = $grpc.ClientMethod<$0.EnterTextAncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/EnterTextByAncestorAndDescendant',
      ($0.EnterTextAncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByKey = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByKey',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByType = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByType',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByText = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByText',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByTooltip = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByTooltip',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByAncestorAndDescendant = $grpc.ClientMethod<$0.AncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByAncestorAndDescendant',
      ($0.AncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByKey = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByKey',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByType = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByType',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByText = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByText',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByTooltip = $grpc.ClientMethod<$0.StringValueRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByTooltip',
      ($0.StringValueRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByAncestorAndDescendant = $grpc.ClientMethod<$0.AncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByAncestorAndDescendant',
      ($0.AncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByKeyExtended = $grpc.ClientMethod<$0.ScrollKeyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByKeyExtended',
      ($0.ScrollKeyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByTypeExtended = $grpc.ClientMethod<$0.ScrollTypeRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByTypeExtended',
      ($0.ScrollTypeRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByTextExtended = $grpc.ClientMethod<$0.ScrollTextRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByTextExtended',
      ($0.ScrollTextRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByTooltipExtended = $grpc.ClientMethod<$0.ScrollTooltipRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByTooltipExtended',
      ($0.ScrollTooltipRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollDownByAncestorAndDescendantExtended = $grpc.ClientMethod<$0.ScrollAncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollDownByAncestorAndDescendantExtended',
      ($0.ScrollAncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByKeyExtended = $grpc.ClientMethod<$0.ScrollKeyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByKeyExtended',
      ($0.ScrollKeyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByTypeExtended = $grpc.ClientMethod<$0.ScrollTypeRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByTypeExtended',
      ($0.ScrollTypeRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByTextExtended = $grpc.ClientMethod<$0.ScrollTextRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByTextExtended',
      ($0.ScrollTextRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByTooltipExtended = $grpc.ClientMethod<$0.ScrollTooltipRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByTooltipExtended',
      ($0.ScrollTooltipRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollUpByAncestorAndDescendantExtended = $grpc.ClientMethod<$0.ScrollAncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollUpByAncestorAndDescendantExtended',
      ($0.ScrollAncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollIntoViewByKey = $grpc.ClientMethod<$0.ScrollIntoViewKeyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollIntoViewByKey',
      ($0.ScrollIntoViewKeyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollIntoViewByType = $grpc.ClientMethod<$0.ScrollIntoViewTypeRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollIntoViewByType',
      ($0.ScrollIntoViewTypeRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollIntoViewByText = $grpc.ClientMethod<$0.ScrollIntoViewTextRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollIntoViewByText',
      ($0.ScrollIntoViewTextRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollIntoViewByTooltip = $grpc.ClientMethod<$0.ScrollIntoViewTooltipRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollIntoViewByTooltip',
      ($0.ScrollIntoViewTooltipRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$scrollIntoViewByAncestorAndDescendant = $grpc.ClientMethod<$0.ScrollIntoViewAncestorDescendantRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/ScrollIntoViewByAncestorAndDescendant',
      ($0.ScrollIntoViewAncestorDescendantRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$isWidgetTreeReady = $grpc.ClientMethod<$0.EmptyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/IsWidgetTreeReady',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$isWidgetCreationTracked = $grpc.ClientMethod<$0.EmptyRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/IsWidgetCreationTracked',
      ($0.EmptyRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getRootWidget = $grpc.ClientMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetRootWidget',
      ($0.ObjectGroupRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getRootWidgetSummaryTree = $grpc.ClientMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetRootWidgetSummaryTree',
      ($0.ObjectGroupRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getRootWidgetSummaryTreeWithPreviews = $grpc.ClientMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetRootWidgetSummaryTreeWithPreviews',
      ($0.ObjectGroupRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getSelectedWidget = $grpc.ClientMethod<$0.SelectedWidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetSelectedWidget',
      ($0.SelectedWidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getSelectedSummaryWidget = $grpc.ClientMethod<$0.SelectedWidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetSelectedSummaryWidget',
      ($0.SelectedWidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setSelectionById = $grpc.ClientMethod<$0.SelectionByIdRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetSelectionById',
      ($0.SelectionByIdRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$disposeAllGroups = $grpc.ClientMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/DisposeAllGroups',
      ($0.ObjectGroupRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$disposeGroup = $grpc.ClientMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/DisposeGroup',
      ($0.ObjectGroupRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$disposeId = $grpc.ClientMethod<$0.DisposeIdRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/DisposeId',
      ($0.DisposeIdRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getParentChain = $grpc.ClientMethod<$0.WidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetParentChain',
      ($0.WidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getProperties = $grpc.ClientMethod<$0.WidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetProperties',
      ($0.WidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getChildren = $grpc.ClientMethod<$0.WidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetChildren',
      ($0.WidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getChildrenSummaryTree = $grpc.ClientMethod<$0.WidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetChildrenSummaryTree',
      ($0.WidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getChildrenDetailsSubtree = $grpc.ClientMethod<$0.WidgetRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetChildrenDetailsSubtree',
      ($0.WidgetRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getDetailsSubtree = $grpc.ClientMethod<$0.DetailSubtreeRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetDetailsSubtree',
      ($0.DetailSubtreeRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$screenshot = $grpc.ClientMethod<$0.ScreenshotRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/Screenshot',
      ($0.ScreenshotRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$getLayoutExplorerNode = $grpc.ClientMethod<$0.LayoutExplorerRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/GetLayoutExplorerNode',
      ($0.LayoutExplorerRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setFlexFit = $grpc.ClientMethod<$0.FlexFitRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetFlexFit',
      ($0.FlexFitRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setFlexFactor = $grpc.ClientMethod<$0.FlexFactorRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetFlexFactor',
      ($0.FlexFactorRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));
  static final _$setFlexProperties = $grpc.ClientMethod<$0.FlexPropertiesRequest, $0.GenericResponse>(
      '/dart_vm_service.DartVmService/SetFlexProperties',
      ($0.FlexPropertiesRequest value) => value.writeToBuffer(),
      ($core.List<$core.int> value) => $0.GenericResponse.fromBuffer(value));

  DartVmServiceClient($grpc.ClientChannel channel,
      {$grpc.CallOptions? options,
      $core.Iterable<$grpc.ClientInterceptor>? interceptors})
      : super(channel, options: options,
        interceptors: interceptors);

  $grpc.ResponseFuture<$0.ConnectResponse> connect($0.ConnectRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$connect, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleDebugPaint($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleDebugPaint, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleRepaintRainbow($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleRepaintRainbow, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> togglePerformanceOverlay($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$togglePerformanceOverlay, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleBaselinePainting($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleBaselinePainting, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleDebugBanner($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleDebugBanner, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleStructuredErrors($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleStructuredErrors, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleOversizedImages($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleOversizedImages, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleDisablePhysicalShapeLayers($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleDisablePhysicalShapeLayers, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleDisableOpacityLayers($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleDisableOpacityLayers, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleProfileWidgetBuilds($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleProfileWidgetBuilds, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleProfileUserWidgetBuilds($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleProfileUserWidgetBuilds, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleProfileRenderObjectPaints($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleProfileRenderObjectPaints, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleProfileRenderObjectLayouts($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleProfileRenderObjectLayouts, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleProfilePlatformChannels($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleProfilePlatformChannels, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleInspector($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleInspector, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleTrackRebuildWidgets($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleTrackRebuildWidgets, request, options: options);
  }

  $grpc.ResponseFuture<$0.ToggleResponse> toggleTrackRepaintWidgets($0.ToggleRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$toggleTrackRepaintWidgets, request, options: options);
  }

  $grpc.ResponseFuture<$0.DisplayRefreshRateResponse> getDisplayRefreshRate($0.ViewIdRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getDisplayRefreshRate, request, options: options);
  }

  $grpc.ResponseFuture<$0.ListViewsResponse> listViews($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$listViews, request, options: options);
  }

  $grpc.ResponseFuture<$0.TreeDumpResponse> dumpWidgetTree($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$dumpWidgetTree, request, options: options);
  }

  $grpc.ResponseFuture<$0.TreeDumpResponse> dumpLayerTree($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$dumpLayerTree, request, options: options);
  }

  $grpc.ResponseFuture<$0.TreeDumpResponse> dumpRenderTree($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$dumpRenderTree, request, options: options);
  }

  $grpc.ResponseFuture<$0.TreeDumpResponse> dumpSemanticsTreeInTraversalOrder($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$dumpSemanticsTreeInTraversalOrder, request, options: options);
  }

  $grpc.ResponseFuture<$0.TreeDumpResponse> dumpSemanticsTreeInInverseHitTestOrder($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$dumpSemanticsTreeInInverseHitTestOrder, request, options: options);
  }

  $grpc.ResponseFuture<$0.TreeDumpResponse> dumpFocusTree($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$dumpFocusTree, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setTimeDilation($0.DoubleValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setTimeDilation, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> didSendFirstFrameEvent($0.BoolValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$didSendFirstFrameEvent, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> didSendFirstFrameRasterizedEvent($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$didSendFirstFrameRasterizedEvent, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> evictAssets($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$evictAssets, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> reassemble($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$reassemble, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> exitApp($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$exitApp, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setVmServiceUri($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setVmServiceUri, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setDevToolsServerAddress($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setDevToolsServerAddress, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setPlatformOverride($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setPlatformOverride, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setBrightnessOverride($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setBrightnessOverride, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setPubRootDirectories($0.StringListRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setPubRootDirectories, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> addPubRootDirectories($0.StringListRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$addPubRootDirectories, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> removePubRootDirectories($0.StringListRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$removePubRootDirectories, request, options: options);
  }

  $grpc.ResponseFuture<$0.StringListResponse> getPubRootDirectories($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getPubRootDirectories, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> tapWidgetByKey($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$tapWidgetByKey, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> tapWidgetByText($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$tapWidgetByText, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> tapWidgetByType($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$tapWidgetByType, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> tapWidgetByTooltip($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$tapWidgetByTooltip, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> tapWidgetByAncestorAndDescendant($0.AncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$tapWidgetByAncestorAndDescendant, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> enterText($0.EnterTextRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$enterText, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> enterTextByKey($0.EnterTextKeyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$enterTextByKey, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> enterTextByType($0.EnterTextTypeRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$enterTextByType, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> enterTextByText($0.EnterTextTextRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$enterTextByText, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> enterTextByTooltip($0.EnterTextTooltipRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$enterTextByTooltip, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> enterTextByAncestorAndDescendant($0.EnterTextAncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$enterTextByAncestorAndDescendant, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByKey($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByKey, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByType($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByType, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByText($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByText, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByTooltip($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByTooltip, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByAncestorAndDescendant($0.AncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByAncestorAndDescendant, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByKey($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByKey, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByType($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByType, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByText($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByText, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByTooltip($0.StringValueRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByTooltip, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByAncestorAndDescendant($0.AncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByAncestorAndDescendant, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByKeyExtended($0.ScrollKeyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByKeyExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByTypeExtended($0.ScrollTypeRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByTypeExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByTextExtended($0.ScrollTextRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByTextExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByTooltipExtended($0.ScrollTooltipRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByTooltipExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollDownByAncestorAndDescendantExtended($0.ScrollAncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollDownByAncestorAndDescendantExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByKeyExtended($0.ScrollKeyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByKeyExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByTypeExtended($0.ScrollTypeRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByTypeExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByTextExtended($0.ScrollTextRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByTextExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByTooltipExtended($0.ScrollTooltipRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByTooltipExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollUpByAncestorAndDescendantExtended($0.ScrollAncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollUpByAncestorAndDescendantExtended, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollIntoViewByKey($0.ScrollIntoViewKeyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollIntoViewByKey, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollIntoViewByType($0.ScrollIntoViewTypeRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollIntoViewByType, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollIntoViewByText($0.ScrollIntoViewTextRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollIntoViewByText, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollIntoViewByTooltip($0.ScrollIntoViewTooltipRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollIntoViewByTooltip, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> scrollIntoViewByAncestorAndDescendant($0.ScrollIntoViewAncestorDescendantRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$scrollIntoViewByAncestorAndDescendant, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> isWidgetTreeReady($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$isWidgetTreeReady, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> isWidgetCreationTracked($0.EmptyRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$isWidgetCreationTracked, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getRootWidget($0.ObjectGroupRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getRootWidget, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getRootWidgetSummaryTree($0.ObjectGroupRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getRootWidgetSummaryTree, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getRootWidgetSummaryTreeWithPreviews($0.ObjectGroupRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getRootWidgetSummaryTreeWithPreviews, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getSelectedWidget($0.SelectedWidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getSelectedWidget, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getSelectedSummaryWidget($0.SelectedWidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getSelectedSummaryWidget, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setSelectionById($0.SelectionByIdRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setSelectionById, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> disposeAllGroups($0.ObjectGroupRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$disposeAllGroups, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> disposeGroup($0.ObjectGroupRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$disposeGroup, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> disposeId($0.DisposeIdRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$disposeId, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getParentChain($0.WidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getParentChain, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getProperties($0.WidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getProperties, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getChildren($0.WidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getChildren, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getChildrenSummaryTree($0.WidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getChildrenSummaryTree, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getChildrenDetailsSubtree($0.WidgetRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getChildrenDetailsSubtree, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getDetailsSubtree($0.DetailSubtreeRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getDetailsSubtree, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> screenshot($0.ScreenshotRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$screenshot, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> getLayoutExplorerNode($0.LayoutExplorerRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$getLayoutExplorerNode, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setFlexFit($0.FlexFitRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setFlexFit, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setFlexFactor($0.FlexFactorRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setFlexFactor, request, options: options);
  }

  $grpc.ResponseFuture<$0.GenericResponse> setFlexProperties($0.FlexPropertiesRequest request, {$grpc.CallOptions? options}) {
    return $createUnaryCall(_$setFlexProperties, request, options: options);
  }
}

@$pb.GrpcServiceName('dart_vm_service.DartVmService')
abstract class DartVmServiceBase extends $grpc.Service {
  $core.String get $name => 'dart_vm_service.DartVmService';

  DartVmServiceBase() {
    $addMethod($grpc.ServiceMethod<$0.ConnectRequest, $0.ConnectResponse>(
        'Connect',
        connect_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ConnectRequest.fromBuffer(value),
        ($0.ConnectResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleDebugPaint',
        toggleDebugPaint_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleRepaintRainbow',
        toggleRepaintRainbow_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'TogglePerformanceOverlay',
        togglePerformanceOverlay_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleBaselinePainting',
        toggleBaselinePainting_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleDebugBanner',
        toggleDebugBanner_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleStructuredErrors',
        toggleStructuredErrors_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleOversizedImages',
        toggleOversizedImages_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleDisablePhysicalShapeLayers',
        toggleDisablePhysicalShapeLayers_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleDisableOpacityLayers',
        toggleDisableOpacityLayers_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleProfileWidgetBuilds',
        toggleProfileWidgetBuilds_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleProfileUserWidgetBuilds',
        toggleProfileUserWidgetBuilds_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleProfileRenderObjectPaints',
        toggleProfileRenderObjectPaints_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleProfileRenderObjectLayouts',
        toggleProfileRenderObjectLayouts_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleProfilePlatformChannels',
        toggleProfilePlatformChannels_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleInspector',
        toggleInspector_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleTrackRebuildWidgets',
        toggleTrackRebuildWidgets_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ToggleRequest, $0.ToggleResponse>(
        'ToggleTrackRepaintWidgets',
        toggleTrackRepaintWidgets_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ToggleRequest.fromBuffer(value),
        ($0.ToggleResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ViewIdRequest, $0.DisplayRefreshRateResponse>(
        'GetDisplayRefreshRate',
        getDisplayRefreshRate_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ViewIdRequest.fromBuffer(value),
        ($0.DisplayRefreshRateResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.ListViewsResponse>(
        'ListViews',
        listViews_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.ListViewsResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
        'DumpWidgetTree',
        dumpWidgetTree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.TreeDumpResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
        'DumpLayerTree',
        dumpLayerTree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.TreeDumpResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
        'DumpRenderTree',
        dumpRenderTree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.TreeDumpResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
        'DumpSemanticsTreeInTraversalOrder',
        dumpSemanticsTreeInTraversalOrder_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.TreeDumpResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
        'DumpSemanticsTreeInInverseHitTestOrder',
        dumpSemanticsTreeInInverseHitTestOrder_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.TreeDumpResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.TreeDumpResponse>(
        'DumpFocusTree',
        dumpFocusTree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.TreeDumpResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.DoubleValueRequest, $0.GenericResponse>(
        'SetTimeDilation',
        setTimeDilation_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.DoubleValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.BoolValueRequest, $0.GenericResponse>(
        'DidSendFirstFrameEvent',
        didSendFirstFrameEvent_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.BoolValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'DidSendFirstFrameRasterizedEvent',
        didSendFirstFrameRasterizedEvent_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'EvictAssets',
        evictAssets_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.GenericResponse>(
        'Reassemble',
        reassemble_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.GenericResponse>(
        'ExitApp',
        exitApp_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'SetVmServiceUri',
        setVmServiceUri_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'SetDevToolsServerAddress',
        setDevToolsServerAddress_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'SetPlatformOverride',
        setPlatformOverride_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'SetBrightnessOverride',
        setBrightnessOverride_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringListRequest, $0.GenericResponse>(
        'SetPubRootDirectories',
        setPubRootDirectories_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringListRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringListRequest, $0.GenericResponse>(
        'AddPubRootDirectories',
        addPubRootDirectories_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringListRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringListRequest, $0.GenericResponse>(
        'RemovePubRootDirectories',
        removePubRootDirectories_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringListRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.StringListResponse>(
        'GetPubRootDirectories',
        getPubRootDirectories_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.StringListResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'TapWidgetByKey',
        tapWidgetByKey_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'TapWidgetByText',
        tapWidgetByText_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'TapWidgetByType',
        tapWidgetByType_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'TapWidgetByTooltip',
        tapWidgetByTooltip_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.AncestorDescendantRequest, $0.GenericResponse>(
        'TapWidgetByAncestorAndDescendant',
        tapWidgetByAncestorAndDescendant_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.AncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EnterTextRequest, $0.GenericResponse>(
        'EnterText',
        enterText_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EnterTextRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EnterTextKeyRequest, $0.GenericResponse>(
        'EnterTextByKey',
        enterTextByKey_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EnterTextKeyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EnterTextTypeRequest, $0.GenericResponse>(
        'EnterTextByType',
        enterTextByType_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EnterTextTypeRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EnterTextTextRequest, $0.GenericResponse>(
        'EnterTextByText',
        enterTextByText_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EnterTextTextRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EnterTextTooltipRequest, $0.GenericResponse>(
        'EnterTextByTooltip',
        enterTextByTooltip_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EnterTextTooltipRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EnterTextAncestorDescendantRequest, $0.GenericResponse>(
        'EnterTextByAncestorAndDescendant',
        enterTextByAncestorAndDescendant_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EnterTextAncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollDownByKey',
        scrollDownByKey_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollDownByType',
        scrollDownByType_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollDownByText',
        scrollDownByText_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollDownByTooltip',
        scrollDownByTooltip_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.AncestorDescendantRequest, $0.GenericResponse>(
        'ScrollDownByAncestorAndDescendant',
        scrollDownByAncestorAndDescendant_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.AncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollUpByKey',
        scrollUpByKey_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollUpByType',
        scrollUpByType_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollUpByText',
        scrollUpByText_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.StringValueRequest, $0.GenericResponse>(
        'ScrollUpByTooltip',
        scrollUpByTooltip_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.StringValueRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.AncestorDescendantRequest, $0.GenericResponse>(
        'ScrollUpByAncestorAndDescendant',
        scrollUpByAncestorAndDescendant_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.AncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollKeyRequest, $0.GenericResponse>(
        'ScrollDownByKeyExtended',
        scrollDownByKeyExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollKeyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollTypeRequest, $0.GenericResponse>(
        'ScrollDownByTypeExtended',
        scrollDownByTypeExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollTypeRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollTextRequest, $0.GenericResponse>(
        'ScrollDownByTextExtended',
        scrollDownByTextExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollTextRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollTooltipRequest, $0.GenericResponse>(
        'ScrollDownByTooltipExtended',
        scrollDownByTooltipExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollTooltipRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollAncestorDescendantRequest, $0.GenericResponse>(
        'ScrollDownByAncestorAndDescendantExtended',
        scrollDownByAncestorAndDescendantExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollAncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollKeyRequest, $0.GenericResponse>(
        'ScrollUpByKeyExtended',
        scrollUpByKeyExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollKeyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollTypeRequest, $0.GenericResponse>(
        'ScrollUpByTypeExtended',
        scrollUpByTypeExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollTypeRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollTextRequest, $0.GenericResponse>(
        'ScrollUpByTextExtended',
        scrollUpByTextExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollTextRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollTooltipRequest, $0.GenericResponse>(
        'ScrollUpByTooltipExtended',
        scrollUpByTooltipExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollTooltipRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollAncestorDescendantRequest, $0.GenericResponse>(
        'ScrollUpByAncestorAndDescendantExtended',
        scrollUpByAncestorAndDescendantExtended_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollAncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollIntoViewKeyRequest, $0.GenericResponse>(
        'ScrollIntoViewByKey',
        scrollIntoViewByKey_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollIntoViewKeyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollIntoViewTypeRequest, $0.GenericResponse>(
        'ScrollIntoViewByType',
        scrollIntoViewByType_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollIntoViewTypeRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollIntoViewTextRequest, $0.GenericResponse>(
        'ScrollIntoViewByText',
        scrollIntoViewByText_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollIntoViewTextRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollIntoViewTooltipRequest, $0.GenericResponse>(
        'ScrollIntoViewByTooltip',
        scrollIntoViewByTooltip_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollIntoViewTooltipRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScrollIntoViewAncestorDescendantRequest, $0.GenericResponse>(
        'ScrollIntoViewByAncestorAndDescendant',
        scrollIntoViewByAncestorAndDescendant_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScrollIntoViewAncestorDescendantRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.GenericResponse>(
        'IsWidgetTreeReady',
        isWidgetTreeReady_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.EmptyRequest, $0.GenericResponse>(
        'IsWidgetCreationTracked',
        isWidgetCreationTracked_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.EmptyRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
        'GetRootWidget',
        getRootWidget_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ObjectGroupRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
        'GetRootWidgetSummaryTree',
        getRootWidgetSummaryTree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ObjectGroupRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
        'GetRootWidgetSummaryTreeWithPreviews',
        getRootWidgetSummaryTreeWithPreviews_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ObjectGroupRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.SelectedWidgetRequest, $0.GenericResponse>(
        'GetSelectedWidget',
        getSelectedWidget_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.SelectedWidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.SelectedWidgetRequest, $0.GenericResponse>(
        'GetSelectedSummaryWidget',
        getSelectedSummaryWidget_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.SelectedWidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.SelectionByIdRequest, $0.GenericResponse>(
        'SetSelectionById',
        setSelectionById_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.SelectionByIdRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
        'DisposeAllGroups',
        disposeAllGroups_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ObjectGroupRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ObjectGroupRequest, $0.GenericResponse>(
        'DisposeGroup',
        disposeGroup_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ObjectGroupRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.DisposeIdRequest, $0.GenericResponse>(
        'DisposeId',
        disposeId_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.DisposeIdRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.WidgetRequest, $0.GenericResponse>(
        'GetParentChain',
        getParentChain_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.WidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.WidgetRequest, $0.GenericResponse>(
        'GetProperties',
        getProperties_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.WidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.WidgetRequest, $0.GenericResponse>(
        'GetChildren',
        getChildren_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.WidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.WidgetRequest, $0.GenericResponse>(
        'GetChildrenSummaryTree',
        getChildrenSummaryTree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.WidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.WidgetRequest, $0.GenericResponse>(
        'GetChildrenDetailsSubtree',
        getChildrenDetailsSubtree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.WidgetRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.DetailSubtreeRequest, $0.GenericResponse>(
        'GetDetailsSubtree',
        getDetailsSubtree_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.DetailSubtreeRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.ScreenshotRequest, $0.GenericResponse>(
        'Screenshot',
        screenshot_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.ScreenshotRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.LayoutExplorerRequest, $0.GenericResponse>(
        'GetLayoutExplorerNode',
        getLayoutExplorerNode_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.LayoutExplorerRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.FlexFitRequest, $0.GenericResponse>(
        'SetFlexFit',
        setFlexFit_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.FlexFitRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.FlexFactorRequest, $0.GenericResponse>(
        'SetFlexFactor',
        setFlexFactor_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.FlexFactorRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
    $addMethod($grpc.ServiceMethod<$0.FlexPropertiesRequest, $0.GenericResponse>(
        'SetFlexProperties',
        setFlexProperties_Pre,
        false,
        false,
        ($core.List<$core.int> value) => $0.FlexPropertiesRequest.fromBuffer(value),
        ($0.GenericResponse value) => value.writeToBuffer()));
  }

  $async.Future<$0.ConnectResponse> connect_Pre($grpc.ServiceCall $call, $async.Future<$0.ConnectRequest> $request) async {
    return connect($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleDebugPaint_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleDebugPaint($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleRepaintRainbow_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleRepaintRainbow($call, await $request);
  }

  $async.Future<$0.ToggleResponse> togglePerformanceOverlay_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return togglePerformanceOverlay($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleBaselinePainting_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleBaselinePainting($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleDebugBanner_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleDebugBanner($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleStructuredErrors_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleStructuredErrors($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleOversizedImages_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleOversizedImages($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleDisablePhysicalShapeLayers_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleDisablePhysicalShapeLayers($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleDisableOpacityLayers_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleDisableOpacityLayers($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleProfileWidgetBuilds_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleProfileWidgetBuilds($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleProfileUserWidgetBuilds_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleProfileUserWidgetBuilds($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleProfileRenderObjectPaints_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleProfileRenderObjectPaints($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleProfileRenderObjectLayouts_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleProfileRenderObjectLayouts($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleProfilePlatformChannels_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleProfilePlatformChannels($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleInspector_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleInspector($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleTrackRebuildWidgets_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleTrackRebuildWidgets($call, await $request);
  }

  $async.Future<$0.ToggleResponse> toggleTrackRepaintWidgets_Pre($grpc.ServiceCall $call, $async.Future<$0.ToggleRequest> $request) async {
    return toggleTrackRepaintWidgets($call, await $request);
  }

  $async.Future<$0.DisplayRefreshRateResponse> getDisplayRefreshRate_Pre($grpc.ServiceCall $call, $async.Future<$0.ViewIdRequest> $request) async {
    return getDisplayRefreshRate($call, await $request);
  }

  $async.Future<$0.ListViewsResponse> listViews_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return listViews($call, await $request);
  }

  $async.Future<$0.TreeDumpResponse> dumpWidgetTree_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return dumpWidgetTree($call, await $request);
  }

  $async.Future<$0.TreeDumpResponse> dumpLayerTree_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return dumpLayerTree($call, await $request);
  }

  $async.Future<$0.TreeDumpResponse> dumpRenderTree_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return dumpRenderTree($call, await $request);
  }

  $async.Future<$0.TreeDumpResponse> dumpSemanticsTreeInTraversalOrder_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return dumpSemanticsTreeInTraversalOrder($call, await $request);
  }

  $async.Future<$0.TreeDumpResponse> dumpSemanticsTreeInInverseHitTestOrder_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return dumpSemanticsTreeInInverseHitTestOrder($call, await $request);
  }

  $async.Future<$0.TreeDumpResponse> dumpFocusTree_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return dumpFocusTree($call, await $request);
  }

  $async.Future<$0.GenericResponse> setTimeDilation_Pre($grpc.ServiceCall $call, $async.Future<$0.DoubleValueRequest> $request) async {
    return setTimeDilation($call, await $request);
  }

  $async.Future<$0.GenericResponse> didSendFirstFrameEvent_Pre($grpc.ServiceCall $call, $async.Future<$0.BoolValueRequest> $request) async {
    return didSendFirstFrameEvent($call, await $request);
  }

  $async.Future<$0.GenericResponse> didSendFirstFrameRasterizedEvent_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return didSendFirstFrameRasterizedEvent($call, await $request);
  }

  $async.Future<$0.GenericResponse> evictAssets_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return evictAssets($call, await $request);
  }

  $async.Future<$0.GenericResponse> reassemble_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return reassemble($call, await $request);
  }

  $async.Future<$0.GenericResponse> exitApp_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return exitApp($call, await $request);
  }

  $async.Future<$0.GenericResponse> setVmServiceUri_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return setVmServiceUri($call, await $request);
  }

  $async.Future<$0.GenericResponse> setDevToolsServerAddress_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return setDevToolsServerAddress($call, await $request);
  }

  $async.Future<$0.GenericResponse> setPlatformOverride_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return setPlatformOverride($call, await $request);
  }

  $async.Future<$0.GenericResponse> setBrightnessOverride_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return setBrightnessOverride($call, await $request);
  }

  $async.Future<$0.GenericResponse> setPubRootDirectories_Pre($grpc.ServiceCall $call, $async.Future<$0.StringListRequest> $request) async {
    return setPubRootDirectories($call, await $request);
  }

  $async.Future<$0.GenericResponse> addPubRootDirectories_Pre($grpc.ServiceCall $call, $async.Future<$0.StringListRequest> $request) async {
    return addPubRootDirectories($call, await $request);
  }

  $async.Future<$0.GenericResponse> removePubRootDirectories_Pre($grpc.ServiceCall $call, $async.Future<$0.StringListRequest> $request) async {
    return removePubRootDirectories($call, await $request);
  }

  $async.Future<$0.StringListResponse> getPubRootDirectories_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return getPubRootDirectories($call, await $request);
  }

  $async.Future<$0.GenericResponse> tapWidgetByKey_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return tapWidgetByKey($call, await $request);
  }

  $async.Future<$0.GenericResponse> tapWidgetByText_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return tapWidgetByText($call, await $request);
  }

  $async.Future<$0.GenericResponse> tapWidgetByType_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return tapWidgetByType($call, await $request);
  }

  $async.Future<$0.GenericResponse> tapWidgetByTooltip_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return tapWidgetByTooltip($call, await $request);
  }

  $async.Future<$0.GenericResponse> tapWidgetByAncestorAndDescendant_Pre($grpc.ServiceCall $call, $async.Future<$0.AncestorDescendantRequest> $request) async {
    return tapWidgetByAncestorAndDescendant($call, await $request);
  }

  $async.Future<$0.GenericResponse> enterText_Pre($grpc.ServiceCall $call, $async.Future<$0.EnterTextRequest> $request) async {
    return enterText($call, await $request);
  }

  $async.Future<$0.GenericResponse> enterTextByKey_Pre($grpc.ServiceCall $call, $async.Future<$0.EnterTextKeyRequest> $request) async {
    return enterTextByKey($call, await $request);
  }

  $async.Future<$0.GenericResponse> enterTextByType_Pre($grpc.ServiceCall $call, $async.Future<$0.EnterTextTypeRequest> $request) async {
    return enterTextByType($call, await $request);
  }

  $async.Future<$0.GenericResponse> enterTextByText_Pre($grpc.ServiceCall $call, $async.Future<$0.EnterTextTextRequest> $request) async {
    return enterTextByText($call, await $request);
  }

  $async.Future<$0.GenericResponse> enterTextByTooltip_Pre($grpc.ServiceCall $call, $async.Future<$0.EnterTextTooltipRequest> $request) async {
    return enterTextByTooltip($call, await $request);
  }

  $async.Future<$0.GenericResponse> enterTextByAncestorAndDescendant_Pre($grpc.ServiceCall $call, $async.Future<$0.EnterTextAncestorDescendantRequest> $request) async {
    return enterTextByAncestorAndDescendant($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByKey_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollDownByKey($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByType_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollDownByType($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByText_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollDownByText($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByTooltip_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollDownByTooltip($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByAncestorAndDescendant_Pre($grpc.ServiceCall $call, $async.Future<$0.AncestorDescendantRequest> $request) async {
    return scrollDownByAncestorAndDescendant($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByKey_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollUpByKey($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByType_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollUpByType($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByText_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollUpByText($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByTooltip_Pre($grpc.ServiceCall $call, $async.Future<$0.StringValueRequest> $request) async {
    return scrollUpByTooltip($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByAncestorAndDescendant_Pre($grpc.ServiceCall $call, $async.Future<$0.AncestorDescendantRequest> $request) async {
    return scrollUpByAncestorAndDescendant($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByKeyExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollKeyRequest> $request) async {
    return scrollDownByKeyExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByTypeExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollTypeRequest> $request) async {
    return scrollDownByTypeExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByTextExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollTextRequest> $request) async {
    return scrollDownByTextExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByTooltipExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollTooltipRequest> $request) async {
    return scrollDownByTooltipExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollDownByAncestorAndDescendantExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollAncestorDescendantRequest> $request) async {
    return scrollDownByAncestorAndDescendantExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByKeyExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollKeyRequest> $request) async {
    return scrollUpByKeyExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByTypeExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollTypeRequest> $request) async {
    return scrollUpByTypeExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByTextExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollTextRequest> $request) async {
    return scrollUpByTextExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByTooltipExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollTooltipRequest> $request) async {
    return scrollUpByTooltipExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollUpByAncestorAndDescendantExtended_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollAncestorDescendantRequest> $request) async {
    return scrollUpByAncestorAndDescendantExtended($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollIntoViewByKey_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollIntoViewKeyRequest> $request) async {
    return scrollIntoViewByKey($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollIntoViewByType_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollIntoViewTypeRequest> $request) async {
    return scrollIntoViewByType($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollIntoViewByText_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollIntoViewTextRequest> $request) async {
    return scrollIntoViewByText($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollIntoViewByTooltip_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollIntoViewTooltipRequest> $request) async {
    return scrollIntoViewByTooltip($call, await $request);
  }

  $async.Future<$0.GenericResponse> scrollIntoViewByAncestorAndDescendant_Pre($grpc.ServiceCall $call, $async.Future<$0.ScrollIntoViewAncestorDescendantRequest> $request) async {
    return scrollIntoViewByAncestorAndDescendant($call, await $request);
  }

  $async.Future<$0.GenericResponse> isWidgetTreeReady_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return isWidgetTreeReady($call, await $request);
  }

  $async.Future<$0.GenericResponse> isWidgetCreationTracked_Pre($grpc.ServiceCall $call, $async.Future<$0.EmptyRequest> $request) async {
    return isWidgetCreationTracked($call, await $request);
  }

  $async.Future<$0.GenericResponse> getRootWidget_Pre($grpc.ServiceCall $call, $async.Future<$0.ObjectGroupRequest> $request) async {
    return getRootWidget($call, await $request);
  }

  $async.Future<$0.GenericResponse> getRootWidgetSummaryTree_Pre($grpc.ServiceCall $call, $async.Future<$0.ObjectGroupRequest> $request) async {
    return getRootWidgetSummaryTree($call, await $request);
  }

  $async.Future<$0.GenericResponse> getRootWidgetSummaryTreeWithPreviews_Pre($grpc.ServiceCall $call, $async.Future<$0.ObjectGroupRequest> $request) async {
    return getRootWidgetSummaryTreeWithPreviews($call, await $request);
  }

  $async.Future<$0.GenericResponse> getSelectedWidget_Pre($grpc.ServiceCall $call, $async.Future<$0.SelectedWidgetRequest> $request) async {
    return getSelectedWidget($call, await $request);
  }

  $async.Future<$0.GenericResponse> getSelectedSummaryWidget_Pre($grpc.ServiceCall $call, $async.Future<$0.SelectedWidgetRequest> $request) async {
    return getSelectedSummaryWidget($call, await $request);
  }

  $async.Future<$0.GenericResponse> setSelectionById_Pre($grpc.ServiceCall $call, $async.Future<$0.SelectionByIdRequest> $request) async {
    return setSelectionById($call, await $request);
  }

  $async.Future<$0.GenericResponse> disposeAllGroups_Pre($grpc.ServiceCall $call, $async.Future<$0.ObjectGroupRequest> $request) async {
    return disposeAllGroups($call, await $request);
  }

  $async.Future<$0.GenericResponse> disposeGroup_Pre($grpc.ServiceCall $call, $async.Future<$0.ObjectGroupRequest> $request) async {
    return disposeGroup($call, await $request);
  }

  $async.Future<$0.GenericResponse> disposeId_Pre($grpc.ServiceCall $call, $async.Future<$0.DisposeIdRequest> $request) async {
    return disposeId($call, await $request);
  }

  $async.Future<$0.GenericResponse> getParentChain_Pre($grpc.ServiceCall $call, $async.Future<$0.WidgetRequest> $request) async {
    return getParentChain($call, await $request);
  }

  $async.Future<$0.GenericResponse> getProperties_Pre($grpc.ServiceCall $call, $async.Future<$0.WidgetRequest> $request) async {
    return getProperties($call, await $request);
  }

  $async.Future<$0.GenericResponse> getChildren_Pre($grpc.ServiceCall $call, $async.Future<$0.WidgetRequest> $request) async {
    return getChildren($call, await $request);
  }

  $async.Future<$0.GenericResponse> getChildrenSummaryTree_Pre($grpc.ServiceCall $call, $async.Future<$0.WidgetRequest> $request) async {
    return getChildrenSummaryTree($call, await $request);
  }

  $async.Future<$0.GenericResponse> getChildrenDetailsSubtree_Pre($grpc.ServiceCall $call, $async.Future<$0.WidgetRequest> $request) async {
    return getChildrenDetailsSubtree($call, await $request);
  }

  $async.Future<$0.GenericResponse> getDetailsSubtree_Pre($grpc.ServiceCall $call, $async.Future<$0.DetailSubtreeRequest> $request) async {
    return getDetailsSubtree($call, await $request);
  }

  $async.Future<$0.GenericResponse> screenshot_Pre($grpc.ServiceCall $call, $async.Future<$0.ScreenshotRequest> $request) async {
    return screenshot($call, await $request);
  }

  $async.Future<$0.GenericResponse> getLayoutExplorerNode_Pre($grpc.ServiceCall $call, $async.Future<$0.LayoutExplorerRequest> $request) async {
    return getLayoutExplorerNode($call, await $request);
  }

  $async.Future<$0.GenericResponse> setFlexFit_Pre($grpc.ServiceCall $call, $async.Future<$0.FlexFitRequest> $request) async {
    return setFlexFit($call, await $request);
  }

  $async.Future<$0.GenericResponse> setFlexFactor_Pre($grpc.ServiceCall $call, $async.Future<$0.FlexFactorRequest> $request) async {
    return setFlexFactor($call, await $request);
  }

  $async.Future<$0.GenericResponse> setFlexProperties_Pre($grpc.ServiceCall $call, $async.Future<$0.FlexPropertiesRequest> $request) async {
    return setFlexProperties($call, await $request);
  }

  $async.Future<$0.ConnectResponse> connect($grpc.ServiceCall call, $0.ConnectRequest request);
  $async.Future<$0.ToggleResponse> toggleDebugPaint($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleRepaintRainbow($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> togglePerformanceOverlay($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleBaselinePainting($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleDebugBanner($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleStructuredErrors($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleOversizedImages($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleDisablePhysicalShapeLayers($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleDisableOpacityLayers($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleProfileWidgetBuilds($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleProfileUserWidgetBuilds($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleProfileRenderObjectPaints($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleProfileRenderObjectLayouts($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleProfilePlatformChannels($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleInspector($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleTrackRebuildWidgets($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.ToggleResponse> toggleTrackRepaintWidgets($grpc.ServiceCall call, $0.ToggleRequest request);
  $async.Future<$0.DisplayRefreshRateResponse> getDisplayRefreshRate($grpc.ServiceCall call, $0.ViewIdRequest request);
  $async.Future<$0.ListViewsResponse> listViews($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.TreeDumpResponse> dumpWidgetTree($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.TreeDumpResponse> dumpLayerTree($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.TreeDumpResponse> dumpRenderTree($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.TreeDumpResponse> dumpSemanticsTreeInTraversalOrder($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.TreeDumpResponse> dumpSemanticsTreeInInverseHitTestOrder($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.TreeDumpResponse> dumpFocusTree($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.GenericResponse> setTimeDilation($grpc.ServiceCall call, $0.DoubleValueRequest request);
  $async.Future<$0.GenericResponse> didSendFirstFrameEvent($grpc.ServiceCall call, $0.BoolValueRequest request);
  $async.Future<$0.GenericResponse> didSendFirstFrameRasterizedEvent($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> evictAssets($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> reassemble($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.GenericResponse> exitApp($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.GenericResponse> setVmServiceUri($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> setDevToolsServerAddress($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> setPlatformOverride($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> setBrightnessOverride($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> setPubRootDirectories($grpc.ServiceCall call, $0.StringListRequest request);
  $async.Future<$0.GenericResponse> addPubRootDirectories($grpc.ServiceCall call, $0.StringListRequest request);
  $async.Future<$0.GenericResponse> removePubRootDirectories($grpc.ServiceCall call, $0.StringListRequest request);
  $async.Future<$0.StringListResponse> getPubRootDirectories($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.GenericResponse> tapWidgetByKey($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> tapWidgetByText($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> tapWidgetByType($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> tapWidgetByTooltip($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> tapWidgetByAncestorAndDescendant($grpc.ServiceCall call, $0.AncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> enterText($grpc.ServiceCall call, $0.EnterTextRequest request);
  $async.Future<$0.GenericResponse> enterTextByKey($grpc.ServiceCall call, $0.EnterTextKeyRequest request);
  $async.Future<$0.GenericResponse> enterTextByType($grpc.ServiceCall call, $0.EnterTextTypeRequest request);
  $async.Future<$0.GenericResponse> enterTextByText($grpc.ServiceCall call, $0.EnterTextTextRequest request);
  $async.Future<$0.GenericResponse> enterTextByTooltip($grpc.ServiceCall call, $0.EnterTextTooltipRequest request);
  $async.Future<$0.GenericResponse> enterTextByAncestorAndDescendant($grpc.ServiceCall call, $0.EnterTextAncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> scrollDownByKey($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollDownByType($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollDownByText($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollDownByTooltip($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollDownByAncestorAndDescendant($grpc.ServiceCall call, $0.AncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> scrollUpByKey($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollUpByType($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollUpByText($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollUpByTooltip($grpc.ServiceCall call, $0.StringValueRequest request);
  $async.Future<$0.GenericResponse> scrollUpByAncestorAndDescendant($grpc.ServiceCall call, $0.AncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> scrollDownByKeyExtended($grpc.ServiceCall call, $0.ScrollKeyRequest request);
  $async.Future<$0.GenericResponse> scrollDownByTypeExtended($grpc.ServiceCall call, $0.ScrollTypeRequest request);
  $async.Future<$0.GenericResponse> scrollDownByTextExtended($grpc.ServiceCall call, $0.ScrollTextRequest request);
  $async.Future<$0.GenericResponse> scrollDownByTooltipExtended($grpc.ServiceCall call, $0.ScrollTooltipRequest request);
  $async.Future<$0.GenericResponse> scrollDownByAncestorAndDescendantExtended($grpc.ServiceCall call, $0.ScrollAncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> scrollUpByKeyExtended($grpc.ServiceCall call, $0.ScrollKeyRequest request);
  $async.Future<$0.GenericResponse> scrollUpByTypeExtended($grpc.ServiceCall call, $0.ScrollTypeRequest request);
  $async.Future<$0.GenericResponse> scrollUpByTextExtended($grpc.ServiceCall call, $0.ScrollTextRequest request);
  $async.Future<$0.GenericResponse> scrollUpByTooltipExtended($grpc.ServiceCall call, $0.ScrollTooltipRequest request);
  $async.Future<$0.GenericResponse> scrollUpByAncestorAndDescendantExtended($grpc.ServiceCall call, $0.ScrollAncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> scrollIntoViewByKey($grpc.ServiceCall call, $0.ScrollIntoViewKeyRequest request);
  $async.Future<$0.GenericResponse> scrollIntoViewByType($grpc.ServiceCall call, $0.ScrollIntoViewTypeRequest request);
  $async.Future<$0.GenericResponse> scrollIntoViewByText($grpc.ServiceCall call, $0.ScrollIntoViewTextRequest request);
  $async.Future<$0.GenericResponse> scrollIntoViewByTooltip($grpc.ServiceCall call, $0.ScrollIntoViewTooltipRequest request);
  $async.Future<$0.GenericResponse> scrollIntoViewByAncestorAndDescendant($grpc.ServiceCall call, $0.ScrollIntoViewAncestorDescendantRequest request);
  $async.Future<$0.GenericResponse> isWidgetTreeReady($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.GenericResponse> isWidgetCreationTracked($grpc.ServiceCall call, $0.EmptyRequest request);
  $async.Future<$0.GenericResponse> getRootWidget($grpc.ServiceCall call, $0.ObjectGroupRequest request);
  $async.Future<$0.GenericResponse> getRootWidgetSummaryTree($grpc.ServiceCall call, $0.ObjectGroupRequest request);
  $async.Future<$0.GenericResponse> getRootWidgetSummaryTreeWithPreviews($grpc.ServiceCall call, $0.ObjectGroupRequest request);
  $async.Future<$0.GenericResponse> getSelectedWidget($grpc.ServiceCall call, $0.SelectedWidgetRequest request);
  $async.Future<$0.GenericResponse> getSelectedSummaryWidget($grpc.ServiceCall call, $0.SelectedWidgetRequest request);
  $async.Future<$0.GenericResponse> setSelectionById($grpc.ServiceCall call, $0.SelectionByIdRequest request);
  $async.Future<$0.GenericResponse> disposeAllGroups($grpc.ServiceCall call, $0.ObjectGroupRequest request);
  $async.Future<$0.GenericResponse> disposeGroup($grpc.ServiceCall call, $0.ObjectGroupRequest request);
  $async.Future<$0.GenericResponse> disposeId($grpc.ServiceCall call, $0.DisposeIdRequest request);
  $async.Future<$0.GenericResponse> getParentChain($grpc.ServiceCall call, $0.WidgetRequest request);
  $async.Future<$0.GenericResponse> getProperties($grpc.ServiceCall call, $0.WidgetRequest request);
  $async.Future<$0.GenericResponse> getChildren($grpc.ServiceCall call, $0.WidgetRequest request);
  $async.Future<$0.GenericResponse> getChildrenSummaryTree($grpc.ServiceCall call, $0.WidgetRequest request);
  $async.Future<$0.GenericResponse> getChildrenDetailsSubtree($grpc.ServiceCall call, $0.WidgetRequest request);
  $async.Future<$0.GenericResponse> getDetailsSubtree($grpc.ServiceCall call, $0.DetailSubtreeRequest request);
  $async.Future<$0.GenericResponse> screenshot($grpc.ServiceCall call, $0.ScreenshotRequest request);
  $async.Future<$0.GenericResponse> getLayoutExplorerNode($grpc.ServiceCall call, $0.LayoutExplorerRequest request);
  $async.Future<$0.GenericResponse> setFlexFit($grpc.ServiceCall call, $0.FlexFitRequest request);
  $async.Future<$0.GenericResponse> setFlexFactor($grpc.ServiceCall call, $0.FlexFactorRequest request);
  $async.Future<$0.GenericResponse> setFlexProperties($grpc.ServiceCall call, $0.FlexPropertiesRequest request);
}
