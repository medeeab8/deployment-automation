REM This batch file provides an easy way to run the deployment tool on
REM Windows systems, bypassing issues with Python entry points.

@echo off
python %~dp0\src\deployer.py %*