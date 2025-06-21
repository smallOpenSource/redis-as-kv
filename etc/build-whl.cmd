@echo off
REM Redis KeyVault - Build WHL Package
REM This script builds the wheel package for Redis KeyVault

echo ======================================
echo Redis KeyVault Package Builder
echo ======================================
echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo ERROR: pyproject.toml not found!
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

REM Clean previous builds
echo [1/4] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "redis_keyvault.egg-info" rmdir /s /q "redis_keyvault.egg-info"
echo ✓ Cleanup completed

echo.
echo [2/4] Installing build dependencies...
pip install --upgrade build twine
echo ✓ Dependencies installed

echo.
echo [3/4] Building package...
python -m build
echo ✓ Package built successfully

echo.
echo [4/4] Listing generated files...
if exist "dist" (
    echo Generated files in dist/:
    dir /b "dist\*"
    echo.
    echo ✓ Build completed successfully!
    echo.
    echo You can now install the package with:
    echo   pip install dist\redis_keyvault-1.0.0-py3-none-any.whl
    echo.
    echo Or upload to PyPI with:
    echo   twine upload dist/*
) else (
    echo ❌ Build failed - dist directory not found
    exit /b 1
)

echo.
echo ======================================
echo Build process completed
echo ======================================
pause
