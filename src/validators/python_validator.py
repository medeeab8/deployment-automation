#!/usr/bin/env python3
"""
python_validator.py - Basic Python application validator
"""
import os
import logging

logger = logging.getLogger("python_validator")

class PythonValidator:
    def __init__(self, app_config):
        self.app_config = app_config
        self.source_dir = app_config['source_dir']
    
    def validate(self):
        logger.info(f"Validating Python application: {self.app_config['name']}")
        
        print(f"DEBUG: Checking for source directory at: {self.source_dir}")
        print(f"DEBUG: Directory exists: {os.path.isdir(self.source_dir)}")
        if not os.path.isdir(self.source_dir):
            logger.error(f"Source directory not found: {self.source_dir}")
            return False
        
        return True