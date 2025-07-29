import 'dart:convert';
import 'package:grpc/grpc.dart';
import '../dart_vm_service_tool.dart';
import 'package:vm_service/vm_service.dart' as vm;

// Import the generated files from the correct location
import 'generated/dart_vm_service.pbgrpc.dart';

/// Main service implementation for the Dart VM Service gRPC API
class DartVmServiceGrpcService extends DartVmServiceBase {
  final DartVmServiceTool _tool = DartVmServiceTool();
  bool _isConnected = false;

  // Check if connected and return appropriate error response if not
  T _checkConnection<T>(T errorResponse, String fieldName) {
    if (!_isConnected) {
      final dynamic response = errorResponse;
      response.success = false;
      response.message = 'Not connected to a Flutter application';
      if (fieldName.isNotEmpty) {
        response.setField(0, fieldName);
      }
      return response;
    }
    return errorResponse;
  }

  // Helper method to convert Response's JSON to string
  String? _responseJsonToString(vm.Response? response) {
    if (response == null || response.json == null) {
      return null;
    }
    return jsonEncode(response.json);
  }

  // Helper method for standard GenericResponse pattern
  Future<GenericResponse> _handleGenericResponse<T>(
    Future<vm.Response> Function() toolMethod,
    String successMessage,
    String errorPrefix,
  ) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await toolMethod();
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = successMessage
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = '$errorPrefix: $e';
    }
  }

  // Connection
  @override
  Future<ConnectResponse> connect(
      ServiceCall call, ConnectRequest request) async {
    try {
      await _tool.start(request.vmServiceUri);
      _isConnected = true;
      return ConnectResponse()
        ..success = true
        ..message = 'Successfully connected to Flutter application';
    } catch (e) {
      return ConnectResponse()
        ..success = false
        ..message = 'Failed to connect: $e';
    }
  }

  // Debug visualization methods
  @override
  Future<ToggleResponse> toggleDebugPaint(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.toggleDebugPaint(request.enable);
      return ToggleResponse()
        ..success = true
        ..message = 'Debug paint ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle debug paint: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleRepaintRainbow(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleRepaintRainbow(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Repaint rainbow ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle repaint rainbow: $e';
    }
  }

  @override
  Future<ToggleResponse> togglePerformanceOverlay(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.togglePerformanceOverlay(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Performance overlay ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle performance overlay: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleBaselinePainting(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleBaselinePainting(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Baseline painting ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle baseline painting: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleDebugBanner(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleDebugBanner(request.enable);
      return ToggleResponse()
        ..success = true
        ..message = 'Debug banner ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle debug banner: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleStructuredErrors(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleStructuredErrors(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Structured errors ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle structured errors: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleOversizedImages(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleOversizedImages(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Oversized images ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle oversized images: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleDisablePhysicalShapeLayers(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleDisablePhysicalShapeLayers(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Physical shape layers ${request.enable ? 'disabled' : 'enabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle physical shape layers: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleDisableOpacityLayers(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleDisableOpacityLayers(request.enable);
      return ToggleResponse()
        ..success = true
        ..message = 'Opacity layers ${request.enable ? 'disabled' : 'enabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle opacity layers: $e';
    }
  }

  // Profiling methods
  @override
  Future<ToggleResponse> toggleProfileWidgetBuilds(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleProfileWidgetBuilds(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Profile widget builds ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle profile widget builds: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleProfileUserWidgetBuilds(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleProfileUserWidgetBuilds(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Profile user widget builds ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle profile user widget builds: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleProfileRenderObjectPaints(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleProfileRenderObjectPaints(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Profile render object paints ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle profile render object paints: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleProfileRenderObjectLayouts(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleProfileRenderObjectLayouts(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Profile render object layouts ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle profile render object layouts: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleProfilePlatformChannels(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleProfilePlatformChannels(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Profile platform channels ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle profile platform channels: $e';
    }
  }

  // Inspector control methods
  @override
  Future<ToggleResponse> toggleInspector(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleInspector(request.enable);
      return ToggleResponse()
        ..success = true
        ..message = 'Inspector ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle inspector: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleTrackRebuildWidgets(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleTrackRebuildWidgets(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Track rebuild widgets ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle track rebuild widgets: $e';
    }
  }

  @override
  Future<ToggleResponse> toggleTrackRepaintWidgets(
      ServiceCall call, ToggleRequest request) async {
    if (!_isConnected) {
      return ToggleResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      await _tool.toggleTrackRepaintWidgets(request.enable);
      return ToggleResponse()
        ..success = true
        ..message =
            'Track repaint widgets ${request.enable ? 'enabled' : 'disabled'}';
    } catch (e) {
      return ToggleResponse()
        ..success = false
        ..message = 'Failed to toggle track repaint widgets: $e';
    }
  }

  // Information methods
  @override
  Future<DisplayRefreshRateResponse> getDisplayRefreshRate(
      ServiceCall call, ViewIdRequest request) async {
    if (!_isConnected) {
      return DisplayRefreshRateResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.getDisplayRefreshRate(request.viewId);
      final jsonResult = (result.json?['result'] as num?)?.toDouble() ?? 0.0;

      return DisplayRefreshRateResponse()
        ..success = true
        ..message = 'Successfully retrieved display refresh rate'
        ..refreshRate = jsonResult;
    } catch (e) {
      return DisplayRefreshRateResponse()
        ..success = false
        ..message = 'Failed to get display refresh rate: $e';
    }
  }

  @override
  Future<ListViewsResponse> listViews(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return ListViewsResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.listViews();
      final viewsList = <String>[];

      // Extract view IDs from the response
      if (result.json != null && result.json!.containsKey('result')) {
        final views = result.json!['result']['views'] as List<dynamic>?;
        if (views != null) {
          for (final view in views) {
            if (view is Map<String, dynamic> && view.containsKey('id')) {
              viewsList.add(view['id'] as String);
            }
          }
        }
      }

      return ListViewsResponse()
        ..success = true
        ..message = 'Successfully retrieved views'
        ..views.addAll(viewsList);
    } catch (e) {
      return ListViewsResponse()
        ..success = false
        ..message = 'Failed to list views: $e';
    }
  }

  // Tree dump methods
  @override
  Future<TreeDumpResponse> dumpWidgetTree(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.dumpWidgetTree();
      final fullJsonDump = _responseJsonToString(result);

      return TreeDumpResponse()
        ..success = true
        ..message = 'Successfully dumped widget tree'
        ..treeDump = fullJsonDump ?? '';
    } catch (e) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Failed to dump widget tree: $e';
    }
  }

  @override
  Future<TreeDumpResponse> dumpLayerTree(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.dumpLayerTree();
      final fullJsonDump = _responseJsonToString(result);

      return TreeDumpResponse()
        ..success = true
        ..message = 'Successfully dumped layer tree'
        ..treeDump = fullJsonDump ?? '';
    } catch (e) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Failed to dump layer tree: $e';
    }
  }

  @override
  Future<TreeDumpResponse> dumpRenderTree(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.dumpRenderTree();
      final fullJsonDump = _responseJsonToString(result);

      return TreeDumpResponse()
        ..success = true
        ..message = 'Successfully dumped render tree'
        ..treeDump = fullJsonDump ?? '';
    } catch (e) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Failed to dump render tree: $e';
    }
  }

  @override
  Future<TreeDumpResponse> dumpSemanticsTreeInTraversalOrder(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.dumpSemanticsTreeInTraversalOrder();
      final fullJsonDump = _responseJsonToString(result);

      return TreeDumpResponse()
        ..success = true
        ..message = 'Successfully dumped semantics tree in traversal order'
        ..treeDump = fullJsonDump ?? '';
    } catch (e) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Failed to dump semantics tree in traversal order: $e';
    }
  }

  @override
  Future<TreeDumpResponse> dumpSemanticsTreeInInverseHitTestOrder(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.dumpSemanticsTreeInInverseHitTestOrder();
      final fullJsonDump = _responseJsonToString(result);

      return TreeDumpResponse()
        ..success = true
        ..message =
            'Successfully dumped semantics tree in inverse hit test order'
        ..treeDump = fullJsonDump ?? '';
    } catch (e) {
      return TreeDumpResponse()
        ..success = false
        ..message =
            'Failed to dump semantics tree in inverse hit test order: $e';
    }
  }

  @override
  Future<TreeDumpResponse> dumpFocusTree(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.dumpFocusTree();
      final fullJsonDump = _responseJsonToString(result);

      return TreeDumpResponse()
        ..success = true
        ..message = 'Successfully dumped focus tree'
        ..treeDump = fullJsonDump ?? '';
    } catch (e) {
      return TreeDumpResponse()
        ..success = false
        ..message = 'Failed to dump focus tree: $e';
    }
  }

  // Frame and timing methods
  @override
  Future<GenericResponse> setTimeDilation(
      ServiceCall call, DoubleValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.setTimeDilation(request.value),
      'Successfully set time dilation to ${request.value}',
      'Failed to set time dilation',
    );
  }

  @override
  Future<GenericResponse> didSendFirstFrameEvent(
      ServiceCall call, BoolValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.didSendFirstFrameEvent(request.value),
      'Successfully set first frame event to ${request.value}',
      'Failed to set first frame event',
    );
  }

  @override
  Future<GenericResponse> didSendFirstFrameRasterizedEvent(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.didSendFirstFrameRasterizedEvent(request.value),
      'Successfully set first frame rasterized event to ${request.value}',
      'Failed to set first frame rasterized event',
    );
  }

  // Asset and application management
  @override
  Future<GenericResponse> evictAssets(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.evictAssets(request.value),
      'Successfully evicted asset: ${request.value}',
      'Failed to evict asset',
    );
  }

  @override
  Future<GenericResponse> reassemble(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.reassemble();
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully reassembled application'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to reassemble application: $e';
    }
  }

  @override
  Future<GenericResponse> exitApp(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.exitApp();
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully exited application'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to exit application: $e';
    }
  }

  // Widget interaction methods
  @override
  Future<GenericResponse> tapWidgetByKey(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.tapWidgetByKey(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully tapped widget with key: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to tap widget by key: $e';
    }
  }

  @override
  Future<GenericResponse> tapWidgetByText(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.tapWidgetByText(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully tapped widget with text: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to tap widget by text: $e';
    }
  }

  @override
  Future<GenericResponse> tapWidgetByType(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.tapWidgetByType(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully tapped widget of type: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to tap widget by type: $e';
    }
  }

  @override
  Future<GenericResponse> enterText(
      ServiceCall call, EnterTextRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.enterTextByKey(request.text, request.keyValue);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully entered text: ${request.text} into widget with key: ${request.keyValue}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to enter text: $e';
    }
  }

  @override
  Future<GenericResponse> enterTextByKey(
      ServiceCall call, EnterTextKeyRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.enterTextByKey(request.text, request.keyValue);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully entered text: ${request.text} into widget with key: ${request.keyValue}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to enter text by key: $e';
    }
  }

  @override
  Future<GenericResponse> enterTextByType(
      ServiceCall call, EnterTextTypeRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result =
          await _tool.enterTextByType(request.text, request.widgetType);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully entered text: ${request.text} into widget of type: ${request.widgetType}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to enter text by type: $e';
    }
  }

  @override
  Future<GenericResponse> enterTextByText(
      ServiceCall call, EnterTextTextRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result =
          await _tool.enterTextByText(request.text, request.widgetText);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully entered text: ${request.text} into widget with text: ${request.widgetText}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to enter text by text: $e';
    }
  }

  @override
  Future<GenericResponse> enterTextByTooltip(
      ServiceCall call, EnterTextTooltipRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result =
          await _tool.enterTextByTooltip(request.text, request.tooltip);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully entered text: ${request.text} into widget with tooltip: ${request.tooltip}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to enter text by tooltip: $e';
    }
  }

  @override
  Future<GenericResponse> enterTextByAncestorAndDescendant(
      ServiceCall call, EnterTextAncestorDescendantRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.enterTextByAncestorAndDescendant(
        text: request.text,
        ancestorType: request.ancestorType,
        descendantType: request.descendantType,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully entered text: ${request.text} into ${request.descendantType} inside ${request.ancestorType}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to enter text by ancestor and descendant: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByKey(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByKey(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget with key: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by key: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByType(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByType(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget of type: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by type: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByText(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByText(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget with text: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by text: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByTooltip(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByTooltip(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget with tooltip: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by tooltip: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByAncestorAndDescendant(
      ServiceCall call, AncestorDescendantRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByAncestorAndDescendant(
        ancestorType: request.ancestorType,
        descendantType: request.descendantType,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down ${request.descendantType} inside ${request.ancestorType}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by ancestor and descendant: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByKey(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByKey(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully scrolled up widget with key: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by key: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByType(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByType(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully scrolled up widget of type: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by type: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByText(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByText(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up widget with text: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by text: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByTooltip(
      ServiceCall call, StringValueRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByTooltip(request.value);
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up widget with tooltip: ${request.value}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by tooltip: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByAncestorAndDescendant(
      ServiceCall call, AncestorDescendantRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByAncestorAndDescendant(
        ancestorType: request.ancestorType,
        descendantType: request.descendantType,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up ${request.descendantType} inside ${request.ancestorType}'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by ancestor and descendant: $e';
    }
  }

  @override
  Future<GenericResponse> addPubRootDirectories(
      ServiceCall call, StringListRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.addPubRootDirectories(request.values.toList());
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message = 'Successfully added pub root directories'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to add pub root directories: $e';
    }
  }

  @override
  Future<GenericResponse> disposeAllGroups(
      ServiceCall call, ObjectGroupRequest request) async {
    return _handleGenericResponse(
      () => _tool.disposeAllGroups(request.objectGroup),
      'Successfully disposed all groups',
      'Failed to dispose all groups',
    );
  }

  @override
  Future<GenericResponse> disposeGroup(
      ServiceCall call, ObjectGroupRequest request) async {
    return _handleGenericResponse(
      () => _tool.disposeGroup(request.objectGroup),
      'Successfully disposed group: ${request.objectGroup}',
      'Failed to dispose group',
    );
  }

  @override
  Future<GenericResponse> disposeId(
      ServiceCall call, DisposeIdRequest request) async {
    return _handleGenericResponse(
      () => _tool.disposeId(request.objectGroup, request.objectId),
      'Successfully disposed object: ${request.objectId}',
      'Failed to dispose object',
    );
  }

  @override
  Future<GenericResponse> getChildren(
      ServiceCall call, WidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getChildren(request.objectGroup, request.widgetId),
      'Successfully retrieved children for widget: ${request.widgetId}',
      'Failed to get children',
    );
  }

  @override
  Future<GenericResponse> getChildrenDetailsSubtree(
      ServiceCall call, WidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getChildrenDetailsSubtree(
          request.objectGroup, request.widgetId),
      'Successfully retrieved children details subtree for widget: ${request.widgetId}',
      'Failed to get children details subtree',
    );
  }

  @override
  Future<GenericResponse> getChildrenSummaryTree(
      ServiceCall call, WidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getChildrenSummaryTree(request.objectGroup, request.widgetId),
      'Successfully retrieved children summary tree for widget: ${request.widgetId}',
      'Failed to get children summary tree',
    );
  }

  @override
  Future<GenericResponse> getProperties(
      ServiceCall call, WidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getProperties(request.objectGroup, request.widgetId),
      'Successfully retrieved properties for widget: ${request.widgetId}',
      'Failed to get properties',
    );
  }

  @override
  Future<GenericResponse> getDetailsSubtree(
      ServiceCall call, DetailSubtreeRequest request) async {
    return _handleGenericResponse(
      () => _tool.getDetailsSubtree(request.objectGroup, request.widgetId,
          subtreeDepth: request.subtreeDepth),
      'Successfully retrieved details subtree for widget: ${request.widgetId}',
      'Failed to get details subtree',
    );
  }

  @override
  Future<GenericResponse> getLayoutExplorerNode(
      ServiceCall call, LayoutExplorerRequest request) async {
    return _handleGenericResponse(
      () => _tool.getLayoutExplorerNode(request.objectGroup,
          id: request.widgetId, subtreeDepth: request.subtreeDepth),
      'Successfully retrieved layout explorer node for widget: ${request.widgetId}',
      'Failed to get layout explorer node',
    );
  }

  @override
  Future<GenericResponse> getParentChain(
      ServiceCall call, WidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getParentChain(request.objectGroup, request.widgetId),
      'Successfully retrieved parent chain for widget: ${request.widgetId}',
      'Failed to get parent chain',
    );
  }

  @override
  Future<StringListResponse> getPubRootDirectories(
      ServiceCall call, EmptyRequest request) async {
    if (!_isConnected) {
      return StringListResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.getPubRootDirectories();
      final jsonData = result.json;
      if (jsonData != null && jsonData['type'] == 'StringList') {
        final values =
            (jsonData['value'] as List<dynamic>?)?.cast<String>() ?? [];
        return StringListResponse()
          ..success = true
          ..message = 'Successfully retrieved pub root directories'
          ..values.addAll(values);
      } else {
        return StringListResponse()
          ..success = false
          ..message = 'Failed to parse pub root directories response';
      }
    } catch (e) {
      return StringListResponse()
        ..success = false
        ..message = 'Failed to get pub root directories: $e';
    }
  }

  @override
  Future<GenericResponse> getRootWidget(
      ServiceCall call, ObjectGroupRequest request) async {
    return _handleGenericResponse(
      () => _tool.getRootWidget(request.objectGroup),
      'Successfully retrieved root widget',
      'Failed to get root widget',
    );
  }

  @override
  Future<GenericResponse> getRootWidgetSummaryTree(
      ServiceCall call, ObjectGroupRequest request) async {
    return _handleGenericResponse(
      () => _tool.getRootWidgetSummaryTree(request.objectGroup),
      'Successfully retrieved root widget summary tree',
      'Failed to get root widget summary tree',
    );
  }

  @override
  Future<GenericResponse> getRootWidgetSummaryTreeWithPreviews(
      ServiceCall call, ObjectGroupRequest request) async {
    return _handleGenericResponse(
      () => _tool.getRootWidgetSummaryTreeWithPreviews(request.objectGroup),
      'Successfully retrieved root widget summary tree with previews',
      'Failed to get root widget summary tree with previews',
    );
  }

  @override
  Future<GenericResponse> getSelectedSummaryWidget(
      ServiceCall call, SelectedWidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getSelectedSummaryWidget(request.objectGroup,
          previousSelectionId: request.previousSelectionId),
      'Successfully retrieved selected summary widget',
      'Failed to get selected summary widget',
    );
  }

  @override
  Future<GenericResponse> getSelectedWidget(
      ServiceCall call, SelectedWidgetRequest request) async {
    return _handleGenericResponse(
      () => _tool.getSelectedWidget(request.objectGroup,
          previousSelectionId: request.previousSelectionId),
      'Successfully retrieved selected widget',
      'Failed to get selected widget',
    );
  }

  @override
  Future<GenericResponse> isWidgetCreationTracked(
      ServiceCall call, EmptyRequest request) async {
    return _handleGenericResponse(
      () => _tool.isWidgetCreationTracked(),
      'Successfully checked widget creation tracking status',
      'Failed to check widget creation tracking status',
    );
  }

  @override
  Future<GenericResponse> isWidgetTreeReady(
      ServiceCall call, EmptyRequest request) async {
    return _handleGenericResponse(
      () => _tool.isWidgetTreeReady(),
      'Successfully checked widget tree readiness',
      'Failed to check widget tree readiness',
    );
  }

  @override
  Future<GenericResponse> removePubRootDirectories(
      ServiceCall call, StringListRequest request) async {
    return _handleGenericResponse(
      () => _tool.removePubRootDirectories(request.values.toList()),
      'Successfully removed pub root directories',
      'Failed to remove pub root directories',
    );
  }

  @override
  Future<GenericResponse> screenshot(
      ServiceCall call, ScreenshotRequest request) async {
    return _handleGenericResponse(
      () => _tool.screenshot(
        request.widgetId,
        request.width,
        request.height,
        margin: request.margin,
        maxPixelRatio: request.maxPixelRatio,
        debugPaint: request.debugPaint,
      ),
      'Successfully captured screenshot for widget: ${request.widgetId}',
      'Failed to capture screenshot',
    );
  }

  @override
  Future<GenericResponse> setBrightnessOverride(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.setBrightnessOverride(request.value),
      'Successfully set brightness override to ${request.value}',
      'Failed to set brightness override',
    );
  }

  @override
  Future<GenericResponse> setDevToolsServerAddress(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.setDevToolsServerAddress(request.value),
      'Successfully set DevTools server address to ${request.value}',
      'Failed to set DevTools server address',
    );
  }

  @override
  Future<GenericResponse> setFlexFactor(
      ServiceCall call, FlexFactorRequest request) async {
    return _handleGenericResponse(
      () => _tool.setFlexFactor(request.widgetId, request.flexFactor),
      'Successfully set flex factor for widget: ${request.widgetId}',
      'Failed to set flex factor',
    );
  }

  @override
  Future<GenericResponse> setFlexFit(
      ServiceCall call, FlexFitRequest request) async {
    return _handleGenericResponse(
      () => _tool.setFlexFit(request.widgetId, request.flexFit),
      'Successfully set flex fit for widget: ${request.widgetId}',
      'Failed to set flex fit',
    );
  }

  @override
  Future<GenericResponse> setFlexProperties(
      ServiceCall call, FlexPropertiesRequest request) async {
    return _handleGenericResponse(
      () => _tool.setFlexProperties(request.widgetId,
          mainAxisAlignment: request.mainAxisAlignment,
          crossAxisAlignment: request.crossAxisAlignment),
      'Successfully set flex properties for widget: ${request.widgetId}',
      'Failed to set flex properties',
    );
  }

  @override
  Future<GenericResponse> setPlatformOverride(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.setPlatformOverride(request.value),
      'Successfully set platform override to ${request.value}',
      'Failed to set platform override',
    );
  }

  @override
  Future<GenericResponse> setPubRootDirectories(
      ServiceCall call, StringListRequest request) async {
    return _handleGenericResponse(
      () => _tool.setPubRootDirectories(request.values.toList()),
      'Successfully set pub root directories',
      'Failed to set pub root directories',
    );
  }

  @override
  Future<GenericResponse> setSelectionById(
      ServiceCall call, SelectionByIdRequest request) async {
    return _handleGenericResponse(
      () => _tool.setSelectionById(request.objectGroup, request.objectId),
      'Successfully set selection to object: ${request.objectId}',
      'Failed to set selection by ID',
    );
  }

  @override
  Future<GenericResponse> setVmServiceUri(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.setVmServiceUri(request.value),
      'Successfully set VM service URI to ${request.value}',
      'Failed to set VM service URI',
    );
  }

  @override
  Future<GenericResponse> tapWidgetByAncestorAndDescendant(
      ServiceCall call, AncestorDescendantRequest request) async {
    return _handleGenericResponse(
      () => _tool.tapWidgetByAncestorAndDescendant(
          ancestorType: request.ancestorType,
          descendantType: request.descendantType),
      'Successfully tapped widget by ancestor and descendant',
      'Failed to tap widget by ancestor and descendant',
    );
  }

  @override
  Future<GenericResponse> tapWidgetByTooltip(
      ServiceCall call, StringValueRequest request) async {
    return _handleGenericResponse(
      () => _tool.tapWidgetByTooltip(request.value),
      'Successfully tapped widget with tooltip: ${request.value}',
      'Failed to tap widget by tooltip',
    );
  }

  @override
  Future<GenericResponse> scrollDownByKeyExtended(
      ServiceCall call, ScrollKeyRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByKeyExtended(
        keyValue: request.keyValue,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget with key: ${request.keyValue} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by key extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByTypeExtended(
      ServiceCall call, ScrollTypeRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByTypeExtended(
        widgetType: request.widgetType,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget of type: ${request.widgetType} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by type extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByTextExtended(
      ServiceCall call, ScrollTextRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByTextExtended(
        text: request.text,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget with text: ${request.text} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by text extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByTooltipExtended(
      ServiceCall call, ScrollTooltipRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByTooltipExtended(
        tooltip: request.tooltip,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down widget with tooltip: ${request.tooltip} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll down by tooltip extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollDownByAncestorAndDescendantExtended(
      ServiceCall call, ScrollAncestorDescendantRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollDownByAncestorAndDescendantExtended(
        ancestorType: request.ancestorType,
        descendantType: request.descendantType,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled down ${request.descendantType} inside ${request.ancestorType} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message =
            'Failed to scroll down by ancestor and descendant extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByKeyExtended(
      ServiceCall call, ScrollKeyRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByKeyExtended(
        keyValue: request.keyValue,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up widget with key: ${request.keyValue} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by key extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByTypeExtended(
      ServiceCall call, ScrollTypeRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByTypeExtended(
        widgetType: request.widgetType,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up widget of type: ${request.widgetType} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by type extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByTextExtended(
      ServiceCall call, ScrollTextRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByTextExtended(
        text: request.text,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up widget with text: ${request.text} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by text extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByTooltipExtended(
      ServiceCall call, ScrollTooltipRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByTooltipExtended(
        tooltip: request.tooltip,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up widget with tooltip: ${request.tooltip} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll up by tooltip extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollUpByAncestorAndDescendantExtended(
      ServiceCall call, ScrollAncestorDescendantRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollUpByAncestorAndDescendantExtended(
        ancestorType: request.ancestorType,
        descendantType: request.descendantType,
        dx: request.dx,
        dy: request.dy,
        duration: Duration(microseconds: request.durationMicroseconds.toInt()),
        frequency: request.frequency,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled up ${request.descendantType} inside ${request.ancestorType} (dx: ${request.dx}, dy: ${request.dy})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message =
            'Failed to scroll up by ancestor and descendant extended: $e';
    }
  }

  @override
  Future<GenericResponse> scrollIntoViewByKey(
      ServiceCall call, ScrollIntoViewKeyRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollIntoViewByKey(
        request.keyValue,
        alignment: request.alignment,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled widget with key: ${request.keyValue} into view (alignment: ${request.alignment})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll into view by key: $e';
    }
  }

  @override
  Future<GenericResponse> scrollIntoViewByType(
      ServiceCall call, ScrollIntoViewTypeRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollIntoViewByType(
        request.widgetType,
        alignment: request.alignment,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled widget of type: ${request.widgetType} into view (alignment: ${request.alignment})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll into view by type: $e';
    }
  }

  @override
  Future<GenericResponse> scrollIntoViewByText(
      ServiceCall call, ScrollIntoViewTextRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollIntoViewByText(
        request.text,
        alignment: request.alignment,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled widget with text: ${request.text} into view (alignment: ${request.alignment})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll into view by text: $e';
    }
  }

  @override
  Future<GenericResponse> scrollIntoViewByTooltip(
      ServiceCall call, ScrollIntoViewTooltipRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollIntoViewByTooltip(
        request.tooltip,
        alignment: request.alignment,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled widget with tooltip: ${request.tooltip} into view (alignment: ${request.alignment})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll into view by tooltip: $e';
    }
  }

  @override
  Future<GenericResponse> scrollIntoViewByAncestorAndDescendant(
      ServiceCall call, ScrollIntoViewAncestorDescendantRequest request) async {
    if (!_isConnected) {
      return GenericResponse()
        ..success = false
        ..message = 'Not connected to a Flutter application';
    }

    try {
      final result = await _tool.scrollIntoViewByAncestorAndDescendant(
        ancestorType: request.ancestorType,
        descendantType: request.descendantType,
        alignment: request.alignment,
      );
      final jsonData = _responseJsonToString(result);
      return GenericResponse()
        ..success = true
        ..message =
            'Successfully scrolled ${request.descendantType} inside ${request.ancestorType} into view (alignment: ${request.alignment})'
        ..data = jsonData ?? '';
    } catch (e) {
      return GenericResponse()
        ..success = false
        ..message = 'Failed to scroll into view by ancestor and descendant: $e';
    }
  }
}

class GrpcServer {
  Server? _server;

  Future<void> start({int port = 50051}) async {
    final service = DartVmServiceGrpcService();
    _server = Server([service]);
    await _server!.serve(port: port);
    print('🚀 Dart VM Service gRPC server started on port $port');
  }

  Future<void> stop() async {
    await _server?.shutdown();
    print('Dart VM Service gRPC server stopped');
  }
}
