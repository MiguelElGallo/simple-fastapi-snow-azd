from fastapi import FastAPI, Query
from WrapperFunction.DbConn.dbconnection import sessionmanager 
from WrapperFunction.DbConn.config import config
from .DataViews.Views.customer import router as customer_router
from fastapi_pagination import add_pagination

def init_app(init_db=True):
    """
    Initializes the FastAPI server application.

    Args:
        init_db (bool, optional): Whether to initialize the database connection. Defaults to True.

    Returns:
        FastAPI: The initialized FastAPI server application.
    """
    lifespan = None

    if init_db:
        sessionmanager.init(config.DB_CONFIG)

        def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                sessionmanager.close()

    server = FastAPI(title="FastAPI server", lifespan=lifespan)
    server.include_router(customer_router, prefix="/api", tags=["customer"])
    add_pagination(server)
    
    return server




