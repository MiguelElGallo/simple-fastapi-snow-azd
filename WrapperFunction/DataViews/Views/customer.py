import logging as log
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import session 
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate, select 

from WrapperFunction.DbConn.dbconnection import get_db

#from WrapperFunction.DataViews.TableModels import User as UserModel
from WrapperFunction.DataViews.TableModels import Customer as CustomerModel

router = APIRouter(prefix="/customer", tags=["customer"])


class CustomerSchemaBase(BaseModel):
    c_name: str | None = None



class CustomerSchemaCreate(CustomerSchemaBase):
    pass


class CustomerSchema(CustomerSchemaBase):
    c_custkey: int | None = None

    class Config:
        from_attributes = True


@router.get("/get-customer", response_model=CustomerSchema, description='Get a customer by C_KEY')
def get_customer(c_custkey: int , db: session = Depends(get_db)):
    log.info("(customer.py) Getting customer with c_custkey: %s", c_custkey)
    customer = CustomerModel.get(db, c_custkey)
    return customer


@router.get("/get-customers", response_model=Page[CustomerSchema])
def get_customers(db: session = Depends(get_db)):
    log.info("(customer.py) Getting all customers")
    customers = paginate(db, select(CustomerModel).order_by(CustomerModel.c_custkey))
    return customers


