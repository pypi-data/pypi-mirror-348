//
//  Generated code. Do not modify.
//  source: dart_vm_service.proto
//
// @dart = 3.3

// ignore_for_file: annotate_overrides, camel_case_types, comment_references
// ignore_for_file: constant_identifier_names, library_prefixes
// ignore_for_file: non_constant_identifier_names, prefer_final_fields
// ignore_for_file: unnecessary_import, unnecessary_this, unused_import

import 'dart:core' as $core;

import 'package:fixnum/fixnum.dart' as $fixnum;
import 'package:protobuf/protobuf.dart' as $pb;

export 'package:protobuf/protobuf.dart' show GeneratedMessageGenericExtensions;

/// Request to connect to a Flutter app
class ConnectRequest extends $pb.GeneratedMessage {
  factory ConnectRequest({
    $core.String? vmServiceUri,
  }) {
    final $result = create();
    if (vmServiceUri != null) {
      $result.vmServiceUri = vmServiceUri;
    }
    return $result;
  }
  ConnectRequest._() : super();
  factory ConnectRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ConnectRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ConnectRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'vmServiceUri')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ConnectRequest clone() => ConnectRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ConnectRequest copyWith(void Function(ConnectRequest) updates) => super.copyWith((message) => updates(message as ConnectRequest)) as ConnectRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ConnectRequest create() => ConnectRequest._();
  ConnectRequest createEmptyInstance() => create();
  static $pb.PbList<ConnectRequest> createRepeated() => $pb.PbList<ConnectRequest>();
  @$core.pragma('dart2js:noInline')
  static ConnectRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ConnectRequest>(create);
  static ConnectRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get vmServiceUri => $_getSZ(0);
  @$pb.TagNumber(1)
  set vmServiceUri($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasVmServiceUri() => $_has(0);
  @$pb.TagNumber(1)
  void clearVmServiceUri() => $_clearField(1);
}

/// Response from connect request
class ConnectResponse extends $pb.GeneratedMessage {
  factory ConnectResponse({
    $core.bool? success,
    $core.String? message,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    return $result;
  }
  ConnectResponse._() : super();
  factory ConnectResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ConnectResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ConnectResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ConnectResponse clone() => ConnectResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ConnectResponse copyWith(void Function(ConnectResponse) updates) => super.copyWith((message) => updates(message as ConnectResponse)) as ConnectResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ConnectResponse create() => ConnectResponse._();
  ConnectResponse createEmptyInstance() => create();
  static $pb.PbList<ConnectResponse> createRepeated() => $pb.PbList<ConnectResponse>();
  @$core.pragma('dart2js:noInline')
  static ConnectResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ConnectResponse>(create);
  static ConnectResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);
}

/// Empty request for methods that don't need parameters
class EmptyRequest extends $pb.GeneratedMessage {
  factory EmptyRequest() => create();
  EmptyRequest._() : super();
  factory EmptyRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EmptyRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EmptyRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EmptyRequest clone() => EmptyRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EmptyRequest copyWith(void Function(EmptyRequest) updates) => super.copyWith((message) => updates(message as EmptyRequest)) as EmptyRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EmptyRequest create() => EmptyRequest._();
  EmptyRequest createEmptyInstance() => create();
  static $pb.PbList<EmptyRequest> createRepeated() => $pb.PbList<EmptyRequest>();
  @$core.pragma('dart2js:noInline')
  static EmptyRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EmptyRequest>(create);
  static EmptyRequest? _defaultInstance;
}

/// Toggle request for features that can be enabled/disabled
class ToggleRequest extends $pb.GeneratedMessage {
  factory ToggleRequest({
    $core.bool? enable,
  }) {
    final $result = create();
    if (enable != null) {
      $result.enable = enable;
    }
    return $result;
  }
  ToggleRequest._() : super();
  factory ToggleRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ToggleRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ToggleRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'enable')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ToggleRequest clone() => ToggleRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ToggleRequest copyWith(void Function(ToggleRequest) updates) => super.copyWith((message) => updates(message as ToggleRequest)) as ToggleRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ToggleRequest create() => ToggleRequest._();
  ToggleRequest createEmptyInstance() => create();
  static $pb.PbList<ToggleRequest> createRepeated() => $pb.PbList<ToggleRequest>();
  @$core.pragma('dart2js:noInline')
  static ToggleRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ToggleRequest>(create);
  static ToggleRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get enable => $_getBF(0);
  @$pb.TagNumber(1)
  set enable($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasEnable() => $_has(0);
  @$pb.TagNumber(1)
  void clearEnable() => $_clearField(1);
}

/// Toggle response
class ToggleResponse extends $pb.GeneratedMessage {
  factory ToggleResponse({
    $core.bool? success,
    $core.String? message,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    return $result;
  }
  ToggleResponse._() : super();
  factory ToggleResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ToggleResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ToggleResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ToggleResponse clone() => ToggleResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ToggleResponse copyWith(void Function(ToggleResponse) updates) => super.copyWith((message) => updates(message as ToggleResponse)) as ToggleResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ToggleResponse create() => ToggleResponse._();
  ToggleResponse createEmptyInstance() => create();
  static $pb.PbList<ToggleResponse> createRepeated() => $pb.PbList<ToggleResponse>();
  @$core.pragma('dart2js:noInline')
  static ToggleResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ToggleResponse>(create);
  static ToggleResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);
}

/// Request with a view ID
class ViewIdRequest extends $pb.GeneratedMessage {
  factory ViewIdRequest({
    $core.String? viewId,
  }) {
    final $result = create();
    if (viewId != null) {
      $result.viewId = viewId;
    }
    return $result;
  }
  ViewIdRequest._() : super();
  factory ViewIdRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ViewIdRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ViewIdRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'viewId')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ViewIdRequest clone() => ViewIdRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ViewIdRequest copyWith(void Function(ViewIdRequest) updates) => super.copyWith((message) => updates(message as ViewIdRequest)) as ViewIdRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ViewIdRequest create() => ViewIdRequest._();
  ViewIdRequest createEmptyInstance() => create();
  static $pb.PbList<ViewIdRequest> createRepeated() => $pb.PbList<ViewIdRequest>();
  @$core.pragma('dart2js:noInline')
  static ViewIdRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ViewIdRequest>(create);
  static ViewIdRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get viewId => $_getSZ(0);
  @$pb.TagNumber(1)
  set viewId($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasViewId() => $_has(0);
  @$pb.TagNumber(1)
  void clearViewId() => $_clearField(1);
}

