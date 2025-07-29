from setuptools import setup, find_packages
import os
import shutil

# Ensure dart_vm_service directory is included in the package
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('dart_vm_client/dart_vm_service')

if __name__ == "__main__":
    setup(
        packages=find_packages(),
        package_data={
            'dart_vm_client': ['dart_vm_service.proto', 'dart_vm_service_pb2.py', 'dart_vm_service_pb2_grpc.py', *extra_files],
        },
        include_package_data=True,
    ) 