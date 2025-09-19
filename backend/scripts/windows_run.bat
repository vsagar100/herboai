@echo off
REM Activate virtual environment
call ..\.venv1\Scripts\activate

REM Run FastAPI with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
