@echo off
setlocal

set TOML_CLI=toml
set TOML_FILE=pyproject.toml

for /f "usebackq tokens=* delims=" %%a in (`%TOML_CLI% get "%TOML_FILE%" project.version`) do (
    set "VERSION=%%a"
)

echo Building docker image for version: %VERSION%
docker build -t billschumacher/athena:%VERSION% .
docker build -t billschumacher/athena .
docker push billschumacher/athena:%VERSION%
docker push billschumacher/athena
rm dist -r
python -m build
python -m twine upload --repository testpypi dist/
python -m twine upload --repository pypi dist/