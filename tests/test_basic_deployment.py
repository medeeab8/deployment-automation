#!/usr/bin/env python3
"""
test_basic_deployment.py - Basic test for deployment functionality
"""
import os
import sys
import subprocess
import logging

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

def main():
    # Make sure we're in the project root
    if not os.path.exists("src/deployer.py"):
        print("Error: Run this script from the project root directory")
        return 1
    
    # Create build directory if it doesn't exist
    os.makedirs("build", exist_ok=True)
    
    # Run tests
    python_test = test_deployment("python-app", "development")
    perl_test = test_deployment("perl-app", "development")
    
    # Print results
    print("\n=== Test Results ===")
    print(f"Python app: {'PASSED' if python_test else 'FAILED'}")
    print(f"Perl app: {'PASSED' if perl_test else 'FAILED'}")
    
    # Return success only if all tests passed
    return 0 if (python_test and perl_test) else 1

if __name__ == "__main__":
    sys.exit(main())