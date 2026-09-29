# Runbook

This runbook explains how to clone, install, run, and verify the Day 5 ship-prep
increment from a clean machine.

## Requirements

- Git
- Python 3.12
- `uv`

## Get The Code

Unzip the handover file and enter the project folder:

```bash
unzip day5-ship-prep.zip
cd day5-ship-prep
```

## Install

Create a virtual environment:

```bash
uv venv .venv --python 3.12
```

Install the required tools and test dependencies.

Mac/Linux:

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

Windows:

```powershell
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

If the virtual environment is already activated, this also works:

```bash
uv pip install -r requirements.txt
```

## Run

Mac/Linux:

```bash
.venv/bin/python -m ruff check .
.venv/bin/python -m mypy src tests
.venv/bin/python -m pytest -q
bash smoke.sh
```

Windows PowerShell:

```powershell
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m mypy src tests
.venv\Scripts\python.exe -m pytest -q
bash smoke.sh
```

## Expected Output

A successful run should end with output like this:

```text
All checks passed!
Success: no issues found in 2 source files
8 passed
smoke OK: reconcile matched, worst_line correct, empty handled
```

`pytest` may print extra timing information depending on the local environment.
The important result is that all gates pass and `smoke.sh` exits successfully.
