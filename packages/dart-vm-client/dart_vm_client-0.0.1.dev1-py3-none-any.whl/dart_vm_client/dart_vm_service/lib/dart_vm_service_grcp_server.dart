/// Dart VM Service gRPC library
library dart_vm_service_grpc;

import 'src/grpc_service.dart';

export 'src/generated/dart_vm_service.pb.dart';
export 'src/generated/dart_vm_service.pbgrpc.dart';

/// The main gRPC server for Dart VM Service.
/// Use this class to start and stop the gRPC service.
class DartVmServiceGrpcServer {
  final int _port;
  GrpcServer? _grpcServer;

  /// Creates a new gRPC server on the specified port.
  DartVmServiceGrpcServer({int port = 50051}) : _port = port;

  /// Starts the gRPC server.
  Future<void> start() async {
    _grpcServer = GrpcServer();
    await _grpcServer!.start(port: _port);
  }

  /// Stops the gRPC server.
  Future<void> stop() async {
    await _grpcServer?.stop();
  }
}
