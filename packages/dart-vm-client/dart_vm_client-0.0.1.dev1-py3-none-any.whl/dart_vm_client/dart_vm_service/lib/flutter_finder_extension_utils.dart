import 'dart:convert';

import 'package:vm_service/vm_service.dart';

class FlutterFinderExtensionUtils {
  final VmService vmService;

  FlutterFinderExtensionUtils({required this.vmService});

  Future<Response> tapWidgetByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
  }) async {
    final vm = await vmService.getVM();
    final mainIsolate = vm.isolates!.first;

    // Create string representations for nested finders
    final ofFinder = jsonEncode({
      'finderType': 'ByType',
      'type': ancestorType,
    });

    final matchingFinder = jsonEncode({
      'finderType': 'ByType',
      'type': descendantType,
    });

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'Descendant',
        'of': ofFinder,
        'matching': matchingFinder,
        'matchRoot': false,
        'firstMatchOnly': true,
      },
    );
  }

  Future<Response> tapWidgetByKey(String keyValue) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByValueKey',
        'keyValueString': keyValue,
        'keyValueType': 'String',
      },
    );
  }

  Future<Response> tapWidgetByText(String text) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates?.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate!.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByText',
        'text': text,
      },
    );
  }

  Future<Response> tapWidgetByType(String widgetType) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates?.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate!.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByType',
        'type': widgetType,
      },
    );
  }

  Future<Response> tapWidgetByTooltip(String tooltip) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByTooltip',
        'tooltip': tooltip,
      },
    );
  }

  // Enter Text methods

  Future<Response> enterTextByKey(String text, String keyValue) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    // First tap the widget
    await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByValueKey',
        'keyValueString': keyValue,
        'keyValueType': 'String',
      },
    );

    // Then enter text
    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'enter_text',
        'text': text,
      },
    );
  }

  Future<Response> enterTextByType(String text, String widgetType) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    // First tap the widget
    await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByType',
        'type': widgetType,
      },
    );

    // Then enter text
    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'enter_text',
        'text': text,
      },
    );
  }

  Future<Response> enterTextByText(String text, String widgetText) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    // First tap the widget
    await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByText',
        'text': widgetText,
      },
    );

    // Then enter text
    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'enter_text',
        'text': text,
      },
    );
  }

  Future<Response> enterTextByTooltip(String text, String tooltip) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    // First tap the widget
    await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'ByTooltip',
        'tooltip': tooltip,
      },
    );

    // Then enter text
    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'enter_text',
        'text': text,
      },
    );
  }

  Future<Response> enterTextByAncestorAndDescendant({
    required String text,
    required String ancestorType,
    required String descendantType,
  }) async {
    final vm = await vmService.getVM();
    final mainIsolate = vm.isolates!.first;

    // Create string representations for nested finders
    final ofFinder = jsonEncode({
      'finderType': 'ByType',
      'type': ancestorType,
    });

    final matchingFinder = jsonEncode({
      'finderType': 'ByType',
      'type': descendantType,
    });

    // First tap the widget
    await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'tap',
        'finderType': 'Descendant',
        'of': ofFinder,
        'matching': matchingFinder,
        'matchRoot': false,
        'firstMatchOnly': true,
      },
    );

    // Then enter text
    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'enter_text',
        'text': text,
      },
    );
  }

  // Scroll Down methods

  Future<Response> scrollDownByKey(
    String keyValue, {
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByValueKey',
        'keyValueString': keyValue,
        'keyValueType': 'String',
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollDownByType(
    String widgetType, {
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByType',
        'type': widgetType,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollDownByText(
    String text, {
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByText',
        'text': text,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollDownByTooltip(
    String tooltip, {
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByTooltip',
        'tooltip': tooltip,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollDownByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
    double dx = 0.0,
    double dy = 200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    final vm = await vmService.getVM();
    final mainIsolate = vm.isolates!.first;

    // Create string representations for nested finders
    final ofFinder = jsonEncode({
      'finderType': 'ByType',
      'type': ancestorType,
    });

    final matchingFinder = jsonEncode({
      'finderType': 'ByType',
      'type': descendantType,
    });

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'Descendant',
        'of': ofFinder,
        'matching': matchingFinder,
        'matchRoot': false,
        'firstMatchOnly': true,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  // Scroll Up methods

  Future<Response> scrollUpByKey(
    String keyValue, {
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByValueKey',
        'keyValueString': keyValue,
        'keyValueType': 'String',
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollUpByType(
    String widgetType, {
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByType',
        'type': widgetType,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollUpByText(
    String text, {
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByText',
        'text': text,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollUpByTooltip(
    String tooltip, {
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'ByTooltip',
        'tooltip': tooltip,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  Future<Response> scrollUpByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
    double dx = 0.0,
    double dy = -200.0,
    Duration duration = const Duration(milliseconds: 100),
    int frequency = 60,
  }) async {
    final vm = await vmService.getVM();
    final mainIsolate = vm.isolates!.first;

    // Create string representations for nested finders
    final ofFinder = jsonEncode({
      'finderType': 'ByType',
      'type': ancestorType,
    });

    final matchingFinder = jsonEncode({
      'finderType': 'ByType',
      'type': descendantType,
    });

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scroll',
        'finderType': 'Descendant',
        'of': ofFinder,
        'matching': matchingFinder,
        'matchRoot': false,
        'firstMatchOnly': true,
        'dx': dx.toString(),
        'dy': dy.toString(),
        'duration': duration.inMicroseconds.toString(),
        'frequency': frequency.toString(),
      },
    );
  }

  // ScrollIntoView methods

  Future<Response> scrollIntoViewByKey(String keyValue,
      {double alignment = 0.0}) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scrollIntoView',
        'finderType': 'ByValueKey',
        'keyValueString': keyValue,
        'keyValueType': 'String',
        'alignment': alignment.toString(),
      },
    );
  }

  Future<Response> scrollIntoViewByType(String widgetType,
      {double alignment = 0.0}) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scrollIntoView',
        'finderType': 'ByType',
        'type': widgetType,
        'alignment': alignment.toString(),
      },
    );
  }

  Future<Response> scrollIntoViewByText(String text,
      {double alignment = 0.0}) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scrollIntoView',
        'finderType': 'ByText',
        'text': text,
        'alignment': alignment.toString(),
      },
    );
  }

  Future<Response> scrollIntoViewByTooltip(String tooltip,
      {double alignment = 0.0}) async {
    VM vm = await vmService.getVM();
    IsolateRef? mainIsolate = vm.isolates!.first;

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scrollIntoView',
        'finderType': 'ByTooltip',
        'tooltip': tooltip,
        'alignment': alignment.toString(),
      },
    );
  }

  Future<Response> scrollIntoViewByAncestorAndDescendant({
    required String ancestorType,
    required String descendantType,
    double alignment = 0.0,
  }) async {
    final vm = await vmService.getVM();
    final mainIsolate = vm.isolates!.first;

    // Create string representations for nested finders
    final ofFinder = jsonEncode({
      'finderType': 'ByType',
      'type': ancestorType,
    });

    final matchingFinder = jsonEncode({
      'finderType': 'ByType',
      'type': descendantType,
    });

    return await vmService.callServiceExtension(
      'ext.flutter.driver',
      isolateId: mainIsolate.id!,
      args: {
        'command': 'scrollIntoView',
        'finderType': 'Descendant',
        'of': ofFinder,
        'matching': matchingFinder,
        'matchRoot': false,
        'firstMatchOnly': true,
        'alignment': alignment.toString(),
      },
    );
  }
}
