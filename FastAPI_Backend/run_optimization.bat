@echo off
echo Trying to run dataset optimization...
echo.

echo Attempting with 'py' command...
py optimize_dataset.py
if %errorlevel% equ 0 goto success

echo.
echo Attempting with 'python3' command...
python3 optimize_dataset.py
if %errorlevel% equ 0 goto success

echo.
echo Attempting with 'python' command...
python optimize_dataset.py
if %errorlevel% equ 0 goto success

echo.
echo All Python commands failed. Please check your Python installation.
echo You can download Python from: https://www.python.org/downloads/
pause
exit /b 1

:success
echo.
echo ✅ Dataset optimization completed successfully!
echo.
pause 