
import logging as log
from sqlalchemy import Column, String, exc
from sqlalchemy.exc import  NoResultFound
from fastapi_pagination.ext.sqlalchemy import paginate
from WrapperFunction.DbConn.dbconnection import Base
from fastapi_pagination import Page
from fastapi import Query
from fastapi_pagination.ext.sqlalchemy import select 

Page = Page.with_custom_options(
       size=Query(100, ge=1, le=500),
       )


class Customer(Base):
    """
    Represents a customer in the database.

    Attributes:
        c_custkey (str): The primary key of the customer.
        c_name (str): The name of the customer.
    """

    __tablename__ = "customer"
    c_custkey = Column(String, primary_key=True)
    c_name = Column(String, nullable=False)


    @classmethod
    def get(cls, db, c_custkey: str):
        """
        Retrieves a customer from the database by their primary key.

        Args:
            db: The database connection.
            c_custkey (str): The primary key of the customer.

        Returns:
            The customer object if found, None otherwise.
        """
        try:
            log.info("Getting customer with c_custkey: %s", c_custkey)
            transaction = db.get(cls, c_custkey)
        except NoResultFound:
            log.warn("Customer with c_custkey: %s not found", c_custkey)
            return None
        return transaction

    #@classmethod
    
    def get_all(cls, db, 
                page: int = Query(1, ge=1), 
                per_page: int = Query(100, ge=0)
    ):
        """
        Retrieves all customers from the database.

        Args:
            db: The database connection.

        Returns:
            A paginated list of customer objects.
        """
        try:
            log.info("Getting all customers page: %s per_page: %s", page, per_page)
            limit = per_page * page
            offset = (page - 1) * per_page
        except exc.SQLAlchemyError as e:
            log.error("Error getting all customers: %s", e)
            raise e

        return paginate(conn = db, query = select(cls).order_by(cls.c_custkey), limit = limit, offset = offset)


