#!/usr/bin/env python3
"""
test_basic_deployment.py - Test for deployment and packaging functionality
"""
import os
import sys
import subprocess
import logging
import yaml

# Add the source directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.app_packager import PythonPackager, PerlPackager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test")

def test_deployment(app, env):
    """Test deploying an app to an environment"""
    logger.info(f"Testing deployment of {app} to {env}")
    
    # Run the deployer script with test flag
    cmd = ["python", "src/deployer.py", app, env, "--test"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Log the output
    print("\nCommand output:")
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    # Return status based on exit code
    return result.returncode == 0

def test_python_tarball_packaging():
    """Test Python tarball packaging directly"""
    logger.info("Testing Python tarball packaging...")
    
    # Create a test configuration
    app_config = {
        'name': 'python-tarball-test',
        'type': 'python',
        'source_dir': './tests/mock/python-app',
        # Not specifying package_type will default to tarball
    }
    
    # Create the mock directory and a simple Python file
    os.makedirs("./tests/mock/python-app", exist_ok=True)
    with open("./tests/mock/python-app/test.py", "w") as f:
        f.write("print('Hello from Python test app')")
    
    os.makedirs("build/python-tarball-test", exist_ok=True)
    
    # Create the packager and run it
    packager = PythonPackager(app_config)
    try:
        package_path = packager.package("test-tarball-version")
        
        if os.path.exists(package_path) and package_path.endswith('.tar.gz'):
            logger.info(f"SUCCESS: Tarball package created at {package_path}")
            return True
        else:
            logger.error(f"FAILURE: Tarball package not created correctly at {package_path}")
            return False
    except Exception as e:
        logger.error(f"ERROR: Tarball packaging failed: {str(e)}")
        return False

def test_python_wheel_packaging():
    """Test Python wheel packaging directly"""
    logger.info("Testing Python wheel packaging...")
    
    # Create a mock Python application with setup.py
    mock_app_dir = "./tests/mock/python-wheel-app"
    os.makedirs(mock_app_dir, exist_ok=True)
    
    # Create a minimal setup.py
    with open(os.path.join(mock_app_dir, "setup.py"), "w") as f:
        f.write("""
from setuptools import setup, find_packages

setup(
    name="test-wheel-app",
    version="0.1",
    packages=find_packages(),
)
""")
    
    # Create an empty package directory
    os.makedirs(os.path.join(mock_app_dir, "test_wheel_app"), exist_ok=True)
    with open(os.path.join(mock_app_dir, "test_wheel_app", "__init__.py"), "w") as f:
        f.write("# Package init")
    
    app_config = {
        'name': 'python-wheel-test',
        'type': 'python',
        'source_dir': mock_app_dir,
        'package_type': 'wheel'
    }
    
    os.makedirs("build/python-wheel-test", exist_ok=True)
    
    # Create the packager and run it
    packager = PythonPackager(app_config)
    try:
        package_path = packager.package("test-wheel-version")
        
        if os.path.exists(package_path) and package_path.endswith('.whl'):
            logger.info(f"SUCCESS: Wheel package created at {package_path}")
            return True
        else:
            logger.error(f"FAILURE: Wheel package not created correctly at {package_path}")
            return False
    except Exception as e:
        logger.error(f"ERROR: Wheel packaging failed: {str(e)}")
        return False

def test_perl_tarball_packaging():
    """Test Perl tarball packaging directly"""
    logger.info("Testing Perl tarball packaging...")
    
    # Create a test configuration
    app_config = {
        'name': 'perl-tarball-test',
        'type': 'perl',
        'source_dir': './tests/mock/perl-app',
        # Not specifying package_type will default to tarball
    }
    
    # Create the mock directory and a simple Perl file
    os.makedirs("./tests/mock/perl-app", exist_ok=True)
    with open("./tests/mock/perl-app/test.pl", "w") as f:
        f.write("print 'Hello from Perl test app\\n';")
    
    os.makedirs("build/perl-tarball-test", exist_ok=True)
    
    # Create the packager and run it
    packager = PerlPackager(app_config)
    try:
        package_path = packager.package("test-tarball-version")
        
        if os.path.exists(package_path) and package_path.endswith('.tar.gz'):
            logger.info(f"SUCCESS: Tarball package created at {package_path}")
            return True
        else:
            logger.error(f"FAILURE: Tarball package not created correctly at {package_path}")
            return False
    except Exception as e:
        logger.error(f"ERROR: Tarball packaging failed: {str(e)}")
        return False

def create_test_configs():
    """Create test configuration files if they don't exist"""
    # Create config directory
    os.makedirs("config", exist_ok=True)
    
    # Create apps.yaml if it doesn't exist
    if not os.path.exists("config/apps.yaml"):
        apps_config = {
            'python-app': {
                'name': 'python-app',
                'type': 'python',
                'source_dir': './tests/mock/python-app'
            },
            'perl-app': {
                'name': 'perl-app',
                'type': 'perl',
                'source_dir': './tests/mock/perl-app'
            }
        }
        with open("config/apps.yaml", "w") as f:
            yaml.dump(apps_config, f)
    
    # Create environments.yaml if it doesn't exist
    if not os.path.exists("config/environments.yaml"):
        env_config = {
            'development': {
                'type': 'vm',
                'hosts': ['localhost']
            },
            'production': {
                'type': 'vm',
                'hosts': ['production-server']
            }
        }
        with open("config/environments.yaml", "w") as f:
            yaml.dump(env_config, f)

def main():
    # Make sure we're in the project root
    if not os.path.exists("src/deployer.py"):
        print("Error: Run this script from the project root directory")
        return 1
    
    # Create build directory if it doesn't exist
    os.makedirs("build", exist_ok=True)
    
    # Create test configuration files
    create_test_configs()
    
    # Test direct packaging functions
    python_tarball_test = test_python_tarball_packaging()
    perl_tarball_test = test_perl_tarball_packaging()
    
    # Try to run the wheel packaging test, but don't fail the whole suite if it fails
    # (since setuptools might not be installed)
    try:
        python_wheel_test = test_python_wheel_packaging()
    except Exception as e:
        logger.warning(f"Wheel packaging test skipped: {str(e)}")
        python_wheel_test = False
    
    # Run full deployment tests
    python_deploy_test = test_deployment("python-app", "development")
    perl_deploy_test = test_deployment("perl-app", "development")
    
    # Print results
    print("\n=== Packaging Test Results ===")
    print(f"Python tarball packaging: {'PASSED' if python_tarball_test else 'FAILED'}")
    print(f"Python wheel packaging: {'PASSED' if python_wheel_test else 'FAILED'}")
    print(f"Perl tarball packaging: {'PASSED' if perl_tarball_test else 'FAILED'}")
    
    print("\n=== Deployment Test Results ===")
    print(f"Python app deployment: {'PASSED' if python_deploy_test else 'FAILED'}")
    print(f"Perl app deployment: {'PASSED' if perl_deploy_test else 'FAILED'}")
    
    # Return success only if all required tests passed
    # (wheel test is optional since it requires setuptools)
    required_tests = [python_tarball_test, perl_tarball_test, python_deploy_test, perl_deploy_test]
    return 0 if all(required_tests) else 1

if __name__ == "__main__":
    sys.exit(main())