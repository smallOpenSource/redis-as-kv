@echo off
REM Redis KeyVault - Clean Build Artifacts
REM This script cleans all build artifacts and temporary files

echo ======================================
echo Redis KeyVault Build Cleaner
echo ======================================
echo.

echo Cleaning build artifacts...

REM Remove build directories
if exist "dist" (
    echo Removing dist/
    rmdir /s /q "dist"
)

if exist "build" (
    echo Removing build/
    rmdir /s /q "build"
)

if exist "redis_keyvault.egg-info" (
    echo Removing redis_keyvault.egg-info/
    rmdir /s /q "redis_keyvault.egg-info"
)

REM Remove Python cache files
echo Removing Python cache files...
for /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Removing %%d
        rmdir /s /q "%%d"
    )
)

REM Remove .pyc files
for /r . %%f in (*.pyc) do (
    if exist "%%f" (
        echo Removing %%f
        del "%%f"
    )
)

REM Remove .pyo files
for /r . %%f in (*.pyo) do (
    if exist "%%f" (
        echo Removing %%f
        del "%%f"
    )
)

echo.
echo ✓ Cleanup completed successfully!
echo.
echo The following directories/files were cleaned:
echo   - dist/
echo   - build/
echo   - redis_keyvault.egg-info/
echo   - __pycache__/ directories
echo   - *.pyc files
echo   - *.pyo files
echo.
echo You can now run build-whl.cmd for a fresh build.
echo.
pause
