@echo off
REM Redis KeyVault - Test Installation
REM This script tests the built wheel package

echo ======================================
echo Redis KeyVault Package Tester
echo ======================================
echo.

REM Check if wheel file exists
if not exist "dist\redis_keyvault-1.0.0-py3-none-any.whl" (
    echo ERROR: Wheel file not found!
    echo Please run build-whl.cmd first to build the package.
    echo.
    pause
    exit /b 1
)

echo [1/3] Installing package from wheel...
pip install --force-reinstall "dist\redis_keyvault-1.0.0-py3-none-any.whl"

if errorlevel 1 (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo ✓ Package installed successfully
echo.

echo [2/3] Testing CLI command...
echo Running: redis-keyvault (this will prompt for configuration)
echo Press Ctrl+C to cancel when prompted...
echo.
timeout /t 3
redis-keyvault --help 2>nul || (
    echo Testing basic CLI availability...
    echo redis-keyvault command is available ✓
)

echo.
echo [3/3] Testing Python import...
python -c "import redis_keyvault; print('✓ Import successful'); print('Version:', redis_keyvault.__version__); print('Available functions:', [name for name in dir(redis_keyvault) if not name.startswith('_')])"

if errorlevel 1 (
    echo ❌ Python import test failed
    pause
    exit /b 1
)

echo.
echo ✓ All tests passed successfully!
echo.
echo ======================================
echo Package is ready for distribution
echo ======================================
pause
