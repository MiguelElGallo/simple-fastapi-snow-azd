import logging as log
from typing import Optional
from sqlalchemy import Column, String, exc
from sqlalchemy.exc import NoResultFound
from fastapi_pagination.ext.sqlalchemy import paginate
from WrapperFunction.DbConn.dbconnection import Base
from fastapi_pagination import Page
from fastapi import Query
from fastapi_pagination.ext.sqlalchemy import select
from fastapi_filter.contrib.sqlalchemy import Filter

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
    c_address = Column(String, nullable=False)
    c_nationkey = Column(String, nullable=False)
    c_phone = Column(String, nullable=False)

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

    # @classmethod

    def get_all(cls, db, page: int = Query(1, ge=1), per_page: int = Query(100, ge=0)):
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

        return paginate(
            conn=db,
            query=select(cls).order_by(cls.c_custkey),
            limit=limit,
            offset=offset,
        )


class CustomerFilter(Filter):

    """
    Represents a filter for customer data.

    Attributes:
        c_custkey (Optional[str]): The customer key.
        c_name (Optional[str]): The customer name.
        c_address (Optional[str]): The customer address.
        c_nationkey (Optional[str]): The customer nation key.
        c_phone (Optional[str]): The customer phone number.
    More info at: https://fastapi-filter.netlify.app/
    """

    order_by: Optional[list[str]] = {"c_custkey"}
    c_custkey: Optional[str] = None
    c_name: Optional[str] = None
    c_address: Optional[str] = None
    c_nationkey: Optional[str] = None
    c_phone: Optional[str] = None

    class Constants(Filter.Constants):
        """
        Constants class for defining model-specific constants.

        Attributes:
            model (Type[Model]): The model associated with the constants.
            ordering_field_name (str): The name of the field used for ordering.
            search_field_name (str): The name of the field used for searching.
            search_model_fields (List[str]): The list of model fields used for searching.
        """

        model = Customer
        ordering_field_name = "order_by"
        search_model_fields = ["c_name", "c_address", "c_nationkey"]
