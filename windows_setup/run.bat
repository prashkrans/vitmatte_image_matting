@echo off
setlocal

:: Change directory to viTmatte_using_hf
cd /d viTmatte_using_hf

:: Activate the virtual environment
call env_vitmatte\Scripts\activate

:: Run main.py in a new window, minimized
start /min "" cmd /c "python main.py && exit"

:: Wait for the Python script to finish
:wait_loop
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 2 >nul
    goto wait_loop
)

endlocal