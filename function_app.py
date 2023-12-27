"""
This script initializes a FastAPI application using the `WrapperFunction` module.
It then creates an Azure Function App using the `func.AsgiFunctionApp` class, with the FastAPI app as the argument.
The `http_auth_level` is set to `func.AuthLevel.ANONYMOUS`, allowing anonymous access to the function app.
"""
# Todo: Async based on: https://github.com/gpkc/fastapi-sqlalchemy-pytest First an Async connector for Snowflake is needed.

import azure.functions as func

from src.WrapperFunction import init_app as server 

fastapi_app = server()
app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
