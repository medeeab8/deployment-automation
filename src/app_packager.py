#!/usr/bin/env python3
"""
app_packager.py - Base packaging functionality
"""
import os
import logging
from abc import ABC, abstractmethod
import shutil
import subprocess
import tempfile

logger = logging.getLogger("packager")

class BasePackager(ABC):
    """Base abstract class for application packagers"""
    
    def __init__(self, app_config):
        self.app_config = app_config
        self.app_name = app_config['name']
        self.source_dir = app_config['source_dir']
        self.build_dir = os.path.join('build', self.app_name)
        
        # Create build directory if it doesn't exist
        os.makedirs(self.build_dir, exist_ok=True)
    
    @abstractmethod
    def package(self, version):
        """Package the application and return the path to the package"""
        pass

class PythonPackager(BasePackager):
    """Handles packaging of Python applications"""
    
    def package(self, version):
        """Package a Python application"""
        logger.info(f"Packaging Python application {self.app_name} version {version}")
        
        # Determine packaging method
        if self.app_config.get('package_type') == 'wheel':
            return self._package_wheel(version)
        else:
            # Default to simple tarball for now
            return self._package_simple_tarball(version)
    
    def _package_wheel(self, version):
        """Package as Python wheel"""
        # Create a temporary directory for building
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy source to temp directory
            temp_source = os.path.join(temp_dir, self.app_name)
            shutil.copytree(self.source_dir, temp_source)
            
            # Check if setup.py exists
            setup_py = os.path.join(temp_source, 'setup.py')
            if not os.path.exists(setup_py):
                logger.error(f"No setup.py found in {self.source_dir}")
                raise FileNotFoundError(f"No setup.py found in {self.source_dir}")
            
            # Build the wheel
            subprocess.run(
                ['python', 'setup.py', 'bdist_wheel'],
                cwd=temp_source,
                check=True
            )
            
            # Copy the wheel to our build directory
            dist_dir = os.path.join(temp_source, 'dist')
            wheel_name = None
            for file in os.listdir(dist_dir):
                if file.endswith('.whl'):
                    wheel_name = file
                    break
            
            if not wheel_name:
                raise RuntimeError("Failed to build wheel package")
            
            wheel_path = os.path.join(dist_dir, wheel_name)
            target_path = os.path.join(self.build_dir, wheel_name)
            shutil.copy(wheel_path, target_path)
            
            return target_path
    
    def _package_simple_tarball(self, version):
        """Package as a simple tarball"""
        tar_name = f"{self.app_name}-{version}.tar.gz"
        tar_path = os.path.join(self.build_dir, tar_name)
        
        # Create tarball using tar command
        subprocess.run(
            ['tar', '-czf', tar_path, '-C', os.path.dirname(self.source_dir), 
             os.path.basename(self.source_dir)],
            check=True
        )
        
        return tar_path
    
    def _create_dockerfile(self, dockerfile_path, base_image, commands):
        with open(dockerfile_path, 'w') as f:
            f.write(f"FROM {base_image}\n\n")
            f.write("WORKDIR /app\n\n")
        
        for cmd in commands:
            f.write(f"{cmd}\n")

    def _package_docker(self, version):
    # Create a temporary directory for Docker build
        with tempfile.TemporaryDirectory() as temp_dir:
            source_copy = os.path.join(temp_dir, self.app_name)
            shutil.copytree(self.source_dir, source_copy)
        
            # Create Dockerfile
            dockerfile_path = os.path.join(temp_dir, 'Dockerfile')
            base_image = self.app_config.get('python_base_image', 'python:3.9-slim')
        
            # Define Docker commands
            commands = [
                "COPY . /app/",
                "RUN pip install --no-cache-dir -r requirements.txt",
                f"ENV APP_VERSION={version}",
                f"LABEL version={version}",
                "EXPOSE 8000",
                "CMD [\"python\", \"app.py\"]"
            ]
        
            # custom commands 
            if 'docker_commands' in self.app_config:
                commands.extend(self.app_config['docker_commands'])
                
            self._create_dockerfile(dockerfile_path, base_image, commands)
            
            # Build Docker image
            image_name = f"{self.app_name.lower()}:{version}"
            subprocess.run(
                ['docker', 'build', '-t', image_name, '.'],
                cwd=temp_dir,
                check=True
            )
            
            tar_path = os.path.join(self.build_dir, f"{self.app_name}-{version}.tar")
            subprocess.run(
                ['docker', 'save', '-o', tar_path, image_name],
                check=True
            )
            
            return tar_path
    
class PerlPackager(BasePackager):
    """Handles packaging of Perl applications"""
    
    def package(self, version):
        """Package a Perl application"""
        logger.info(f"Packaging Perl application {self.app_name} version {version}")
        
        # For now, just create a simple tarball
        tar_name = f"{self.app_name}-{version}.tar.gz"
        tar_path = os.path.join(self.build_dir, tar_name)
        
        # Create tarball using tar command
        subprocess.run(
            ['tar', '-czf', tar_path, '-C', os.path.dirname(self.source_dir), 
             os.path.basename(self.source_dir)],
            check=True
        )
        
        return tar_path