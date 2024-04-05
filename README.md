# finance-tracker-backend

Finance tracker fastapi backend  

## Installation Instructions

1. pdm Installation
***NOTE:***
    - If your system's python is not aliased, use `python3 -` instead.
    - If you have multiple python3 versions, specify the version eg `python3.10`
```curl -sSL https://pdm.fming.dev/dev/install-pdm.py | python3 -```
2. Clone the repository and `cd` into `finance-tracker-backend`  
3. Install the required modules using `pdm install` in the project directory.

## Run the application

**Note**: You might need a .env file before running  
`pdm run uvicorn app.main:app --reload`  
