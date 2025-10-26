@echo off
echo ================================================
echo MCP Generator - Quick Test Script
echo ================================================
echo.

REM Test 1: Install dependencies
echo [1/5] Installing dependencies...
pip install -e . >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo PASS: Dependencies installed
echo.

REM Test 2: Create sample config
echo [2/5] Creating sample configuration...
python -m mcp_generator.cli.main init -o test-config.yaml >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to create config
    exit /b 1
)
echo PASS: Sample config created
echo.

REM Test 3: Validate config
echo [3/5] Validating configuration...
python -m mcp_generator.cli.main validate test-config.yaml
if %errorlevel% neq 0 (
    echo ERROR: Validation failed
    exit /b 1
)
echo PASS: Configuration validated
echo.

REM Test 4: Generate code
echo [4/5] Generating server code...
python -m mcp_generator.cli.main generate test-config.yaml -o test-output
if %errorlevel% neq 0 (
    echo ERROR: Code generation failed
    exit /b 1
)
echo PASS: Code generated
echo.

REM Test 5: Check generated files
echo [5/5] Checking generated files...
if not exist "test-output\server.py" (
    echo ERROR: server.py not found
    exit /b 1
)
if not exist "test-output\requirements.txt" (
    echo ERROR: requirements.txt not found
    exit /b 1
)
if not exist "test-output\README.md" (
    echo ERROR: README.md not found
    exit /b 1
)
echo PASS: All files generated successfully
echo.

echo ================================================
echo ALL TESTS PASSED!
echo ================================================
echo.
echo Generated files are in: test-output\
echo.
echo To test with JSONPlaceholder API:
echo   mcp-gen generate examples\basic-api.yaml -o jsonplaceholder-server
echo   cd jsonplaceholder-server
echo   pip install -r requirements.txt
echo   python server.py
echo.

REM Cleanup
echo Cleaning up test files...
if exist "test-config.yaml" del test-config.yaml
if exist "test-output" rmdir /s /q test-output

echo Done!
