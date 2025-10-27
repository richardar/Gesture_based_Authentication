<#
Installer script for Windows PowerShell.

Usage:
  .\install.ps1            # create venv and install minimal recommended packages
  .\install.ps1 -Full     # install full set from requirements.txt (may be large)

#>

param(
    [switch]$Full
)

Write-Host "Gesture_Based_Authentication installer"

$venvPath = Join-Path $PSScriptRoot '.venv'
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath"
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists at $venvPath"
}

Write-Host "To activate run: .\$venvPath\Scripts\Activate.ps1"

if ($Full) {
    Write-Host "Installing full requirements (this can be large and slow)..."
    & "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
    & "$venvPath\Scripts\python.exe" -m pip install -r "$PSScriptRoot\requirements.txt"
    Write-Host "Full install complete."
    return
}

Write-Host "Installing minimal recommended packages (opencv, pillow, pyttsx3)"
& "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$venvPath\Scripts\python.exe" -m pip install opencv-python Pillow pyttsx3 Flask

Write-Host "Done. Activate your venv and run: python app.py or python webui.py"
