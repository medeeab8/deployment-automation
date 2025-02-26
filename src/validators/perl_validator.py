#!/usr/bin/env python3
"""
perl_validator.py - Basic Perl application validator
"""
import os
import logging

logger = logging.getLogger("perl_validator")

class PerlValidator:
    def __init__(self, app_config):
        self.app_config = app_config
        self.source_dir = app_config['source_dir']
    
    def validate(self):
        logger.info(f"Validating Perl application: {self.app_config['name']}")
        
        if not os.path.isdir(self.source_dir):
            logger.error(f"Source directory not found: {self.source_dir}")
            return False
        
        return True