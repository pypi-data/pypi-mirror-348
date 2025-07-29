import 'package:vm_service/vm_service.dart';
import 'package:vm_service/vm_service_io.dart';
import 'dart:io';
import 'flutter_extension_utils.dart';
import 'flutter_finder_extension_utils.dart';

/// Tool that exposes the Dart VM Service API.
///
/// This tool is used to interact with the Dart VM Service API.
/// It is used to get the current screen widgets, enable all highlights,
/// toggle debug paint, performance overlay, repaint rainbow, and time dilation.
/// It also allows the agent to tap on widgets by key value or text.
///
///
class DartVmServiceTool {
  VmService? _vmService;
  FlutterExtensionUtils? _extensionUtils;
  FlutterFinderExtensionUtils? _finderUtils;
  bool _isRunning = false;

  Future<void> start(String vmServiceUri) async {
    print('🔍 Connecting to application...');

    try {
      // Connect to the VM service
      _vmService = await vmServiceConnectUri(vmServiceUri);
      _extensionUtils = FlutterExtensionUtils(_vmService!);
      _finderUtils = FlutterFinderExtensionUtils(vmService: _vmService!);

      _stop();
    } catch (e, stackTrace) {
      print('Dart VM Service Error: $e');
      print('Stack trace: $stackTrace');
      exit(1);
    }
  }

  // Helper method to get the main isolate
  Future<String> _getMainIsolateId() async {
    if (_vmService == null) {
      throw Exception('VM Service not connected. Call start() first.');
    }

    final vm = await _vmService!.getVM();
    final mainIsolate = vm.isolates!.first;
    return mainIsolate.id!;
  }

  /*
   * Flutter Extension Utils Methods
   */

  /// Get the display refresh rate for a view
  Future<Response> getDisplayRefreshRate(String viewId) async {
    _checkConnection();
    final response = await _extensionUtils!.getDisplayRefreshRate(viewId);
    print('Got display refresh rate for view: $viewId');
    return response;
  }

