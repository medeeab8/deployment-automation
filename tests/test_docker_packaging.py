#!/usr/bin/env python3
"""
test_docker_packaging.py - Test Docker packaging functionality
"""
import os
import sys
import subprocess
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import logging


from src.app_packager import PythonPackager, PerlPackager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_docker")

def test_python_docker_packaging():

    app_config = {
        'name': 'python-docker-test',
        'type': 'python',
        'source_dir': './tests/mock/python-app',
        'package_type': 'docker',
        'python_base_image': 'python:3.9-slim',
        'docker_commands': [
            'RUN pip install -r requirements.txt',
            'CMD ["python", "python-app.py"]'
        ]
    }
    

    os.makedirs("build/python-docker-test", exist_ok=True)
    
    packager = PythonPackager(app_config)
    
    try:
        logger.info("Testing Python Docker packaging...")
        package_path = packager.package("test-version")
        
        if os.path.exists(package_path):
            logger.info(f"SUCCESS: Docker package created at {package_path}")
            return True
        else:
            logger.error(f"FAILURE: Docker package not created at {package_path}")
            return False
    except Exception as e:
        logger.error(f"ERROR: Docker packaging failed: {str(e)}")
        return False

def test_perl_docker_packaging():
    app_config = {
        'name': 'perl-docker-test',
        'type': 'perl',
        'source_dir': './tests/mock/perl-app',
        'package_type': 'docker',
        'perl_base_image': 'perl:3.9-slim',
        'docker_commands': [
            'CMD ["perl", "perl-app.pl"]'
        ]
    }
    

    os.makedirs("build/perl-docker-test", exist_ok=True)
    
    packager = PerlPackager(app_config)
    
    try:
        logger.info("Testing Perl Docker packaging...")  # Fixed the log message
        package_path = packager.package("test-version")
        
        if os.path.exists(package_path):
            logger.info(f"SUCCESS: Docker package created at {package_path}")
            return True
        else:
            logger.error(f"FAILURE: Docker package not created at {package_path}")
            return False
    except Exception as e:
        logger.error(f"ERROR: Docker packaging failed: {str(e)}")
        return False

def check_docker_available():
    try:
        subprocess.run(
            ["docker", "--version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def main():
    if not check_docker_available():
        logger.error("Docker is not available. Please install Docker to run this test.")
        return 1
    
    python_success = test_python_docker_packaging()
    perl_success = test_perl_docker_packaging()
    
    print("\n=== Docker Packaging Test Results ===")
    print(f"Python Docker packaging: {'PASSED' if python_success else 'FAILED'}")
    print(f"Perl Docker packaging: {'PASSED' if perl_success else 'FAILED'}")
    
    return 0 if (python_success and perl_success) else 1

if __name__ == "__main__":
    sys.exit(main())