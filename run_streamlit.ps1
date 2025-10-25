param()

# run_streamlit.ps1
# Activates the project venv (if available) and runs Streamlit for this repo's app.py.
# Usage: Open PowerShell in the repo and run: & ./run_streamlit.ps1

Set-StrictMode -Version Latest

$repoRoot = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
$venvPath = Join-Path $repoRoot 'venv'
$activateScript = Join-Path $venvPath 'Scripts\\Activate.ps1'
$venvPython = Join-Path $venvPath 'python.exe'

Write-Host "Repository root: $repoRoot"
Write-Host "Looking for venv at: $venvPath"

if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..."
    # Allow running the activation script in this process
    Try {
        Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
    } Catch {
        Write-Host "Warning: couldn't set execution policy: $_"
    }

    & $activateScript
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: activation returned exit code $LASTEXITCODE"
    } else {
        Write-Host "Virtual environment activated."
    }
} else {
    Write-Host "No Activate.ps1 found at $activateScript — will use venv python directly."
}

# Prefer to call streamlit directly if available in the environment; otherwise use venv python -m streamlit
function Invoke-Streamlit {
    param([string[]]$Args)

    # If there's a streamlit command available, use it
    $cmd = Get-Command streamlit -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Host "Running streamlit via: $($cmd.Source)"
        & streamlit @Args
        return $LASTEXITCODE
    }

    if (Test-Path $venvPython) {
        Write-Host "streamlit not on PATH — falling back to venv python at $venvPython"
        & $venvPython -m streamlit @Args
        return $LASTEXITCODE
    }

    throw "No streamlit command found and venv python not present at $venvPython"
}

try {
    $appPath = Join-Path $repoRoot 'app.py'
    if (-not (Test-Path $appPath)) {
        throw "app.py not found in repo root: $repoRoot"
    }

    Write-Host "Starting Streamlit for $appPath"
    Invoke-Streamlit 'run' $appPath
} catch {
    Write-Host "ERROR: $_"
    exit 1
}