  /// Toggle debug paint
  Future<Response> toggleDebugPaint(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.debugPaint(isolateId, enabled: enable);
    print('Debug paint ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle repaint rainbow
  Future<Response> toggleRepaintRainbow(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.repaintRainbow(isolateId, enabled: enable);
    print('Repaint rainbow ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle performance overlay
  Future<Response> togglePerformanceOverlay(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .showPerformanceOverlay(isolateId, enabled: enable);
    print('Performance overlay ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Dump the widget tree
  Future<Response> dumpWidgetTree() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.debugDumpApp(isolateId);
    print('Widget tree dumped');
    return response;
  }

  /// Set time dilation
  Future<Response> setTimeDilation(double value) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.timeDilation(isolateId, value: value.toString());
    print('Time dilation set to $value');
    return response;
  }

  /// List all Flutter views
  Future<Response> listViews() async {
    _checkConnection();
    final response = await _extensionUtils!.listViews();
    print('Flutter views listed');
    return response;
  }

  /// Toggle oversized images
  Future<Response> toggleOversizedImages(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.invertOversizedImage(isolateId, enabled: enable);
    print('Oversized images ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle baseline painting
  Future<Response> toggleBaselinePainting(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .debugPaintBaselinesEnabled(isolateId, enabled: enable);
    print('Baseline painting ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Dump the layer tree
  Future<Response> dumpLayerTree() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.debugDumpLayerTree(isolateId);
    print('Layer tree dumped');
    return response;
  }

  /// Toggle disabling of physical shape layers
  Future<Response> toggleDisablePhysicalShapeLayers(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .debugDisablePhysicalShapeLayers(isolateId, enabled: enable);
    print('Physical shape layers ${enable ? 'disabled' : 'enabled'}');
    return response;
  }

  /// Toggle disabling of opacity layers
  Future<Response> toggleDisableOpacityLayers(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .debugDisableOpacityLayers(isolateId, enabled: enable);
    print('Opacity layers ${enable ? 'disabled' : 'enabled'}');
    return response;
  }

  /// Dump the render tree
  Future<Response> dumpRenderTree() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.debugDumpRenderTree(isolateId);
    print('Render tree dumped');
    return response;
  }

  /// Dump the semantics tree in traversal order
  Future<Response> dumpSemanticsTreeInTraversalOrder() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .debugDumpSemanticsTreeInTraversalOrder(isolateId);
    print('Semantics tree dumped in traversal order');
    return response;
  }

  /// Dump the semantics tree in inverse hit test order
  Future<Response> dumpSemanticsTreeInInverseHitTestOrder() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .debugDumpSemanticsTreeInInverseHitTestOrder(isolateId);
    print('Semantics tree dumped in inverse hit test order');
    return response;
  }

  /// Toggle profiling of render object paints
  Future<Response> toggleProfileRenderObjectPaints(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .profileRenderObjectPaints(isolateId, enabled: enable);
    print(
        'Profiling of render object paints ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle profiling of render object layouts
  Future<Response> toggleProfileRenderObjectLayouts(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .profileRenderObjectLayouts(isolateId, enabled: enable);
    print(
        'Profiling of render object layouts ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle profiling of platform channels
  Future<Response> toggleProfilePlatformChannels(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .profilePlatformChannels(isolateId, enabled: enable);
    print('Profiling of platform channels ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle profiling of user widget builds
  Future<Response> toggleProfileUserWidgetBuilds(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .profileUserWidgetBuilds(isolateId, enabled: enable);
    print('Profiling of user widget builds ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Sets or queries the first frame event status
  Future<Response> didSendFirstFrameEvent(bool value) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .didSendFirstFrameEvent(isolateId, enabled: value);
    print('First frame event status set to: $value');
    return response;
  }

  /// Sets or queries the first frame rasterized event status
  Future<Response> didSendFirstFrameRasterizedEvent(String value) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .didSendFirstFrameRasterizedEvent(isolateId, enabled: value);
    print('First frame rasterized event status set to: $value');
    return response;
  }

  /// Evict assets from cache
  Future<Response> evictAssets(String assetPath) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.evict(isolateId, value: assetPath);
    print('Asset evicted: $assetPath');
    return response;
  }

  /// Trigger reassemble of the application
  Future<Response> reassemble() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.reassemble(isolateId);
    print('Application reassembled');
    return response;
  }

  /// Exit the application
  Future<Response> exitApp() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.exit(isolateId);
    print('Application exit requested');
    return response;
  }

  /// Set or get the connected VM service URI
  Future<Response> setVmServiceUri(String uri) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.connectedVmServiceUri(isolateId, value: uri);
    print('VM service URI set to: $uri');
    return response;
  }

  /// Set or get the active DevTools server address
  Future<Response> setDevToolsServerAddress(String address) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .activeDevToolsServerAddress(isolateId, value: address);
    print('DevTools server address set to: $address');
    return response;
  }

  /// Override the platform
  Future<Response> setPlatformOverride(String platform) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.platformOverride(isolateId, value: platform);
    print('Platform overridden to: $platform');
    return response;
  }

  /// Override the brightness
  Future<Response> setBrightnessOverride(String brightness) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.brightnessOverride(isolateId, value: brightness);
    print('Brightness overridden to: $brightness');
    return response;
  }

  /// Dump the focus tree
  Future<Response> dumpFocusTree() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.debugDumpFocusTree(isolateId);
    print('Focus tree dumped');
    return response;
  }

  /// Toggle the debug banner
  Future<Response> toggleDebugBanner(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.debugAllowBanner(isolateId, enabled: enable);
    print('Debug banner ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle structured error reporting
  Future<Response> toggleStructuredErrors(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.structuredErrors(isolateId, enabled: enable);
    print('Structured error reporting ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle profiling of widget builds
  Future<Response> toggleProfileWidgetBuilds(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.profileWidgetBuilds(isolateId, enabled: enable);
    print('Profiling of widget builds ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /*
   * Flutter Inspector Methods
   */

  /// Toggle inspector visibility
  Future<Response> toggleInspector(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.show(isolateId, enabled: enable);
    print('Inspector ${enable ? 'shown' : 'hidden'}');
    return response;
  }

  /// Toggle tracking of widget rebuilds
  Future<Response> toggleTrackRebuildWidgets(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .trackRebuildDirtyWidgets(isolateId, enabled: enable);
    print('Widget rebuild tracking ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Toggle tracking of widget repaints
  Future<Response> toggleTrackRepaintWidgets(bool enable) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.trackRepaintWidgets(isolateId, enabled: enable);
    print('Widget repaint tracking ${enable ? 'enabled' : 'disabled'}');
    return response;
  }

  /// Dispose all object groups
  Future<Response> disposeAllGroups(String objectGroup) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.disposeAllGroups(isolateId, objectGroup);
    print('All groups disposed');
    return response;
  }

  /// Dispose a specific object group
  Future<Response> disposeGroup(String objectGroup) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.disposeGroup(isolateId, objectGroup);
    print('Group disposed: $objectGroup');
    return response;
  }

  /// Check if the widget tree is ready
  Future<Response> isWidgetTreeReady() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.isWidgetTreeReady(isolateId);
    print('Widget tree ready status checked');
    return response;
  }

  /// Dispose a specific object by ID
  Future<Response> disposeId(String objectGroup, String objectId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .disposeId(isolateId, objectGroup, objectId: objectId);
    print('Object disposed: $objectId');
    return response;
  }

  /// Set pub root directories
  Future<Response> setPubRootDirectories(List<String> directories) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.setPubRootDirectories(isolateId, directories);
    print('Pub root directories set');
    return response;
  }

  /// Add pub root directories
  Future<Response> addPubRootDirectories(List<String> directories) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.addPubRootDirectories(isolateId, directories);
    print('Pub root directories added');
    return response;
  }

  /// Remove pub root directories
  Future<Response> removePubRootDirectories(List<String> directories) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.removePubRootDirectories(isolateId, directories);
    print('Pub root directories removed');
    return response;
  }

  /// Get the list of pub root directories
  Future<Response> getPubRootDirectories() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getPubRootDirectories(isolateId);
    print('Pub root directories retrieved');
    return response;
  }

  /// Set widget selection by ID
  Future<Response> setSelectionById(String objectGroup, String objectId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .setSelectionById(isolateId, objectGroup, objectId: objectId);
    print('Widget selected: $objectId');
    return response;
  }

  /// Get the parent chain of a widget
  Future<Response> getParentChain(String objectGroup, String objectId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .getParentChain(isolateId, objectGroup, objectId: objectId);
    print('Parent chain retrieved for: $objectId');
    return response;
  }

  /// Get properties of a diagnosticable object
  Future<Response> getProperties(
      String objectGroup, String diagnosticableId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getProperties(
        isolateId, objectGroup,
        diagnosticableId: diagnosticableId);
    print('Properties retrieved for: $diagnosticableId');
    return response;
  }

  /// Get children of a diagnosticable object
  Future<Response> getChildren(
      String objectGroup, String diagnosticableId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getChildren(isolateId, objectGroup,
        diagnosticableId: diagnosticableId);
    print('Children retrieved for: $diagnosticableId');
    return response;
  }

  /// Get summary tree of children of a diagnosticable object
  Future<Response> getChildrenSummaryTree(
      String objectGroup, String diagnosticableId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getChildrenSummaryTree(
        isolateId, objectGroup,
        diagnosticableId: diagnosticableId);
    print('Children summary tree retrieved for: $diagnosticableId');
    return response;
  }

  /// Get details subtree of children of a diagnosticable object
  Future<Response> getChildrenDetailsSubtree(
      String objectGroup, String diagnosticableId) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getChildrenDetailsSubtree(
        isolateId, objectGroup,
        diagnosticableId: diagnosticableId);
    print('Children details subtree retrieved for: $diagnosticableId');
    return response;
  }

  /// Get the root widget
  Future<Response> getRootWidget(String objectGroup) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .getRootWidget(isolateId, objectGroup: objectGroup);
    print('Root widget retrieved');
    return response;
  }

