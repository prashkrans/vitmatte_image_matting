@echo off
setlocal

:: Change directory to viTmatte_using_hf
cd /d "C:\Workspace\image_matting\viTmatte_using_hf"

:: Activate the virtual environment
call env_vitmatte\Scripts\activate

:: Run main.py
echo Starting image matting...
python main.py
if %errorLevel% neq 0 (
    echo Failed to run main.py.
    pause
    exit /b 1
)


endlocal
