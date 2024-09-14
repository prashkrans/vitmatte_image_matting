@echo off
setlocal enabledelayedexpansion

:: Remove existing vitmatte_image_matting directory if it exists
if exist vitmatte_image_matting (
    echo Removing existing vitmatte_image_matting directory...
    rmdir /s /q vitmatte_image_matting
    if %errorLevel% neq 0 (
        echo Failed to remove existing vitmatte_image_matting directory.
        pause
        exit /b 1
    )
)

:: Clone the repository
echo Cloning the repository...
git clone https://github.com/prashkrans/vitmatte_image_matting.git
if %errorLevel% neq 0 (
    echo Failed to clone the repository.
    pause
    exit /b 1
)
cd vitmatte_image_matting

:: Download the model using curl
echo Downloading the viTMatte checkpoint model...
curl -L -o ".\checkpoints\pytorch_model.bin" "https://huggingface.co/hustvl/vitmatte-base-composition-1k/resolve/main/pytorch_model.bin"
if %ERRORLEVEL% neq 0 (
    echo Failed to download the model.
    pause
    exit /b 1
)

:: Create and activate virtual environment
echo Creating and activating virtual environment...
python -m venv env_vit
if %errorLevel% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)
call env_vit\Scripts\activate.bat

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