#!/usr/bin/env python3

import os
import sys
import yaml
import logging
import argparse
from datetime import datetime

from app_packager import PythonPackager, PerlPackager
from env_manager import EnvironmentManager
from validators.python_validator import PythonValidator
from validators.perl_validator import PerlValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("deployer")

class DeploymentManager:
    def __init__(self, app_name, env_name, version=None, test_mode=False):
        self.app_name = app_name
        self.env_name = env_name
        self.version = version or datetime.now().strftime('%Y%m%d.%H%M%S')
        self.test_mode = test_mode
        

        with open('config/environments.yaml', 'r') as file:
            self.environments = yaml.safe_load(file)
        
        with open('config/apps.yaml', 'r') as file:
            self.apps = yaml.safe_load(file)
            

        if app_name not in self.apps:
            raise ValueError(f"Application '{app_name}' not found in configuration")
        
        if env_name not in self.environments:
            raise ValueError(f"Environment '{env_name}' not found in configuration")
            
        self.app_config = self.apps[app_name]
        self.env_config = self.environments[env_name]
        

        self.env_manager = EnvironmentManager(self.env_config)

        if self.app_config['type'] == 'python':
            self.packager = PythonPackager(self.app_config)
            self.validator = PythonValidator(self.app_config)
        elif self.app_config['type'] == 'perl':
            self.packager = PerlPackager(self.app_config)
            self.validator = PerlValidator(self.app_config)
        else:
            raise ValueError(f"Unsupported application type: {self.app_config['type']}")
    
    def validate(self):
        logger.info(f"Validating {self.app_name} for deployment to {self.env_name}")
        return self.validator.validate()
    
    def package(self):

        logger.info(f"Packaging {self.app_name} version {self.version}")
        package_path = self.packager.package(self.version)
        logger.info(f"Package created at {package_path}")

        return package_path
    
    def deploy(self, package_path):

        logger.info(f"Deploying {self.app_name} version {self.version} to {self.env_name}")
        self.env_manager.prepare()
        logger.info(f"Would deploy {package_path} to {self.env_name}")
        
        return True
    
    def run_deployment(self):
        try:
            if not self.validate():
                raise ValueError("Validation failed")

            package_path = self.package()

            success = self.deploy(package_path)
            
            return success
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}", exc_info=True)
            return False

def main():
    parser = argparse.ArgumentParser(description="Deploy applications to environments")
    parser.add_argument("app", help="Application name (defined in apps.yaml)")
    parser.add_argument("environment", help="Target environment (defined in environments.yaml)")
    parser.add_argument("--version", help="Version tag (defaults to timestamp)")
    parser.add_argument("--test", action="store_true", help="Run in test mode (no actual deployments)")
    args = parser.parse_args()
    

    try:
        manager = DeploymentManager(args.app, args.environment, args.version, test_mode=args.test)
        success = manager.run_deployment()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.critical(f"Deployment error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()