#!/usr/bin/env python3
"""
app_packager.py - Base packaging functionality
"""
import os
import logging
from abc import ABC, abstractmethod

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