#!/usr/bin/env python3
"""
env_manager.py - Basic environment management
"""
import logging

logger = logging.getLogger("env_manager")

class EnvironmentManager:
    def __init__(self, env_config):
        self.env_config = env_config
        self.env_type = env_config['type']
    
    def prepare(self):
        logger.info(f"Preparing {self.env_type} environment")
        
        # will expand later
        if self.env_type == 'vm':
            self._prepare_vm()
        else:
            logger.info(f"Environment type {self.env_type} preparation not implemented yet")
    
    def _prepare_vm(self):
        hosts = self.env_config.get('hosts', [])
        if hosts:
            logger.info(f"Would prepare VM environment on hosts: {', '.join(hosts)}")
           