@echo off
setlocal enabledelayedexpansion

:: Remove existing vitmatte_using_hf directory if it exists
if exist vitmatte_using_hf (
    echo Removing existing vitmatte_using_hf directory...
    rmdir /s /q vitmatte_using_hf
    if %errorLevel% neq 0 (
        echo Failed to remove existing vitmatte_using_hf directory.
        pause
        exit /b 1
    )
)

:: Clone the repository
echo Cloning the repository...
git clone https://github.com/prashkrans/viTmatte_using_hf.git
if %errorLevel% neq 0 (
    echo Failed to clone the repository.
    pause
    exit /b 1
)
cd vitmatte_using_hf

:: Create and activate virtual environment
echo Creating and activating virtual environment...
python -m venv env_vitmatte
if %errorLevel% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)
call env_vitmatte\Scripts\activate.bat

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo Failed to install requirements.
    pause
    exit /b 1
)


echo Setup complete!
pause