  /// Get the summary tree of the root widget
  Future<Response> getRootWidgetSummaryTree(String objectGroup) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .getRootWidgetSummaryTree(isolateId, objectGroup: objectGroup);
    print('Root widget summary tree retrieved');
    return response;
  }

  /// Get the summary tree of the root widget with previews
  Future<Response> getRootWidgetSummaryTreeWithPreviews(
      String objectGroup) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .getRootWidgetSummaryTreeWithPreviews(isolateId,
            objectGroup: objectGroup);
    print('Root widget summary tree with previews retrieved');
    return response;
  }

  /// Get details subtree of a diagnosticable object
  Future<Response> getDetailsSubtree(
      String objectGroup, String diagnosticableId,
      {int? subtreeDepth}) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getDetailsSubtree(
        isolateId, objectGroup,
        diagnosticableId: diagnosticableId, subtreeDepth: subtreeDepth);
    print('Details subtree retrieved for: $diagnosticableId');
    return response;
  }

  /// Get the selected widget
  Future<Response> getSelectedWidget(String objectGroup,
      {String? previousSelectionId}) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getSelectedWidget(
        isolateId, objectGroup,
        previousSelectionId: previousSelectionId);
    print('Selected widget retrieved');
    return response;
  }

  /// Get the selected summary widget
  Future<Response> getSelectedSummaryWidget(String objectGroup,
      {String? previousSelectionId}) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getSelectedSummaryWidget(
        isolateId, objectGroup,
        previousSelectionId: previousSelectionId);
    print('Selected summary widget retrieved');
    return response;
  }

  /// Check if widget creation is tracked
  Future<Response> isWidgetCreationTracked() async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.isWidgetCreationTracked(isolateId);
    print('Widget creation tracking status checked');
    return response;
  }

  /// Take a screenshot of a widget
  Future<Response> screenshot(String id, double width, double height,
      {double? margin, double? maxPixelRatio, bool? debugPaint}) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.screenshot(
        isolateId, id, width, height,
        margin: margin, maxPixelRatio: maxPixelRatio, debugPaint: debugPaint);
    print('Screenshot taken for widget: $id');
    return response;
  }

  /// Get the layout explorer node
  Future<Response> getLayoutExplorerNode(String objectGroup,
      {String? id, int? subtreeDepth}) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.getLayoutExplorerNode(
        isolateId, objectGroup,
        id: id, subtreeDepth: subtreeDepth);
    print('Layout explorer node retrieved');
    return response;
  }

  /// Set flex fit on a widget
  Future<Response> setFlexFit(String id, String flexFit) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response =
        await _extensionUtils!.setFlexFit(isolateId, id: id, flexFit: flexFit);
    print('Flex fit set to $flexFit for widget: $id');
    return response;
  }

  /// Set flex factor on a widget
  Future<Response> setFlexFactor(String id, int flexFactor) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!
        .setFlexFactor(isolateId, id: id, flexFactor: flexFactor);
    print('Flex factor set to $flexFactor for widget: $id');
    return response;
  }

  /// Set flex properties on a widget
  Future<Response> setFlexProperties(String id,
      {String? mainAxisAlignment, String? crossAxisAlignment}) async {
    _checkConnection();
    final isolateId = await _getMainIsolateId();
    final response = await _extensionUtils!.setFlexProperties(isolateId,
        id: id,
        mainAxisAlignment: mainAxisAlignment,
        crossAxisAlignment: crossAxisAlignment);
    print('Flex properties set for widget: $id');
    return response;
  }

  /*
   * Flutter Finder Extension Utils Methods
   */

  /// Tap a widget by its key
  Future<Response> tapWidgetByKey(String keyValue) async {
    _checkConnection();
    final response = await _finderUtils!.tapWidgetByKey(keyValue);
    print('🤖 Tapped widget with key: $keyValue');
    return response;
  }

  /// Tap a widget by its text
  Future<Response> tapWidgetByText(String text) async {
    _checkConnection();
    final response = await _finderUtils!.tapWidgetByText(text);
    print('🤖 Tapped widget with text: $text');
    return response;
  }

  /// Tap a widget by its type
  Future<Response> tapWidgetByType(String widgetType) async {
    _checkConnection();
    final response = await _finderUtils!.tapWidgetByType(widgetType);
    print('🤖 Tapped widget of type: $widgetType');
    return response;
  }

  /// Tap a widget by its ancestor and descendant
  Future<Response> tapWidgetByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.tapWidgetByAncestorAndDescendant(
      ancestorType: ancestorType,
      descendantType: descendantType,
    );
    print('🤖 Tapped $descendantType inside $ancestorType');
    return response;
  }

  /// Tap a widget by its tooltip
  Future<Response> tapWidgetByTooltip(String tooltip) async {
    _checkConnection();
    final response = await _finderUtils!.tapWidgetByTooltip(tooltip);
    print('🤖 Tapped widget with tooltip: $tooltip');
    return response;
  }

  /// Enter text into a widget by its key
  Future<Response> enterTextByKey(String text, String keyValue) async {
    _checkConnection();
    final response = await _finderUtils!.enterTextByKey(text, keyValue);
    print('🤖 Entered text "$text" into widget with key: $keyValue');
    return response;
  }

  /// Enter text into a widget by its text
  Future<Response> enterTextByText(String text, String widgetText) async {
    _checkConnection();
    final response = await _finderUtils!.enterTextByText(text, widgetText);
    print('🤖 Entered text "$text" into widget with text: $widgetText');
    return response;
  }

  /// Enter text into a widget by its type
  Future<Response> enterTextByType(String text, String widgetType) async {
    _checkConnection();
    final response = await _finderUtils!.enterTextByType(text, widgetType);
    print('🤖 Entered text "$text" into widget of type: $widgetType');
    return response;
  }

  /// Enter text into a widget by its tooltip
  Future<Response> enterTextByTooltip(String text, String tooltip) async {
    _checkConnection();
    final response = await _finderUtils!.enterTextByTooltip(text, tooltip);
    print('🤖 Entered text "$text" into widget with tooltip: $tooltip');
    return response;
  }

  /// Enter text into a widget identified by ancestor and descendant
  Future<Response> enterTextByAncestorAndDescendant({
    required String text,
    required String ancestorType,
    required String descendantType,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.enterTextByAncestorAndDescendant(
      text: text,
      ancestorType: ancestorType,
      descendantType: descendantType,
    );
    print('🤖 Entered text "$text" into $descendantType inside $ancestorType');
    return response;
  }

  /// Scroll down a widget by its key
  Future<Response> scrollDownByKey(String keyValue) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByKey(keyValue);
    print('🤖 Scrolled down widget with key: $keyValue');
    return response;
  }

  /// Scroll down a widget by its type
  Future<Response> scrollDownByType(String widgetType) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByType(widgetType);
    print('🤖 Scrolled down widget of type: $widgetType');
    return response;
  }

  /// Scroll down a widget by its text
  Future<Response> scrollDownByText(String text) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByText(text);
    print('🤖 Scrolled down widget with text: $text');
    return response;
  }

  /// Scroll down a widget by its tooltip
  Future<Response> scrollDownByTooltip(String tooltip) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByTooltip(tooltip);
    print('🤖 Scrolled down widget with tooltip: $tooltip');
    return response;
  }

  /// Scroll down a widget identified by ancestor and descendant
  Future<Response> scrollDownByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByAncestorAndDescendant(
      ancestorType: ancestorType,
      descendantType: descendantType,
    );
    print('🤖 Scrolled down $descendantType inside $ancestorType');
    return response;
  }

  /// Scroll up a widget by its key
  Future<Response> scrollUpByKey(String keyValue) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByKey(keyValue);
    print('🤖 Scrolled up widget with key: $keyValue');
    return response;
  }

  /// Scroll up a widget by its type
  Future<Response> scrollUpByType(String widgetType) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByType(widgetType);
    print('🤖 Scrolled up widget of type: $widgetType');
    return response;
  }

  /// Scroll up a widget by its text
  Future<Response> scrollUpByText(String text) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByText(text);
    print('🤖 Scrolled up widget with text: $text');
    return response;
  }

  /// Scroll up a widget by its tooltip
  Future<Response> scrollUpByTooltip(String tooltip) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByTooltip(tooltip);
    print('🤖 Scrolled up widget with tooltip: $tooltip');
    return response;
  }

  /// Scroll up a widget identified by ancestor and descendant
  Future<Response> scrollUpByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByAncestorAndDescendant(
      ancestorType: ancestorType,
      descendantType: descendantType,
    );
    print('🤖 Scrolled up $descendantType inside $ancestorType');
    return response;
  }

  /// Scroll down a widget by its key with extended parameters
  Future<Response> scrollDownByKeyExtended({
    required String keyValue,
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByKey(
      keyValue,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled down widget with key: $keyValue (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll down a widget by its type with extended parameters
  Future<Response> scrollDownByTypeExtended({
    required String widgetType,
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByType(
      widgetType,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled down widget of type: $widgetType (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll down a widget by its text with extended parameters
  Future<Response> scrollDownByTextExtended({
    required String text,
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByText(
      text,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled down widget with text: $text (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll down a widget by its tooltip with extended parameters
  Future<Response> scrollDownByTooltipExtended({
    required String tooltip,
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByTooltip(
      tooltip,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled down widget with tooltip: $tooltip (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll down a widget identified by ancestor and descendant with extended parameters
  Future<Response> scrollDownByAncestorAndDescendantExtended({
    required String ancestorType,
    required String descendantType,
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollDownByAncestorAndDescendant(
      ancestorType: ancestorType,
      descendantType: descendantType,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print(
        '🤖 Scrolled down $descendantType inside $ancestorType (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll up a widget by its key with extended parameters
  Future<Response> scrollUpByKeyExtended({
    required String keyValue,
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByKey(
      keyValue,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled up widget with key: $keyValue (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll up a widget by its type with extended parameters
  Future<Response> scrollUpByTypeExtended({
    required String widgetType,
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByType(
      widgetType,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled up widget of type: $widgetType (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll up a widget by its text with extended parameters
  Future<Response> scrollUpByTextExtended({
    required String text,
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByText(
      text,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled up widget with text: $text (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll up a widget by its tooltip with extended parameters
  Future<Response> scrollUpByTooltipExtended({
    required String tooltip,
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByTooltip(
      tooltip,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print('🤖 Scrolled up widget with tooltip: $tooltip (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll up a widget identified by ancestor and descendant with extended parameters
  Future<Response> scrollUpByAncestorAndDescendantExtended({
    required String ancestorType,
    required String descendantType,
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollUpByAncestorAndDescendant(
      ancestorType: ancestorType,
      descendantType: descendantType,
      dx: dx,
      dy: dy,
      duration: duration,
      frequency: frequency,
    );
    print(
        '🤖 Scrolled up $descendantType inside $ancestorType (dx: $dx, dy: $dy)');
    return response;
  }

  /// Scroll into view a widget by key
  Future<Response> scrollIntoViewByKey(String keyValue,
      {double alignment = 0.0}) async {
    _checkConnection();
    final response =
        await _finderUtils!.scrollIntoViewByKey(keyValue, alignment: alignment);
    print(
        '🤖 Scrolled widget with key: $keyValue into view (alignment: $alignment)');
    return response;
  }

  /// Scroll into view a widget by type
  Future<Response> scrollIntoViewByType(String widgetType,
      {double alignment = 0.0}) async {
    _checkConnection();
    final response = await _finderUtils!
        .scrollIntoViewByType(widgetType, alignment: alignment);
    print(
        '🤖 Scrolled widget of type: $widgetType into view (alignment: $alignment)');
    return response;
  }

  /// Scroll into view a widget by text
  Future<Response> scrollIntoViewByText(String text,
      {double alignment = 0.0}) async {
    _checkConnection();
    final response =
        await _finderUtils!.scrollIntoViewByText(text, alignment: alignment);
    print(
        '🤖 Scrolled widget with text: $text into view (alignment: $alignment)');
    return response;
  }

  /// Scroll into view a widget by tooltip
  Future<Response> scrollIntoViewByTooltip(String tooltip,
      {double alignment = 0.0}) async {
    _checkConnection();
    final response = await _finderUtils!
        .scrollIntoViewByTooltip(tooltip, alignment: alignment);
    print(
        '🤖 Scrolled widget with tooltip: $tooltip into view (alignment: $alignment)');
    return response;
  }

  /// Scroll into view a widget identified by ancestor and descendant
  Future<Response> scrollIntoViewByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
    double alignment = 0.0,
  }) async {
    _checkConnection();
    final response = await _finderUtils!.scrollIntoViewByAncestorAndDescendant(
      ancestorType: ancestorType,
      descendantType: descendantType,
      alignment: alignment,
    );
    print(
        '🤖 Scrolled $descendantType inside $ancestorType into view (alignment: $alignment)');
    return response;
  }

  // Helper to check connection status
  void _checkConnection() {
    if (_vmService == null || _extensionUtils == null || _finderUtils == null) {
      throw Exception('VM Service not connected. Call start() first.');
    }
  }

  void _stop() {
    _isRunning = false;
    print('FlutterBrowserTool stopped.');
  }
}
