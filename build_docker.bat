@echo off
setlocal

set TOML_CLI=toml
set TOML_FILE=pyproject.toml

for /f "usebackq tokens=* delims=" %%a in (`%TOML_CLI% get "%TOML_FILE%" project.version`) do (
    set "VERSION=%%a"
)

echo Building docker image for version: %VERSION%
docker build -t billschumacher/athena:%VERSION% .