import 'package:vm_service/vm_service.dart';

/// A utility class for interacting with Flutter's service extension APIs.
///
/// This provides a Dart implementation of the VM service extension functions
/// with proper parameter handling based on the Flutter framework's expectations.
class FlutterExtensionUtils {
  final VmService vmService;

  FlutterExtensionUtils(this.vmService);

  /// Lists all the Flutter views available.
  Future<Response> listViews() async {
    return await vmService.callServiceExtension('_flutter.listViews', args: {});
  }

  /// Gets the display refresh rate for a view.
  Future<Response> getDisplayRefreshRate(String viewId) async {
    return await vmService.callServiceExtension(
      '_flutter.getDisplayRefreshRate',
      args: {'viewId': viewId},
    );
  }

  /// Toggles the display of oversized images.
  Future<Response> invertOversizedImage(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.invertOversizedImages',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles debug paint mode.
  Future<Response> debugPaint(String isolateId, {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugPaint',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles baseline painting.
  Future<Response> debugPaintBaselinesEnabled(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugPaintBaselinesEnabled',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles repaint rainbow effect.
  Future<Response> repaintRainbow(String isolateId, {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.repaintRainbow',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Dumps the layer tree.
  Future<Response> debugDumpLayerTree(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDumpLayerTree',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Toggles disabling of physical shape layers.
  Future<Response> debugDisablePhysicalShapeLayers(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDisablePhysicalShapeLayers',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles disabling of opacity layers.
  Future<Response> debugDisableOpacityLayers(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDisableOpacityLayers',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Dumps the render tree.
  Future<Response> debugDumpRenderTree(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDumpRenderTree',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Dumps the semantics tree in traversal order.
  Future<Response> debugDumpSemanticsTreeInTraversalOrder(
      String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDumpSemanticsTreeInTraversalOrder',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Dumps the semantics tree in inverse hit test order.
  Future<Response> debugDumpSemanticsTreeInInverseHitTestOrder(
      String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDumpSemanticsTreeInInverseHitTestOrder',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Toggles profiling of render object paints.
  Future<Response> profileRenderObjectPaints(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.profileRenderObjectPaints',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles profiling of render object layouts.
  Future<Response> profileRenderObjectLayouts(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.profileRenderObjectLayouts',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Sets time dilation factor.
  Future<Response> timeDilation(String isolateId, {String? value}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.timeDilation',
      isolateId: isolateId,
      args: {'value': value},
    );
  }

  /// Toggles profiling of platform channels.
  Future<Response> profilePlatformChannels(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.profilePlatformChannels',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Evicts assets from cache.
  Future<Response> evict(String isolateId, {String? value}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.evict',
      isolateId: isolateId,
      args: {'value': value},
    );
  }

  /// Triggers reassemble of the application.
  Future<Response> reassemble(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.reassemble',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Exits the application.
  Future<Response> exit(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.exit',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Sets or gets the connected VM service URI.
  Future<Response> connectedVmServiceUri(String isolateId,
      {String? value}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.connectedVmServiceUri',
      isolateId: isolateId,
      args: {'value': value},
    );
  }

  /// Sets or gets the active DevTools server address.
  Future<Response> activeDevToolsServerAddress(String isolateId,
      {String? value}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.activeDevToolsServerAddress',
      isolateId: isolateId,
      args: {'value': value},
    );
  }

  /// Overrides the platform.
  Future<Response> platformOverride(String isolateId, {String? value}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.platformOverride',
      isolateId: isolateId,
      args: {'value': value},
    );
  }

  /// Overrides the brightness.
  Future<Response> brightnessOverride(String isolateId, {String? value}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.brightnessOverride',
      isolateId: isolateId,
      args: {'value': value},
    );
  }

  /// Dumps the application widget tree.
  Future<Response> debugDumpApp(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDumpApp',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Dumps the focus tree.
  Future<Response> debugDumpFocusTree(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugDumpFocusTree',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Toggles the performance overlay.
  Future<Response> showPerformanceOverlay(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.showPerformanceOverlay',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Sets or queries the first frame event status.
  Future<Response> didSendFirstFrameEvent(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.didSendFirstFrameEvent',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Sets or queries the first frame rasterized event status.
  Future<Response> didSendFirstFrameRasterizedEvent(String isolateId,
      {String? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.didSendFirstFrameRasterizedEvent',
      isolateId: isolateId,
      args: {'enabled': enabled},
    );
  }

  /// Toggles profiling of widget builds.
  Future<Response> profileWidgetBuilds(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.profileWidgetBuilds',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles profiling of user widget builds.
  Future<Response> profileUserWidgetBuilds(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.profileUserWidgetBuilds',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles the debug banner.
  Future<Response> debugAllowBanner(String isolateId, {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.debugAllowBanner',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles structured error reporting.
  Future<Response> structuredErrors(String isolateId, {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.structuredErrors',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles inspector visibility.
  Future<Response> show(String isolateId, {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.show',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles tracking of widget rebuilds.
  Future<Response> trackRebuildDirtyWidgets(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.trackRebuildDirtyWidgets',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Toggles tracking of widget repaints.
  Future<Response> trackRepaintWidgets(String isolateId,
      {bool? enabled}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.trackRepaintWidgets',
      isolateId: isolateId,
      args: {'enabled': enabled?.toString()},
    );
  }

  /// Disposes all object groups.
  Future<Response> disposeAllGroups(
      String isolateId, String objectGroup) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.disposeAllGroups',
      isolateId: isolateId,
      args: {'objectGroup': objectGroup},
    );
  }

  /// Disposes a specific object group.
  Future<Response> disposeGroup(String isolateId, String objectGroup) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.disposeGroup',
      isolateId: isolateId,
      args: {'objectGroup': objectGroup},
    );
  }

  /// Checks if the widget tree is ready.
  Future<Response> isWidgetTreeReady(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.isWidgetTreeReady',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Disposes a specific object by ID.
  Future<Response> disposeId(String isolateId, String objectGroup,
      {String? objectId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.disposeId',
      isolateId: isolateId,
      args: {
        'arg': objectId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Sets pub root directories.
  Future<Response> setPubRootDirectories(
      String isolateId, List<String> args) async {
    final Map<String, dynamic> params = {'isolateId': isolateId};
    for (int i = 0; i < args.length; i++) {
      params['arg$i'] = args[i];
    }
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.setPubRootDirectories',
      isolateId: isolateId,
      args: params,
    );
  }

  /// Adds pub root directories.
  Future<Response> addPubRootDirectories(
      String isolateId, List<String> args) async {
    final Map<String, dynamic> params = {'isolateId': isolateId};
    for (int i = 0; i < args.length; i++) {
      params['arg$i'] = args[i];
    }
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.addPubRootDirectories',
      isolateId: isolateId,
      args: params,
    );
  }

  /// Removes pub root directories.
  Future<Response> removePubRootDirectories(
      String isolateId, List<String> args) async {
    final Map<String, dynamic> params = {'isolateId': isolateId};
    for (int i = 0; i < args.length; i++) {
      params['arg$i'] = args[i];
    }
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.removePubRootDirectories',
      isolateId: isolateId,
      args: params,
    );
  }

  /// Gets the list of pub root directories.
  Future<Response> getPubRootDirectories(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getPubRootDirectories',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Sets widget selection by ID.
  Future<Response> setSelectionById(String isolateId, String objectGroup,
      {String? objectId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.setSelectionById',
      isolateId: isolateId,
      args: {
        'arg': objectId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets the parent chain of a widget.
  Future<Response> getParentChain(String isolateId, String objectGroup,
      {String? objectId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getParentChain',
      isolateId: isolateId,
      args: {
        'arg': objectId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets properties of a diagnosticable object.
  Future<Response> getProperties(String isolateId, String objectGroup,
      {String? diagnosticableId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getProperties',
      isolateId: isolateId,
      args: {
        'arg': diagnosticableId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets children of a diagnosticable object.
  Future<Response> getChildren(String isolateId, String objectGroup,
      {String? diagnosticableId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getChildren',
      isolateId: isolateId,
      args: {
        'arg': diagnosticableId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets summary tree of children of a diagnosticable object.
  Future<Response> getChildrenSummaryTree(String isolateId, String objectGroup,
      {String? diagnosticableId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getChildrenSummaryTree',
      isolateId: isolateId,
      args: {
        'arg': diagnosticableId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets details subtree of children of a diagnosticable object.
  Future<Response> getChildrenDetailsSubtree(
      String isolateId, String objectGroup,
      {String? diagnosticableId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getChildrenDetailsSubtree',
      isolateId: isolateId,
      args: {
        'arg': diagnosticableId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets the root widget.
  Future<Response> getRootWidget(String isolateId,
      {String? objectGroup}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getRootWidget',
      isolateId: isolateId,
      args: {
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets the summary tree of the root widget.
  Future<Response> getRootWidgetSummaryTree(String isolateId,
      {String? objectGroup}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getRootWidgetSummaryTree',
      isolateId: isolateId,
      args: {
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets the summary tree of the root widget with previews.
  Future<Response> getRootWidgetSummaryTreeWithPreviews(String isolateId,
      {String? objectGroup}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getRootWidgetSummaryTreeWithPreviews',
      isolateId: isolateId,
      args: {
        'groupName':
            objectGroup, // Note: This uses 'groupName' instead of 'objectGroup'
      },
    );
  }

  /// Gets details subtree of a diagnosticable object.
  Future<Response> getDetailsSubtree(String isolateId, String objectGroup,
      {String? diagnosticableId, int? subtreeDepth}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getDetailsSubtree',
      isolateId: isolateId,
      args: {
        'arg': diagnosticableId,
        'subtreeDepth': subtreeDepth?.toString(),
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets the selected widget.
  Future<Response> getSelectedWidget(String isolateId, String objectGroup,
      {String? previousSelectionId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getSelectedWidget',
      isolateId: isolateId,
      args: {
        'arg': previousSelectionId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Gets the selected summary widget.
  Future<Response> getSelectedSummaryWidget(
      String isolateId, String objectGroup,
      {String? previousSelectionId}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getSelectedSummaryWidget',
      isolateId: isolateId,
      args: {
        'arg': previousSelectionId,
        'objectGroup': objectGroup,
      },
    );
  }

  /// Checks if widget creation is tracked.
  Future<Response> isWidgetCreationTracked(String isolateId) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.isWidgetCreationTracked',
      isolateId: isolateId,
      args: {},
    );
  }

  /// Takes a screenshot of a widget.
  Future<Response> screenshot(
      String isolateId, String id, double width, double height,
      {double? margin, double? maxPixelRatio, bool? debugPaint}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.screenshot',
      isolateId: isolateId,
      args: {
        'id': id,
        'width': width.toString(),
        'height': height.toString(),
        'margin': margin?.toString(),
        'maxPixelRatio': maxPixelRatio?.toString(),
        'debugPaint': debugPaint?.toString(),
      },
    );
  }

  /// Gets the layout explorer node.
  Future<Response> getLayoutExplorerNode(String isolateId, String objectGroup,
      {String? id, int? subtreeDepth}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.getLayoutExplorerNode',
      isolateId: isolateId,
      args: {
        'id': id,
        'groupName':
            objectGroup, // Note: This uses 'groupName' instead of 'objectGroup'
        'subtreeDepth': subtreeDepth?.toString(),
      },
    );
  }

  /// Sets flex fit on a widget.
  Future<Response> setFlexFit(String isolateId,
      {String? id, String? flexFit}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.setFlexFit',
      isolateId: isolateId,
      args: {
        'id': id,
        'flexFit': flexFit,
      },
    );
  }

  /// Sets flex factor on a widget.
  Future<Response> setFlexFactor(String isolateId,
      {String? id, int? flexFactor}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.setFlexFactor',
      isolateId: isolateId,
      args: {
        'id': id,
        'flexFactor': flexFactor?.toString(),
      },
    );
  }

  /// Sets flex properties on a widget.
  Future<Response> setFlexProperties(String isolateId,
      {String? id,
      String? mainAxisAlignment,
      String? crossAxisAlignment}) async {
    return await vmService.callServiceExtension(
      'ext.flutter.inspector.setFlexProperties',
      isolateId: isolateId,
      args: {
        'id': id,
        'mainAxisAlignment': mainAxisAlignment,
        'crossAxisAlignment': crossAxisAlignment,
      },
    );
  }
}

/// Enum for flex fit values.
enum FlexFit {
  tight,
  loose,
}

/// Enum for main axis alignment values.
enum MainAxisAlignment {
  start,
  end,
  center,
  spaceBetween,
  spaceAround,
  spaceEvenly,
}

/// Enum for cross axis alignment values.
enum CrossAxisAlignment {
  start,
  end,
  center,
  stretch,
  baseline,
}

/// Extension methods for enum serialization
extension FlexFitExtension on FlexFit {
  String get serialized => toString().split('.').last;
}

extension MainAxisAlignmentExtension on MainAxisAlignment {
  String get serialized => toString().split('.').last;
}

extension CrossAxisAlignmentExtension on CrossAxisAlignment {
  String get serialized => toString().split('.').last;
}