/// Response with display refresh rate
class DisplayRefreshRateResponse extends $pb.GeneratedMessage {
  factory DisplayRefreshRateResponse({
    $core.bool? success,
    $core.String? message,
    $core.double? refreshRate,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    if (refreshRate != null) {
      $result.refreshRate = refreshRate;
    }
    return $result;
  }
  DisplayRefreshRateResponse._() : super();
  factory DisplayRefreshRateResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory DisplayRefreshRateResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'DisplayRefreshRateResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..a<$core.double>(3, _omitFieldNames ? '' : 'refreshRate', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  DisplayRefreshRateResponse clone() => DisplayRefreshRateResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  DisplayRefreshRateResponse copyWith(void Function(DisplayRefreshRateResponse) updates) => super.copyWith((message) => updates(message as DisplayRefreshRateResponse)) as DisplayRefreshRateResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static DisplayRefreshRateResponse create() => DisplayRefreshRateResponse._();
  DisplayRefreshRateResponse createEmptyInstance() => create();
  static $pb.PbList<DisplayRefreshRateResponse> createRepeated() => $pb.PbList<DisplayRefreshRateResponse>();
  @$core.pragma('dart2js:noInline')
  static DisplayRefreshRateResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<DisplayRefreshRateResponse>(create);
  static DisplayRefreshRateResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get refreshRate => $_getN(2);
  @$pb.TagNumber(3)
  set refreshRate($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasRefreshRate() => $_has(2);
  @$pb.TagNumber(3)
  void clearRefreshRate() => $_clearField(3);
}

/// Response with views
class ListViewsResponse extends $pb.GeneratedMessage {
  factory ListViewsResponse({
    $core.bool? success,
    $core.String? message,
    $core.Iterable<$core.String>? views,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    if (views != null) {
      $result.views.addAll(views);
    }
    return $result;
  }
  ListViewsResponse._() : super();
  factory ListViewsResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ListViewsResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ListViewsResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..pPS(3, _omitFieldNames ? '' : 'views')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ListViewsResponse clone() => ListViewsResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ListViewsResponse copyWith(void Function(ListViewsResponse) updates) => super.copyWith((message) => updates(message as ListViewsResponse)) as ListViewsResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ListViewsResponse create() => ListViewsResponse._();
  ListViewsResponse createEmptyInstance() => create();
  static $pb.PbList<ListViewsResponse> createRepeated() => $pb.PbList<ListViewsResponse>();
  @$core.pragma('dart2js:noInline')
  static ListViewsResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ListViewsResponse>(create);
  static ListViewsResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);

  @$pb.TagNumber(3)
  $pb.PbList<$core.String> get views => $_getList(2);
}

/// Request with a double value
class DoubleValueRequest extends $pb.GeneratedMessage {
  factory DoubleValueRequest({
    $core.double? value,
  }) {
    final $result = create();
    if (value != null) {
      $result.value = value;
    }
    return $result;
  }
  DoubleValueRequest._() : super();
  factory DoubleValueRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory DoubleValueRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'DoubleValueRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..a<$core.double>(1, _omitFieldNames ? '' : 'value', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  DoubleValueRequest clone() => DoubleValueRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  DoubleValueRequest copyWith(void Function(DoubleValueRequest) updates) => super.copyWith((message) => updates(message as DoubleValueRequest)) as DoubleValueRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static DoubleValueRequest create() => DoubleValueRequest._();
  DoubleValueRequest createEmptyInstance() => create();
  static $pb.PbList<DoubleValueRequest> createRepeated() => $pb.PbList<DoubleValueRequest>();
  @$core.pragma('dart2js:noInline')
  static DoubleValueRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<DoubleValueRequest>(create);
  static DoubleValueRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.double get value => $_getN(0);
  @$pb.TagNumber(1)
  set value($core.double v) { $_setDouble(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearValue() => $_clearField(1);
}

/// Request with a boolean value
class BoolValueRequest extends $pb.GeneratedMessage {
  factory BoolValueRequest({
    $core.bool? value,
  }) {
    final $result = create();
    if (value != null) {
      $result.value = value;
    }
    return $result;
  }
  BoolValueRequest._() : super();
  factory BoolValueRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory BoolValueRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'BoolValueRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'value')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  BoolValueRequest clone() => BoolValueRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  BoolValueRequest copyWith(void Function(BoolValueRequest) updates) => super.copyWith((message) => updates(message as BoolValueRequest)) as BoolValueRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static BoolValueRequest create() => BoolValueRequest._();
  BoolValueRequest createEmptyInstance() => create();
  static $pb.PbList<BoolValueRequest> createRepeated() => $pb.PbList<BoolValueRequest>();
  @$core.pragma('dart2js:noInline')
  static BoolValueRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<BoolValueRequest>(create);
  static BoolValueRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get value => $_getBF(0);
  @$pb.TagNumber(1)
  set value($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearValue() => $_clearField(1);
}

/// Request with a string value
class StringValueRequest extends $pb.GeneratedMessage {
  factory StringValueRequest({
    $core.String? value,
  }) {
    final $result = create();
    if (value != null) {
      $result.value = value;
    }
    return $result;
  }
  StringValueRequest._() : super();
  factory StringValueRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory StringValueRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'StringValueRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'value')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  StringValueRequest clone() => StringValueRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  StringValueRequest copyWith(void Function(StringValueRequest) updates) => super.copyWith((message) => updates(message as StringValueRequest)) as StringValueRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static StringValueRequest create() => StringValueRequest._();
  StringValueRequest createEmptyInstance() => create();
  static $pb.PbList<StringValueRequest> createRepeated() => $pb.PbList<StringValueRequest>();
  @$core.pragma('dart2js:noInline')
  static StringValueRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<StringValueRequest>(create);
  static StringValueRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get value => $_getSZ(0);
  @$pb.TagNumber(1)
  set value($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearValue() => $_clearField(1);
}

/// Generic response message
class GenericResponse extends $pb.GeneratedMessage {
  factory GenericResponse({
    $core.bool? success,
    $core.String? message,
    $core.String? data,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    if (data != null) {
      $result.data = data;
    }
    return $result;
  }
  GenericResponse._() : super();
  factory GenericResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory GenericResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'GenericResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..aOS(3, _omitFieldNames ? '' : 'data')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  GenericResponse clone() => GenericResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  GenericResponse copyWith(void Function(GenericResponse) updates) => super.copyWith((message) => updates(message as GenericResponse)) as GenericResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static GenericResponse create() => GenericResponse._();
  GenericResponse createEmptyInstance() => create();
  static $pb.PbList<GenericResponse> createRepeated() => $pb.PbList<GenericResponse>();
  @$core.pragma('dart2js:noInline')
  static GenericResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<GenericResponse>(create);
  static GenericResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.String get data => $_getSZ(2);
  @$pb.TagNumber(3)
  set data($core.String v) { $_setString(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasData() => $_has(2);
  @$pb.TagNumber(3)
  void clearData() => $_clearField(3);
}

/// Request with a list of strings
class StringListRequest extends $pb.GeneratedMessage {
  factory StringListRequest({
    $core.Iterable<$core.String>? values,
  }) {
    final $result = create();
    if (values != null) {
      $result.values.addAll(values);
    }
    return $result;
  }
  StringListRequest._() : super();
  factory StringListRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory StringListRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'StringListRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..pPS(1, _omitFieldNames ? '' : 'values')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  StringListRequest clone() => StringListRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  StringListRequest copyWith(void Function(StringListRequest) updates) => super.copyWith((message) => updates(message as StringListRequest)) as StringListRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static StringListRequest create() => StringListRequest._();
  StringListRequest createEmptyInstance() => create();
  static $pb.PbList<StringListRequest> createRepeated() => $pb.PbList<StringListRequest>();
  @$core.pragma('dart2js:noInline')
  static StringListRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<StringListRequest>(create);
  static StringListRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $pb.PbList<$core.String> get values => $_getList(0);
}

/// Response with a list of strings
class StringListResponse extends $pb.GeneratedMessage {
  factory StringListResponse({
    $core.bool? success,
    $core.String? message,
    $core.Iterable<$core.String>? values,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    if (values != null) {
      $result.values.addAll(values);
    }
    return $result;
  }
  StringListResponse._() : super();
  factory StringListResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory StringListResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'StringListResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..pPS(3, _omitFieldNames ? '' : 'values')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  StringListResponse clone() => StringListResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  StringListResponse copyWith(void Function(StringListResponse) updates) => super.copyWith((message) => updates(message as StringListResponse)) as StringListResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static StringListResponse create() => StringListResponse._();
  StringListResponse createEmptyInstance() => create();
  static $pb.PbList<StringListResponse> createRepeated() => $pb.PbList<StringListResponse>();
  @$core.pragma('dart2js:noInline')
  static StringListResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<StringListResponse>(create);
  static StringListResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);

  @$pb.TagNumber(3)
  $pb.PbList<$core.String> get values => $_getList(2);
}

/// Request for entering text
class EnterTextRequest extends $pb.GeneratedMessage {
  factory EnterTextRequest({
    $core.String? keyValue,
    $core.String? text,
  }) {
    final $result = create();
    if (keyValue != null) {
      $result.keyValue = keyValue;
    }
    if (text != null) {
      $result.text = text;
    }
    return $result;
  }
  EnterTextRequest._() : super();
  factory EnterTextRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EnterTextRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EnterTextRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'keyValue')
    ..aOS(2, _omitFieldNames ? '' : 'text')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EnterTextRequest clone() => EnterTextRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EnterTextRequest copyWith(void Function(EnterTextRequest) updates) => super.copyWith((message) => updates(message as EnterTextRequest)) as EnterTextRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EnterTextRequest create() => EnterTextRequest._();
  EnterTextRequest createEmptyInstance() => create();
  static $pb.PbList<EnterTextRequest> createRepeated() => $pb.PbList<EnterTextRequest>();
  @$core.pragma('dart2js:noInline')
  static EnterTextRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EnterTextRequest>(create);
  static EnterTextRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get keyValue => $_getSZ(0);
  @$pb.TagNumber(1)
  set keyValue($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasKeyValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearKeyValue() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get text => $_getSZ(1);
  @$pb.TagNumber(2)
  set text($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasText() => $_has(1);
  @$pb.TagNumber(2)
  void clearText() => $_clearField(2);
}

/// Request for ancestor/descendant widget tapping
class AncestorDescendantRequest extends $pb.GeneratedMessage {
  factory AncestorDescendantRequest({
    $core.String? ancestorType,
    $core.String? descendantType,
  }) {
    final $result = create();
    if (ancestorType != null) {
      $result.ancestorType = ancestorType;
    }
    if (descendantType != null) {
      $result.descendantType = descendantType;
    }
    return $result;
  }
  AncestorDescendantRequest._() : super();
  factory AncestorDescendantRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory AncestorDescendantRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'AncestorDescendantRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'ancestorType')
    ..aOS(2, _omitFieldNames ? '' : 'descendantType')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  AncestorDescendantRequest clone() => AncestorDescendantRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  AncestorDescendantRequest copyWith(void Function(AncestorDescendantRequest) updates) => super.copyWith((message) => updates(message as AncestorDescendantRequest)) as AncestorDescendantRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static AncestorDescendantRequest create() => AncestorDescendantRequest._();
  AncestorDescendantRequest createEmptyInstance() => create();
  static $pb.PbList<AncestorDescendantRequest> createRepeated() => $pb.PbList<AncestorDescendantRequest>();
  @$core.pragma('dart2js:noInline')
  static AncestorDescendantRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<AncestorDescendantRequest>(create);
  static AncestorDescendantRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get ancestorType => $_getSZ(0);
  @$pb.TagNumber(1)
  set ancestorType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasAncestorType() => $_has(0);
  @$pb.TagNumber(1)
  void clearAncestorType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get descendantType => $_getSZ(1);
  @$pb.TagNumber(2)
  set descendantType($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDescendantType() => $_has(1);
  @$pb.TagNumber(2)
  void clearDescendantType() => $_clearField(2);
}

/// Tree dump response
class TreeDumpResponse extends $pb.GeneratedMessage {
  factory TreeDumpResponse({
    $core.bool? success,
    $core.String? message,
    $core.String? treeDump,
  }) {
    final $result = create();
    if (success != null) {
      $result.success = success;
    }
    if (message != null) {
      $result.message = message;
    }
    if (treeDump != null) {
      $result.treeDump = treeDump;
    }
    return $result;
  }
  TreeDumpResponse._() : super();
  factory TreeDumpResponse.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory TreeDumpResponse.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'TreeDumpResponse', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOB(1, _omitFieldNames ? '' : 'success')
    ..aOS(2, _omitFieldNames ? '' : 'message')
    ..aOS(3, _omitFieldNames ? '' : 'treeDump')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  TreeDumpResponse clone() => TreeDumpResponse()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  TreeDumpResponse copyWith(void Function(TreeDumpResponse) updates) => super.copyWith((message) => updates(message as TreeDumpResponse)) as TreeDumpResponse;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static TreeDumpResponse create() => TreeDumpResponse._();
  TreeDumpResponse createEmptyInstance() => create();
  static $pb.PbList<TreeDumpResponse> createRepeated() => $pb.PbList<TreeDumpResponse>();
  @$core.pragma('dart2js:noInline')
  static TreeDumpResponse getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<TreeDumpResponse>(create);
  static TreeDumpResponse? _defaultInstance;

  @$pb.TagNumber(1)
  $core.bool get success => $_getBF(0);
  @$pb.TagNumber(1)
  set success($core.bool v) { $_setBool(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasSuccess() => $_has(0);
  @$pb.TagNumber(1)
  void clearSuccess() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get message => $_getSZ(1);
  @$pb.TagNumber(2)
  set message($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMessage() => $_has(1);
  @$pb.TagNumber(2)
  void clearMessage() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.String get treeDump => $_getSZ(2);
  @$pb.TagNumber(3)
  set treeDump($core.String v) { $_setString(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasTreeDump() => $_has(2);
  @$pb.TagNumber(3)
  void clearTreeDump() => $_clearField(3);
}

/// Request with object group
class ObjectGroupRequest extends $pb.GeneratedMessage {
  factory ObjectGroupRequest({
    $core.String? objectGroup,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    return $result;
  }
  ObjectGroupRequest._() : super();
  factory ObjectGroupRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ObjectGroupRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ObjectGroupRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ObjectGroupRequest clone() => ObjectGroupRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ObjectGroupRequest copyWith(void Function(ObjectGroupRequest) updates) => super.copyWith((message) => updates(message as ObjectGroupRequest)) as ObjectGroupRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ObjectGroupRequest create() => ObjectGroupRequest._();
  ObjectGroupRequest createEmptyInstance() => create();
  static $pb.PbList<ObjectGroupRequest> createRepeated() => $pb.PbList<ObjectGroupRequest>();
  @$core.pragma('dart2js:noInline')
  static ObjectGroupRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ObjectGroupRequest>(create);
  static ObjectGroupRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);
}

/// Request for selected widget
class SelectedWidgetRequest extends $pb.GeneratedMessage {
  factory SelectedWidgetRequest({
    $core.String? objectGroup,
    $core.String? previousSelectionId,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    if (previousSelectionId != null) {
      $result.previousSelectionId = previousSelectionId;
    }
    return $result;
  }
  SelectedWidgetRequest._() : super();
  factory SelectedWidgetRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory SelectedWidgetRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'SelectedWidgetRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..aOS(2, _omitFieldNames ? '' : 'previousSelectionId')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  SelectedWidgetRequest clone() => SelectedWidgetRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  SelectedWidgetRequest copyWith(void Function(SelectedWidgetRequest) updates) => super.copyWith((message) => updates(message as SelectedWidgetRequest)) as SelectedWidgetRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static SelectedWidgetRequest create() => SelectedWidgetRequest._();
  SelectedWidgetRequest createEmptyInstance() => create();
  static $pb.PbList<SelectedWidgetRequest> createRepeated() => $pb.PbList<SelectedWidgetRequest>();
  @$core.pragma('dart2js:noInline')
  static SelectedWidgetRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<SelectedWidgetRequest>(create);
  static SelectedWidgetRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get previousSelectionId => $_getSZ(1);
  @$pb.TagNumber(2)
  set previousSelectionId($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasPreviousSelectionId() => $_has(1);
  @$pb.TagNumber(2)
  void clearPreviousSelectionId() => $_clearField(2);
}

/// Request for selection by ID
class SelectionByIdRequest extends $pb.GeneratedMessage {
  factory SelectionByIdRequest({
    $core.String? objectGroup,
    $core.String? objectId,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    if (objectId != null) {
      $result.objectId = objectId;
    }
    return $result;
  }
  SelectionByIdRequest._() : super();
  factory SelectionByIdRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory SelectionByIdRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'SelectionByIdRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..aOS(2, _omitFieldNames ? '' : 'objectId')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  SelectionByIdRequest clone() => SelectionByIdRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  SelectionByIdRequest copyWith(void Function(SelectionByIdRequest) updates) => super.copyWith((message) => updates(message as SelectionByIdRequest)) as SelectionByIdRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static SelectionByIdRequest create() => SelectionByIdRequest._();
  SelectionByIdRequest createEmptyInstance() => create();
  static $pb.PbList<SelectionByIdRequest> createRepeated() => $pb.PbList<SelectionByIdRequest>();
  @$core.pragma('dart2js:noInline')
  static SelectionByIdRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<SelectionByIdRequest>(create);
  static SelectionByIdRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get objectId => $_getSZ(1);
  @$pb.TagNumber(2)
  set objectId($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasObjectId() => $_has(1);
  @$pb.TagNumber(2)
  void clearObjectId() => $_clearField(2);
}

/// Request for disposing an object ID
class DisposeIdRequest extends $pb.GeneratedMessage {
  factory DisposeIdRequest({
    $core.String? objectGroup,
    $core.String? objectId,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    if (objectId != null) {
      $result.objectId = objectId;
    }
    return $result;
  }
  DisposeIdRequest._() : super();
  factory DisposeIdRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory DisposeIdRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'DisposeIdRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..aOS(2, _omitFieldNames ? '' : 'objectId')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  DisposeIdRequest clone() => DisposeIdRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  DisposeIdRequest copyWith(void Function(DisposeIdRequest) updates) => super.copyWith((message) => updates(message as DisposeIdRequest)) as DisposeIdRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static DisposeIdRequest create() => DisposeIdRequest._();
  DisposeIdRequest createEmptyInstance() => create();
  static $pb.PbList<DisposeIdRequest> createRepeated() => $pb.PbList<DisposeIdRequest>();
  @$core.pragma('dart2js:noInline')
  static DisposeIdRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<DisposeIdRequest>(create);
  static DisposeIdRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get objectId => $_getSZ(1);
  @$pb.TagNumber(2)
  set objectId($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasObjectId() => $_has(1);
  @$pb.TagNumber(2)
  void clearObjectId() => $_clearField(2);
}

/// Request for widget operations
class WidgetRequest extends $pb.GeneratedMessage {
  factory WidgetRequest({
    $core.String? objectGroup,
    $core.String? widgetId,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    return $result;
  }
  WidgetRequest._() : super();
  factory WidgetRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory WidgetRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'WidgetRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..aOS(2, _omitFieldNames ? '' : 'widgetId')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  WidgetRequest clone() => WidgetRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  WidgetRequest copyWith(void Function(WidgetRequest) updates) => super.copyWith((message) => updates(message as WidgetRequest)) as WidgetRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static WidgetRequest create() => WidgetRequest._();
  WidgetRequest createEmptyInstance() => create();
  static $pb.PbList<WidgetRequest> createRepeated() => $pb.PbList<WidgetRequest>();
  @$core.pragma('dart2js:noInline')
  static WidgetRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<WidgetRequest>(create);
  static WidgetRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get widgetId => $_getSZ(1);
  @$pb.TagNumber(2)
  set widgetId($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasWidgetId() => $_has(1);
  @$pb.TagNumber(2)
  void clearWidgetId() => $_clearField(2);
}

/// Request for detailed subtree
class DetailSubtreeRequest extends $pb.GeneratedMessage {
  factory DetailSubtreeRequest({
    $core.String? objectGroup,
    $core.String? widgetId,
    $core.int? subtreeDepth,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    if (subtreeDepth != null) {
      $result.subtreeDepth = subtreeDepth;
    }
    return $result;
  }
  DetailSubtreeRequest._() : super();
  factory DetailSubtreeRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory DetailSubtreeRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'DetailSubtreeRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..aOS(2, _omitFieldNames ? '' : 'widgetId')
    ..a<$core.int>(3, _omitFieldNames ? '' : 'subtreeDepth', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  DetailSubtreeRequest clone() => DetailSubtreeRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  DetailSubtreeRequest copyWith(void Function(DetailSubtreeRequest) updates) => super.copyWith((message) => updates(message as DetailSubtreeRequest)) as DetailSubtreeRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static DetailSubtreeRequest create() => DetailSubtreeRequest._();
  DetailSubtreeRequest createEmptyInstance() => create();
  static $pb.PbList<DetailSubtreeRequest> createRepeated() => $pb.PbList<DetailSubtreeRequest>();
  @$core.pragma('dart2js:noInline')
  static DetailSubtreeRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<DetailSubtreeRequest>(create);
  static DetailSubtreeRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get widgetId => $_getSZ(1);
  @$pb.TagNumber(2)
  set widgetId($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasWidgetId() => $_has(1);
  @$pb.TagNumber(2)
  void clearWidgetId() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.int get subtreeDepth => $_getIZ(2);
  @$pb.TagNumber(3)
  set subtreeDepth($core.int v) { $_setSignedInt32(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasSubtreeDepth() => $_has(2);
  @$pb.TagNumber(3)
  void clearSubtreeDepth() => $_clearField(3);
}

/// Request for screenshot
class ScreenshotRequest extends $pb.GeneratedMessage {
  factory ScreenshotRequest({
    $core.String? widgetId,
    $core.double? width,
    $core.double? height,
    $core.double? margin,
    $core.double? maxPixelRatio,
    $core.bool? debugPaint,
  }) {
    final $result = create();
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    if (width != null) {
      $result.width = width;
    }
    if (height != null) {
      $result.height = height;
    }
    if (margin != null) {
      $result.margin = margin;
    }
    if (maxPixelRatio != null) {
      $result.maxPixelRatio = maxPixelRatio;
    }
    if (debugPaint != null) {
      $result.debugPaint = debugPaint;
    }
    return $result;
  }
  ScreenshotRequest._() : super();
  factory ScreenshotRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScreenshotRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScreenshotRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetId')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'width', $pb.PbFieldType.OD)
    ..a<$core.double>(3, _omitFieldNames ? '' : 'height', $pb.PbFieldType.OD)
    ..a<$core.double>(4, _omitFieldNames ? '' : 'margin', $pb.PbFieldType.OD)
    ..a<$core.double>(5, _omitFieldNames ? '' : 'maxPixelRatio', $pb.PbFieldType.OD)
    ..aOB(6, _omitFieldNames ? '' : 'debugPaint')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScreenshotRequest clone() => ScreenshotRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScreenshotRequest copyWith(void Function(ScreenshotRequest) updates) => super.copyWith((message) => updates(message as ScreenshotRequest)) as ScreenshotRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScreenshotRequest create() => ScreenshotRequest._();
  ScreenshotRequest createEmptyInstance() => create();
  static $pb.PbList<ScreenshotRequest> createRepeated() => $pb.PbList<ScreenshotRequest>();
  @$core.pragma('dart2js:noInline')
  static ScreenshotRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScreenshotRequest>(create);
  static ScreenshotRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetId => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetId($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetId() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetId() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get width => $_getN(1);
  @$pb.TagNumber(2)
  set width($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasWidth() => $_has(1);
  @$pb.TagNumber(2)
  void clearWidth() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get height => $_getN(2);
  @$pb.TagNumber(3)
  set height($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasHeight() => $_has(2);
  @$pb.TagNumber(3)
  void clearHeight() => $_clearField(3);

  @$pb.TagNumber(4)
  $core.double get margin => $_getN(3);
  @$pb.TagNumber(4)
  set margin($core.double v) { $_setDouble(3, v); }
  @$pb.TagNumber(4)
  $core.bool hasMargin() => $_has(3);
  @$pb.TagNumber(4)
  void clearMargin() => $_clearField(4);

  @$pb.TagNumber(5)
  $core.double get maxPixelRatio => $_getN(4);
  @$pb.TagNumber(5)
  set maxPixelRatio($core.double v) { $_setDouble(4, v); }
  @$pb.TagNumber(5)
  $core.bool hasMaxPixelRatio() => $_has(4);
  @$pb.TagNumber(5)
  void clearMaxPixelRatio() => $_clearField(5);

  @$pb.TagNumber(6)
  $core.bool get debugPaint => $_getBF(5);
  @$pb.TagNumber(6)
  set debugPaint($core.bool v) { $_setBool(5, v); }
  @$pb.TagNumber(6)
  $core.bool hasDebugPaint() => $_has(5);
  @$pb.TagNumber(6)
  void clearDebugPaint() => $_clearField(6);
}

/// Request for layout explorer
class LayoutExplorerRequest extends $pb.GeneratedMessage {
  factory LayoutExplorerRequest({
    $core.String? objectGroup,
    $core.String? widgetId,
    $core.int? subtreeDepth,
  }) {
    final $result = create();
    if (objectGroup != null) {
      $result.objectGroup = objectGroup;
    }
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    if (subtreeDepth != null) {
      $result.subtreeDepth = subtreeDepth;
    }
    return $result;
  }
  LayoutExplorerRequest._() : super();
  factory LayoutExplorerRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory LayoutExplorerRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'LayoutExplorerRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'objectGroup')
    ..aOS(2, _omitFieldNames ? '' : 'widgetId')
    ..a<$core.int>(3, _omitFieldNames ? '' : 'subtreeDepth', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  LayoutExplorerRequest clone() => LayoutExplorerRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  LayoutExplorerRequest copyWith(void Function(LayoutExplorerRequest) updates) => super.copyWith((message) => updates(message as LayoutExplorerRequest)) as LayoutExplorerRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static LayoutExplorerRequest create() => LayoutExplorerRequest._();
  LayoutExplorerRequest createEmptyInstance() => create();
  static $pb.PbList<LayoutExplorerRequest> createRepeated() => $pb.PbList<LayoutExplorerRequest>();
  @$core.pragma('dart2js:noInline')
  static LayoutExplorerRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<LayoutExplorerRequest>(create);
  static LayoutExplorerRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get objectGroup => $_getSZ(0);
  @$pb.TagNumber(1)
  set objectGroup($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasObjectGroup() => $_has(0);
  @$pb.TagNumber(1)
  void clearObjectGroup() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get widgetId => $_getSZ(1);
  @$pb.TagNumber(2)
  set widgetId($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasWidgetId() => $_has(1);
  @$pb.TagNumber(2)
  void clearWidgetId() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.int get subtreeDepth => $_getIZ(2);
  @$pb.TagNumber(3)
  set subtreeDepth($core.int v) { $_setSignedInt32(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasSubtreeDepth() => $_has(2);
  @$pb.TagNumber(3)
  void clearSubtreeDepth() => $_clearField(3);
}

/// Request for flex fit
class FlexFitRequest extends $pb.GeneratedMessage {
  factory FlexFitRequest({
    $core.String? widgetId,
    $core.String? flexFit,
  }) {
    final $result = create();
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    if (flexFit != null) {
      $result.flexFit = flexFit;
    }
    return $result;
  }
  FlexFitRequest._() : super();
  factory FlexFitRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory FlexFitRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'FlexFitRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetId')
    ..aOS(2, _omitFieldNames ? '' : 'flexFit')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  FlexFitRequest clone() => FlexFitRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  FlexFitRequest copyWith(void Function(FlexFitRequest) updates) => super.copyWith((message) => updates(message as FlexFitRequest)) as FlexFitRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static FlexFitRequest create() => FlexFitRequest._();
  FlexFitRequest createEmptyInstance() => create();
  static $pb.PbList<FlexFitRequest> createRepeated() => $pb.PbList<FlexFitRequest>();
  @$core.pragma('dart2js:noInline')
  static FlexFitRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<FlexFitRequest>(create);
  static FlexFitRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetId => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetId($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetId() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetId() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get flexFit => $_getSZ(1);
  @$pb.TagNumber(2)
  set flexFit($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasFlexFit() => $_has(1);
  @$pb.TagNumber(2)
  void clearFlexFit() => $_clearField(2);
}

/// Request for flex factor
class FlexFactorRequest extends $pb.GeneratedMessage {
  factory FlexFactorRequest({
    $core.String? widgetId,
    $core.int? flexFactor,
  }) {
    final $result = create();
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    if (flexFactor != null) {
      $result.flexFactor = flexFactor;
    }
    return $result;
  }
  FlexFactorRequest._() : super();
  factory FlexFactorRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory FlexFactorRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'FlexFactorRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetId')
    ..a<$core.int>(2, _omitFieldNames ? '' : 'flexFactor', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  FlexFactorRequest clone() => FlexFactorRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  FlexFactorRequest copyWith(void Function(FlexFactorRequest) updates) => super.copyWith((message) => updates(message as FlexFactorRequest)) as FlexFactorRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static FlexFactorRequest create() => FlexFactorRequest._();
  FlexFactorRequest createEmptyInstance() => create();
  static $pb.PbList<FlexFactorRequest> createRepeated() => $pb.PbList<FlexFactorRequest>();
  @$core.pragma('dart2js:noInline')
  static FlexFactorRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<FlexFactorRequest>(create);
  static FlexFactorRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetId => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetId($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetId() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetId() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.int get flexFactor => $_getIZ(1);
  @$pb.TagNumber(2)
  set flexFactor($core.int v) { $_setSignedInt32(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasFlexFactor() => $_has(1);
  @$pb.TagNumber(2)
  void clearFlexFactor() => $_clearField(2);
}

/// Request for flex properties
class FlexPropertiesRequest extends $pb.GeneratedMessage {
  factory FlexPropertiesRequest({
    $core.String? widgetId,
    $core.String? mainAxisAlignment,
    $core.String? crossAxisAlignment,
  }) {
    final $result = create();
    if (widgetId != null) {
      $result.widgetId = widgetId;
    }
    if (mainAxisAlignment != null) {
      $result.mainAxisAlignment = mainAxisAlignment;
    }
    if (crossAxisAlignment != null) {
      $result.crossAxisAlignment = crossAxisAlignment;
    }
    return $result;
  }
  FlexPropertiesRequest._() : super();
  factory FlexPropertiesRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory FlexPropertiesRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'FlexPropertiesRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetId')
    ..aOS(2, _omitFieldNames ? '' : 'mainAxisAlignment')
    ..aOS(3, _omitFieldNames ? '' : 'crossAxisAlignment')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  FlexPropertiesRequest clone() => FlexPropertiesRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  FlexPropertiesRequest copyWith(void Function(FlexPropertiesRequest) updates) => super.copyWith((message) => updates(message as FlexPropertiesRequest)) as FlexPropertiesRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static FlexPropertiesRequest create() => FlexPropertiesRequest._();
  FlexPropertiesRequest createEmptyInstance() => create();
  static $pb.PbList<FlexPropertiesRequest> createRepeated() => $pb.PbList<FlexPropertiesRequest>();
  @$core.pragma('dart2js:noInline')
  static FlexPropertiesRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<FlexPropertiesRequest>(create);
  static FlexPropertiesRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetId => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetId($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetId() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetId() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get mainAxisAlignment => $_getSZ(1);
  @$pb.TagNumber(2)
  set mainAxisAlignment($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasMainAxisAlignment() => $_has(1);
  @$pb.TagNumber(2)
  void clearMainAxisAlignment() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.String get crossAxisAlignment => $_getSZ(2);
  @$pb.TagNumber(3)
  set crossAxisAlignment($core.String v) { $_setString(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasCrossAxisAlignment() => $_has(2);
  @$pb.TagNumber(3)
  void clearCrossAxisAlignment() => $_clearField(3);
}

/// Request for entering text by key
class EnterTextKeyRequest extends $pb.GeneratedMessage {
  factory EnterTextKeyRequest({
    $core.String? keyValue,
    $core.String? text,
  }) {
    final $result = create();
    if (keyValue != null) {
      $result.keyValue = keyValue;
    }
    if (text != null) {
      $result.text = text;
    }
    return $result;
  }
  EnterTextKeyRequest._() : super();
  factory EnterTextKeyRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EnterTextKeyRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EnterTextKeyRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'keyValue')
    ..aOS(2, _omitFieldNames ? '' : 'text')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EnterTextKeyRequest clone() => EnterTextKeyRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EnterTextKeyRequest copyWith(void Function(EnterTextKeyRequest) updates) => super.copyWith((message) => updates(message as EnterTextKeyRequest)) as EnterTextKeyRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EnterTextKeyRequest create() => EnterTextKeyRequest._();
  EnterTextKeyRequest createEmptyInstance() => create();
  static $pb.PbList<EnterTextKeyRequest> createRepeated() => $pb.PbList<EnterTextKeyRequest>();
  @$core.pragma('dart2js:noInline')
  static EnterTextKeyRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EnterTextKeyRequest>(create);
  static EnterTextKeyRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get keyValue => $_getSZ(0);
  @$pb.TagNumber(1)
  set keyValue($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasKeyValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearKeyValue() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get text => $_getSZ(1);
  @$pb.TagNumber(2)
  set text($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasText() => $_has(1);
  @$pb.TagNumber(2)
  void clearText() => $_clearField(2);
}

/// Request for entering text by type
class EnterTextTypeRequest extends $pb.GeneratedMessage {
  factory EnterTextTypeRequest({
    $core.String? widgetType,
    $core.String? text,
  }) {
    final $result = create();
    if (widgetType != null) {
      $result.widgetType = widgetType;
    }
    if (text != null) {
      $result.text = text;
    }
    return $result;
  }
  EnterTextTypeRequest._() : super();
  factory EnterTextTypeRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EnterTextTypeRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EnterTextTypeRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetType')
    ..aOS(2, _omitFieldNames ? '' : 'text')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EnterTextTypeRequest clone() => EnterTextTypeRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EnterTextTypeRequest copyWith(void Function(EnterTextTypeRequest) updates) => super.copyWith((message) => updates(message as EnterTextTypeRequest)) as EnterTextTypeRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EnterTextTypeRequest create() => EnterTextTypeRequest._();
  EnterTextTypeRequest createEmptyInstance() => create();
  static $pb.PbList<EnterTextTypeRequest> createRepeated() => $pb.PbList<EnterTextTypeRequest>();
  @$core.pragma('dart2js:noInline')
  static EnterTextTypeRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EnterTextTypeRequest>(create);
  static EnterTextTypeRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetType => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetType() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get text => $_getSZ(1);
  @$pb.TagNumber(2)
  set text($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasText() => $_has(1);
  @$pb.TagNumber(2)
  void clearText() => $_clearField(2);
}

/// Request for entering text by text
class EnterTextTextRequest extends $pb.GeneratedMessage {
  factory EnterTextTextRequest({
    $core.String? widgetText,
    $core.String? text,
  }) {
    final $result = create();
    if (widgetText != null) {
      $result.widgetText = widgetText;
    }
    if (text != null) {
      $result.text = text;
    }
    return $result;
  }
  EnterTextTextRequest._() : super();
  factory EnterTextTextRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EnterTextTextRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EnterTextTextRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetText')
    ..aOS(2, _omitFieldNames ? '' : 'text')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EnterTextTextRequest clone() => EnterTextTextRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EnterTextTextRequest copyWith(void Function(EnterTextTextRequest) updates) => super.copyWith((message) => updates(message as EnterTextTextRequest)) as EnterTextTextRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EnterTextTextRequest create() => EnterTextTextRequest._();
  EnterTextTextRequest createEmptyInstance() => create();
  static $pb.PbList<EnterTextTextRequest> createRepeated() => $pb.PbList<EnterTextTextRequest>();
  @$core.pragma('dart2js:noInline')
  static EnterTextTextRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EnterTextTextRequest>(create);
  static EnterTextTextRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetText => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetText($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetText() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetText() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get text => $_getSZ(1);
  @$pb.TagNumber(2)
  set text($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasText() => $_has(1);
  @$pb.TagNumber(2)
  void clearText() => $_clearField(2);
}

/// Request for entering text by tooltip
class EnterTextTooltipRequest extends $pb.GeneratedMessage {
  factory EnterTextTooltipRequest({
    $core.String? tooltip,
    $core.String? text,
  }) {
    final $result = create();
    if (tooltip != null) {
      $result.tooltip = tooltip;
    }
    if (text != null) {
      $result.text = text;
    }
    return $result;
  }
  EnterTextTooltipRequest._() : super();
  factory EnterTextTooltipRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EnterTextTooltipRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EnterTextTooltipRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'tooltip')
    ..aOS(2, _omitFieldNames ? '' : 'text')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EnterTextTooltipRequest clone() => EnterTextTooltipRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EnterTextTooltipRequest copyWith(void Function(EnterTextTooltipRequest) updates) => super.copyWith((message) => updates(message as EnterTextTooltipRequest)) as EnterTextTooltipRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EnterTextTooltipRequest create() => EnterTextTooltipRequest._();
  EnterTextTooltipRequest createEmptyInstance() => create();
  static $pb.PbList<EnterTextTooltipRequest> createRepeated() => $pb.PbList<EnterTextTooltipRequest>();
  @$core.pragma('dart2js:noInline')
  static EnterTextTooltipRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EnterTextTooltipRequest>(create);
  static EnterTextTooltipRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get tooltip => $_getSZ(0);
  @$pb.TagNumber(1)
  set tooltip($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasTooltip() => $_has(0);
  @$pb.TagNumber(1)
  void clearTooltip() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get text => $_getSZ(1);
  @$pb.TagNumber(2)
  set text($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasText() => $_has(1);
  @$pb.TagNumber(2)
  void clearText() => $_clearField(2);
}

/// Request for entering text by ancestor and descendant
class EnterTextAncestorDescendantRequest extends $pb.GeneratedMessage {
  factory EnterTextAncestorDescendantRequest({
    $core.String? ancestorType,
    $core.String? descendantType,
    $core.String? text,
  }) {
    final $result = create();
    if (ancestorType != null) {
      $result.ancestorType = ancestorType;
    }
    if (descendantType != null) {
      $result.descendantType = descendantType;
    }
    if (text != null) {
      $result.text = text;
    }
    return $result;
  }
  EnterTextAncestorDescendantRequest._() : super();
  factory EnterTextAncestorDescendantRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory EnterTextAncestorDescendantRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'EnterTextAncestorDescendantRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'ancestorType')
    ..aOS(2, _omitFieldNames ? '' : 'descendantType')
    ..aOS(3, _omitFieldNames ? '' : 'text')
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  EnterTextAncestorDescendantRequest clone() => EnterTextAncestorDescendantRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  EnterTextAncestorDescendantRequest copyWith(void Function(EnterTextAncestorDescendantRequest) updates) => super.copyWith((message) => updates(message as EnterTextAncestorDescendantRequest)) as EnterTextAncestorDescendantRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static EnterTextAncestorDescendantRequest create() => EnterTextAncestorDescendantRequest._();
  EnterTextAncestorDescendantRequest createEmptyInstance() => create();
  static $pb.PbList<EnterTextAncestorDescendantRequest> createRepeated() => $pb.PbList<EnterTextAncestorDescendantRequest>();
  @$core.pragma('dart2js:noInline')
  static EnterTextAncestorDescendantRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<EnterTextAncestorDescendantRequest>(create);
  static EnterTextAncestorDescendantRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get ancestorType => $_getSZ(0);
  @$pb.TagNumber(1)
  set ancestorType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasAncestorType() => $_has(0);
  @$pb.TagNumber(1)
  void clearAncestorType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get descendantType => $_getSZ(1);
  @$pb.TagNumber(2)
  set descendantType($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDescendantType() => $_has(1);
  @$pb.TagNumber(2)
  void clearDescendantType() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.String get text => $_getSZ(2);
  @$pb.TagNumber(3)
  set text($core.String v) { $_setString(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasText() => $_has(2);
  @$pb.TagNumber(3)
  void clearText() => $_clearField(3);
}

/// Request for scroll key
class ScrollKeyRequest extends $pb.GeneratedMessage {
  factory ScrollKeyRequest({
    $core.String? keyValue,
    $core.double? dx,
    $core.double? dy,
    $fixnum.Int64? durationMicroseconds,
    $core.int? frequency,
  }) {
    final $result = create();
    if (keyValue != null) {
      $result.keyValue = keyValue;
    }
    if (dx != null) {
      $result.dx = dx;
    }
    if (dy != null) {
      $result.dy = dy;
    }
    if (durationMicroseconds != null) {
      $result.durationMicroseconds = durationMicroseconds;
    }
    if (frequency != null) {
      $result.frequency = frequency;
    }
    return $result;
  }
  ScrollKeyRequest._() : super();
  factory ScrollKeyRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollKeyRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollKeyRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'keyValue')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'dx', $pb.PbFieldType.OD)
    ..a<$core.double>(3, _omitFieldNames ? '' : 'dy', $pb.PbFieldType.OD)
    ..aInt64(4, _omitFieldNames ? '' : 'durationMicroseconds')
    ..a<$core.int>(5, _omitFieldNames ? '' : 'frequency', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollKeyRequest clone() => ScrollKeyRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollKeyRequest copyWith(void Function(ScrollKeyRequest) updates) => super.copyWith((message) => updates(message as ScrollKeyRequest)) as ScrollKeyRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollKeyRequest create() => ScrollKeyRequest._();
  ScrollKeyRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollKeyRequest> createRepeated() => $pb.PbList<ScrollKeyRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollKeyRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollKeyRequest>(create);
  static ScrollKeyRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get keyValue => $_getSZ(0);
  @$pb.TagNumber(1)
  set keyValue($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasKeyValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearKeyValue() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get dx => $_getN(1);
  @$pb.TagNumber(2)
  set dx($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDx() => $_has(1);
  @$pb.TagNumber(2)
  void clearDx() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get dy => $_getN(2);
  @$pb.TagNumber(3)
  set dy($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasDy() => $_has(2);
  @$pb.TagNumber(3)
  void clearDy() => $_clearField(3);

  @$pb.TagNumber(4)
  $fixnum.Int64 get durationMicroseconds => $_getI64(3);
  @$pb.TagNumber(4)
  set durationMicroseconds($fixnum.Int64 v) { $_setInt64(3, v); }
  @$pb.TagNumber(4)
  $core.bool hasDurationMicroseconds() => $_has(3);
  @$pb.TagNumber(4)
  void clearDurationMicroseconds() => $_clearField(4);

  @$pb.TagNumber(5)
  $core.int get frequency => $_getIZ(4);
  @$pb.TagNumber(5)
  set frequency($core.int v) { $_setSignedInt32(4, v); }
  @$pb.TagNumber(5)
  $core.bool hasFrequency() => $_has(4);
  @$pb.TagNumber(5)
  void clearFrequency() => $_clearField(5);
}

/// Request for scroll type
class ScrollTypeRequest extends $pb.GeneratedMessage {
  factory ScrollTypeRequest({
    $core.String? widgetType,
    $core.double? dx,
    $core.double? dy,
    $fixnum.Int64? durationMicroseconds,
    $core.int? frequency,
  }) {
    final $result = create();
    if (widgetType != null) {
      $result.widgetType = widgetType;
    }
    if (dx != null) {
      $result.dx = dx;
    }
    if (dy != null) {
      $result.dy = dy;
    }
    if (durationMicroseconds != null) {
      $result.durationMicroseconds = durationMicroseconds;
    }
    if (frequency != null) {
      $result.frequency = frequency;
    }
    return $result;
  }
  ScrollTypeRequest._() : super();
  factory ScrollTypeRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollTypeRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollTypeRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetType')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'dx', $pb.PbFieldType.OD)
    ..a<$core.double>(3, _omitFieldNames ? '' : 'dy', $pb.PbFieldType.OD)
    ..aInt64(4, _omitFieldNames ? '' : 'durationMicroseconds')
    ..a<$core.int>(5, _omitFieldNames ? '' : 'frequency', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollTypeRequest clone() => ScrollTypeRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollTypeRequest copyWith(void Function(ScrollTypeRequest) updates) => super.copyWith((message) => updates(message as ScrollTypeRequest)) as ScrollTypeRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollTypeRequest create() => ScrollTypeRequest._();
  ScrollTypeRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollTypeRequest> createRepeated() => $pb.PbList<ScrollTypeRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollTypeRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollTypeRequest>(create);
  static ScrollTypeRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetType => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetType() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get dx => $_getN(1);
  @$pb.TagNumber(2)
  set dx($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDx() => $_has(1);
  @$pb.TagNumber(2)
  void clearDx() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get dy => $_getN(2);
  @$pb.TagNumber(3)
  set dy($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasDy() => $_has(2);
  @$pb.TagNumber(3)
  void clearDy() => $_clearField(3);

  @$pb.TagNumber(4)
  $fixnum.Int64 get durationMicroseconds => $_getI64(3);
  @$pb.TagNumber(4)
  set durationMicroseconds($fixnum.Int64 v) { $_setInt64(3, v); }
  @$pb.TagNumber(4)
  $core.bool hasDurationMicroseconds() => $_has(3);
  @$pb.TagNumber(4)
  void clearDurationMicroseconds() => $_clearField(4);

  @$pb.TagNumber(5)
  $core.int get frequency => $_getIZ(4);
  @$pb.TagNumber(5)
  set frequency($core.int v) { $_setSignedInt32(4, v); }
  @$pb.TagNumber(5)
  $core.bool hasFrequency() => $_has(4);
  @$pb.TagNumber(5)
  void clearFrequency() => $_clearField(5);
}

/// Request for scroll text
class ScrollTextRequest extends $pb.GeneratedMessage {
  factory ScrollTextRequest({
    $core.String? text,
    $core.double? dx,
    $core.double? dy,
    $fixnum.Int64? durationMicroseconds,
    $core.int? frequency,
  }) {
    final $result = create();
    if (text != null) {
      $result.text = text;
    }
    if (dx != null) {
      $result.dx = dx;
    }
    if (dy != null) {
      $result.dy = dy;
    }
    if (durationMicroseconds != null) {
      $result.durationMicroseconds = durationMicroseconds;
    }
    if (frequency != null) {
      $result.frequency = frequency;
    }
    return $result;
  }
  ScrollTextRequest._() : super();
  factory ScrollTextRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollTextRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollTextRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'text')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'dx', $pb.PbFieldType.OD)
    ..a<$core.double>(3, _omitFieldNames ? '' : 'dy', $pb.PbFieldType.OD)
    ..aInt64(4, _omitFieldNames ? '' : 'durationMicroseconds')
    ..a<$core.int>(5, _omitFieldNames ? '' : 'frequency', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollTextRequest clone() => ScrollTextRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollTextRequest copyWith(void Function(ScrollTextRequest) updates) => super.copyWith((message) => updates(message as ScrollTextRequest)) as ScrollTextRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollTextRequest create() => ScrollTextRequest._();
  ScrollTextRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollTextRequest> createRepeated() => $pb.PbList<ScrollTextRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollTextRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollTextRequest>(create);
  static ScrollTextRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get text => $_getSZ(0);
  @$pb.TagNumber(1)
  set text($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasText() => $_has(0);
  @$pb.TagNumber(1)
  void clearText() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get dx => $_getN(1);
  @$pb.TagNumber(2)
  set dx($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDx() => $_has(1);
  @$pb.TagNumber(2)
  void clearDx() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get dy => $_getN(2);
  @$pb.TagNumber(3)
  set dy($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasDy() => $_has(2);
  @$pb.TagNumber(3)
  void clearDy() => $_clearField(3);

  @$pb.TagNumber(4)
  $fixnum.Int64 get durationMicroseconds => $_getI64(3);
  @$pb.TagNumber(4)
  set durationMicroseconds($fixnum.Int64 v) { $_setInt64(3, v); }
  @$pb.TagNumber(4)
  $core.bool hasDurationMicroseconds() => $_has(3);
  @$pb.TagNumber(4)
  void clearDurationMicroseconds() => $_clearField(4);

  @$pb.TagNumber(5)
  $core.int get frequency => $_getIZ(4);
  @$pb.TagNumber(5)
  set frequency($core.int v) { $_setSignedInt32(4, v); }
  @$pb.TagNumber(5)
  $core.bool hasFrequency() => $_has(4);
  @$pb.TagNumber(5)
  void clearFrequency() => $_clearField(5);
}

/// Request for scroll tooltip
class ScrollTooltipRequest extends $pb.GeneratedMessage {
  factory ScrollTooltipRequest({
    $core.String? tooltip,
    $core.double? dx,
    $core.double? dy,
    $fixnum.Int64? durationMicroseconds,
    $core.int? frequency,
  }) {
    final $result = create();
    if (tooltip != null) {
      $result.tooltip = tooltip;
    }
    if (dx != null) {
      $result.dx = dx;
    }
    if (dy != null) {
      $result.dy = dy;
    }
    if (durationMicroseconds != null) {
      $result.durationMicroseconds = durationMicroseconds;
    }
    if (frequency != null) {
      $result.frequency = frequency;
    }
    return $result;
  }
  ScrollTooltipRequest._() : super();
  factory ScrollTooltipRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollTooltipRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollTooltipRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'tooltip')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'dx', $pb.PbFieldType.OD)
    ..a<$core.double>(3, _omitFieldNames ? '' : 'dy', $pb.PbFieldType.OD)
    ..aInt64(4, _omitFieldNames ? '' : 'durationMicroseconds')
    ..a<$core.int>(5, _omitFieldNames ? '' : 'frequency', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollTooltipRequest clone() => ScrollTooltipRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollTooltipRequest copyWith(void Function(ScrollTooltipRequest) updates) => super.copyWith((message) => updates(message as ScrollTooltipRequest)) as ScrollTooltipRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollTooltipRequest create() => ScrollTooltipRequest._();
  ScrollTooltipRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollTooltipRequest> createRepeated() => $pb.PbList<ScrollTooltipRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollTooltipRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollTooltipRequest>(create);
  static ScrollTooltipRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get tooltip => $_getSZ(0);
  @$pb.TagNumber(1)
  set tooltip($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasTooltip() => $_has(0);
  @$pb.TagNumber(1)
  void clearTooltip() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get dx => $_getN(1);
  @$pb.TagNumber(2)
  set dx($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDx() => $_has(1);
  @$pb.TagNumber(2)
  void clearDx() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get dy => $_getN(2);
  @$pb.TagNumber(3)
  set dy($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasDy() => $_has(2);
  @$pb.TagNumber(3)
  void clearDy() => $_clearField(3);

  @$pb.TagNumber(4)
  $fixnum.Int64 get durationMicroseconds => $_getI64(3);
  @$pb.TagNumber(4)
  set durationMicroseconds($fixnum.Int64 v) { $_setInt64(3, v); }
  @$pb.TagNumber(4)
  $core.bool hasDurationMicroseconds() => $_has(3);
  @$pb.TagNumber(4)
  void clearDurationMicroseconds() => $_clearField(4);

  @$pb.TagNumber(5)
  $core.int get frequency => $_getIZ(4);
  @$pb.TagNumber(5)
  set frequency($core.int v) { $_setSignedInt32(4, v); }
  @$pb.TagNumber(5)
  $core.bool hasFrequency() => $_has(4);
  @$pb.TagNumber(5)
  void clearFrequency() => $_clearField(5);
}

/// Request for scroll ancestor and descendant
class ScrollAncestorDescendantRequest extends $pb.GeneratedMessage {
  factory ScrollAncestorDescendantRequest({
    $core.String? ancestorType,
    $core.String? descendantType,
    $core.double? dx,
    $core.double? dy,
    $fixnum.Int64? durationMicroseconds,
    $core.int? frequency,
  }) {
    final $result = create();
    if (ancestorType != null) {
      $result.ancestorType = ancestorType;
    }
    if (descendantType != null) {
      $result.descendantType = descendantType;
    }
    if (dx != null) {
      $result.dx = dx;
    }
    if (dy != null) {
      $result.dy = dy;
    }
    if (durationMicroseconds != null) {
      $result.durationMicroseconds = durationMicroseconds;
    }
    if (frequency != null) {
      $result.frequency = frequency;
    }
    return $result;
  }
  ScrollAncestorDescendantRequest._() : super();
  factory ScrollAncestorDescendantRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollAncestorDescendantRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollAncestorDescendantRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'ancestorType')
    ..aOS(2, _omitFieldNames ? '' : 'descendantType')
    ..a<$core.double>(3, _omitFieldNames ? '' : 'dx', $pb.PbFieldType.OD)
    ..a<$core.double>(4, _omitFieldNames ? '' : 'dy', $pb.PbFieldType.OD)
    ..aInt64(5, _omitFieldNames ? '' : 'durationMicroseconds')
    ..a<$core.int>(6, _omitFieldNames ? '' : 'frequency', $pb.PbFieldType.O3)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollAncestorDescendantRequest clone() => ScrollAncestorDescendantRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollAncestorDescendantRequest copyWith(void Function(ScrollAncestorDescendantRequest) updates) => super.copyWith((message) => updates(message as ScrollAncestorDescendantRequest)) as ScrollAncestorDescendantRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollAncestorDescendantRequest create() => ScrollAncestorDescendantRequest._();
  ScrollAncestorDescendantRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollAncestorDescendantRequest> createRepeated() => $pb.PbList<ScrollAncestorDescendantRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollAncestorDescendantRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollAncestorDescendantRequest>(create);
  static ScrollAncestorDescendantRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get ancestorType => $_getSZ(0);
  @$pb.TagNumber(1)
  set ancestorType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasAncestorType() => $_has(0);
  @$pb.TagNumber(1)
  void clearAncestorType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get descendantType => $_getSZ(1);
  @$pb.TagNumber(2)
  set descendantType($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDescendantType() => $_has(1);
  @$pb.TagNumber(2)
  void clearDescendantType() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get dx => $_getN(2);
  @$pb.TagNumber(3)
  set dx($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasDx() => $_has(2);
  @$pb.TagNumber(3)
  void clearDx() => $_clearField(3);

  @$pb.TagNumber(4)
  $core.double get dy => $_getN(3);
  @$pb.TagNumber(4)
  set dy($core.double v) { $_setDouble(3, v); }
  @$pb.TagNumber(4)
  $core.bool hasDy() => $_has(3);
  @$pb.TagNumber(4)
  void clearDy() => $_clearField(4);

  @$pb.TagNumber(5)
  $fixnum.Int64 get durationMicroseconds => $_getI64(4);
  @$pb.TagNumber(5)
  set durationMicroseconds($fixnum.Int64 v) { $_setInt64(4, v); }
  @$pb.TagNumber(5)
  $core.bool hasDurationMicroseconds() => $_has(4);
  @$pb.TagNumber(5)
  void clearDurationMicroseconds() => $_clearField(5);

  @$pb.TagNumber(6)
  $core.int get frequency => $_getIZ(5);
  @$pb.TagNumber(6)
  set frequency($core.int v) { $_setSignedInt32(5, v); }
  @$pb.TagNumber(6)
  $core.bool hasFrequency() => $_has(5);
  @$pb.TagNumber(6)
  void clearFrequency() => $_clearField(6);
}

/// Request for scroll into view by key
class ScrollIntoViewKeyRequest extends $pb.GeneratedMessage {
  factory ScrollIntoViewKeyRequest({
    $core.String? keyValue,
    $core.double? alignment,
  }) {
    final $result = create();
    if (keyValue != null) {
      $result.keyValue = keyValue;
    }
    if (alignment != null) {
      $result.alignment = alignment;
    }
    return $result;
  }
  ScrollIntoViewKeyRequest._() : super();
  factory ScrollIntoViewKeyRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollIntoViewKeyRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollIntoViewKeyRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'keyValue')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'alignment', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollIntoViewKeyRequest clone() => ScrollIntoViewKeyRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollIntoViewKeyRequest copyWith(void Function(ScrollIntoViewKeyRequest) updates) => super.copyWith((message) => updates(message as ScrollIntoViewKeyRequest)) as ScrollIntoViewKeyRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewKeyRequest create() => ScrollIntoViewKeyRequest._();
  ScrollIntoViewKeyRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollIntoViewKeyRequest> createRepeated() => $pb.PbList<ScrollIntoViewKeyRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewKeyRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollIntoViewKeyRequest>(create);
  static ScrollIntoViewKeyRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get keyValue => $_getSZ(0);
  @$pb.TagNumber(1)
  set keyValue($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasKeyValue() => $_has(0);
  @$pb.TagNumber(1)
  void clearKeyValue() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get alignment => $_getN(1);
  @$pb.TagNumber(2)
  set alignment($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasAlignment() => $_has(1);
  @$pb.TagNumber(2)
  void clearAlignment() => $_clearField(2);
}

/// Request for scroll into view by type
class ScrollIntoViewTypeRequest extends $pb.GeneratedMessage {
  factory ScrollIntoViewTypeRequest({
    $core.String? widgetType,
    $core.double? alignment,
  }) {
    final $result = create();
    if (widgetType != null) {
      $result.widgetType = widgetType;
    }
    if (alignment != null) {
      $result.alignment = alignment;
    }
    return $result;
  }
  ScrollIntoViewTypeRequest._() : super();
  factory ScrollIntoViewTypeRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollIntoViewTypeRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollIntoViewTypeRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'widgetType')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'alignment', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollIntoViewTypeRequest clone() => ScrollIntoViewTypeRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollIntoViewTypeRequest copyWith(void Function(ScrollIntoViewTypeRequest) updates) => super.copyWith((message) => updates(message as ScrollIntoViewTypeRequest)) as ScrollIntoViewTypeRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewTypeRequest create() => ScrollIntoViewTypeRequest._();
  ScrollIntoViewTypeRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollIntoViewTypeRequest> createRepeated() => $pb.PbList<ScrollIntoViewTypeRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewTypeRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollIntoViewTypeRequest>(create);
  static ScrollIntoViewTypeRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get widgetType => $_getSZ(0);
  @$pb.TagNumber(1)
  set widgetType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasWidgetType() => $_has(0);
  @$pb.TagNumber(1)
  void clearWidgetType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get alignment => $_getN(1);
  @$pb.TagNumber(2)
  set alignment($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasAlignment() => $_has(1);
  @$pb.TagNumber(2)
  void clearAlignment() => $_clearField(2);
}

/// Request for scroll into view by text
class ScrollIntoViewTextRequest extends $pb.GeneratedMessage {
  factory ScrollIntoViewTextRequest({
    $core.String? text,
    $core.double? alignment,
  }) {
    final $result = create();
    if (text != null) {
      $result.text = text;
    }
    if (alignment != null) {
      $result.alignment = alignment;
    }
    return $result;
  }
  ScrollIntoViewTextRequest._() : super();
  factory ScrollIntoViewTextRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollIntoViewTextRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollIntoViewTextRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'text')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'alignment', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollIntoViewTextRequest clone() => ScrollIntoViewTextRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollIntoViewTextRequest copyWith(void Function(ScrollIntoViewTextRequest) updates) => super.copyWith((message) => updates(message as ScrollIntoViewTextRequest)) as ScrollIntoViewTextRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewTextRequest create() => ScrollIntoViewTextRequest._();
  ScrollIntoViewTextRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollIntoViewTextRequest> createRepeated() => $pb.PbList<ScrollIntoViewTextRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewTextRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollIntoViewTextRequest>(create);
  static ScrollIntoViewTextRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get text => $_getSZ(0);
  @$pb.TagNumber(1)
  set text($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasText() => $_has(0);
  @$pb.TagNumber(1)
  void clearText() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get alignment => $_getN(1);
  @$pb.TagNumber(2)
  set alignment($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasAlignment() => $_has(1);
  @$pb.TagNumber(2)
  void clearAlignment() => $_clearField(2);
}

/// Request for scroll into view by tooltip
class ScrollIntoViewTooltipRequest extends $pb.GeneratedMessage {
  factory ScrollIntoViewTooltipRequest({
    $core.String? tooltip,
    $core.double? alignment,
  }) {
    final $result = create();
    if (tooltip != null) {
      $result.tooltip = tooltip;
    }
    if (alignment != null) {
      $result.alignment = alignment;
    }
    return $result;
  }
  ScrollIntoViewTooltipRequest._() : super();
  factory ScrollIntoViewTooltipRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollIntoViewTooltipRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollIntoViewTooltipRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'tooltip')
    ..a<$core.double>(2, _omitFieldNames ? '' : 'alignment', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollIntoViewTooltipRequest clone() => ScrollIntoViewTooltipRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollIntoViewTooltipRequest copyWith(void Function(ScrollIntoViewTooltipRequest) updates) => super.copyWith((message) => updates(message as ScrollIntoViewTooltipRequest)) as ScrollIntoViewTooltipRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewTooltipRequest create() => ScrollIntoViewTooltipRequest._();
  ScrollIntoViewTooltipRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollIntoViewTooltipRequest> createRepeated() => $pb.PbList<ScrollIntoViewTooltipRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewTooltipRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollIntoViewTooltipRequest>(create);
  static ScrollIntoViewTooltipRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get tooltip => $_getSZ(0);
  @$pb.TagNumber(1)
  set tooltip($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasTooltip() => $_has(0);
  @$pb.TagNumber(1)
  void clearTooltip() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.double get alignment => $_getN(1);
  @$pb.TagNumber(2)
  set alignment($core.double v) { $_setDouble(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasAlignment() => $_has(1);
  @$pb.TagNumber(2)
  void clearAlignment() => $_clearField(2);
}

/// Request for scroll into view by ancestor and descendant
class ScrollIntoViewAncestorDescendantRequest extends $pb.GeneratedMessage {
  factory ScrollIntoViewAncestorDescendantRequest({
    $core.String? ancestorType,
    $core.String? descendantType,
    $core.double? alignment,
  }) {
    final $result = create();
    if (ancestorType != null) {
      $result.ancestorType = ancestorType;
    }
    if (descendantType != null) {
      $result.descendantType = descendantType;
    }
    if (alignment != null) {
      $result.alignment = alignment;
    }
    return $result;
  }
  ScrollIntoViewAncestorDescendantRequest._() : super();
  factory ScrollIntoViewAncestorDescendantRequest.fromBuffer($core.List<$core.int> i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromBuffer(i, r);
  factory ScrollIntoViewAncestorDescendantRequest.fromJson($core.String i, [$pb.ExtensionRegistry r = $pb.ExtensionRegistry.EMPTY]) => create()..mergeFromJson(i, r);

  static final $pb.BuilderInfo _i = $pb.BuilderInfo(_omitMessageNames ? '' : 'ScrollIntoViewAncestorDescendantRequest', package: const $pb.PackageName(_omitMessageNames ? '' : 'dart_vm_service'), createEmptyInstance: create)
    ..aOS(1, _omitFieldNames ? '' : 'ancestorType')
    ..aOS(2, _omitFieldNames ? '' : 'descendantType')
    ..a<$core.double>(3, _omitFieldNames ? '' : 'alignment', $pb.PbFieldType.OD)
    ..hasRequiredFields = false
  ;

  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.deepCopy] instead. '
  'Will be removed in next major version')
  ScrollIntoViewAncestorDescendantRequest clone() => ScrollIntoViewAncestorDescendantRequest()..mergeFromMessage(this);
  @$core.Deprecated(
  'Using this can add significant overhead to your binary. '
  'Use [GeneratedMessageGenericExtensions.rebuild] instead. '
  'Will be removed in next major version')
  ScrollIntoViewAncestorDescendantRequest copyWith(void Function(ScrollIntoViewAncestorDescendantRequest) updates) => super.copyWith((message) => updates(message as ScrollIntoViewAncestorDescendantRequest)) as ScrollIntoViewAncestorDescendantRequest;

  $pb.BuilderInfo get info_ => _i;

  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewAncestorDescendantRequest create() => ScrollIntoViewAncestorDescendantRequest._();
  ScrollIntoViewAncestorDescendantRequest createEmptyInstance() => create();
  static $pb.PbList<ScrollIntoViewAncestorDescendantRequest> createRepeated() => $pb.PbList<ScrollIntoViewAncestorDescendantRequest>();
  @$core.pragma('dart2js:noInline')
  static ScrollIntoViewAncestorDescendantRequest getDefault() => _defaultInstance ??= $pb.GeneratedMessage.$_defaultFor<ScrollIntoViewAncestorDescendantRequest>(create);
  static ScrollIntoViewAncestorDescendantRequest? _defaultInstance;

  @$pb.TagNumber(1)
  $core.String get ancestorType => $_getSZ(0);
  @$pb.TagNumber(1)
  set ancestorType($core.String v) { $_setString(0, v); }
  @$pb.TagNumber(1)
  $core.bool hasAncestorType() => $_has(0);
  @$pb.TagNumber(1)
  void clearAncestorType() => $_clearField(1);

  @$pb.TagNumber(2)
  $core.String get descendantType => $_getSZ(1);
  @$pb.TagNumber(2)
  set descendantType($core.String v) { $_setString(1, v); }
  @$pb.TagNumber(2)
  $core.bool hasDescendantType() => $_has(1);
  @$pb.TagNumber(2)
  void clearDescendantType() => $_clearField(2);

  @$pb.TagNumber(3)
  $core.double get alignment => $_getN(2);
  @$pb.TagNumber(3)
  set alignment($core.double v) { $_setDouble(2, v); }
  @$pb.TagNumber(3)
  $core.bool hasAlignment() => $_has(2);
  @$pb.TagNumber(3)
  void clearAlignment() => $_clearField(3);
}


const _omitFieldNames = $core.bool.fromEnvironment('protobuf.omit_field_names');
const _omitMessageNames = $core.bool.fromEnvironment('protobuf.omit_message_names');
