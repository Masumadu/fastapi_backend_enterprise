from sqlalchemy.exc import DBAPIError, IntegrityError

from app.core.database import Base, db
from app.core.exceptions import AppException

from .crud_repository_interface import CRUDRepositoryInterface


class SQLBaseRepository(CRUDRepositoryInterface):
    model: Base

    def __init__(self):
        """
        Base class to be inherited by all repositories. This class comes with
        base crud functionalities attached

        :param model: base model of the class to be used for queries
        """

        self.db = db

    def index(self) -> [Base]:
        """

        :return: {list} returns a list of objects of type model
        """
        try:
            data = self.db.query(self.model).all()
        except DBAPIError as exc:
            raise AppException.OperationError(error_message=exc.orig.args[0])
        return data

    def create(self, obj_in) -> Base:
        """

        :param obj_in: the data you want to use to create the model
        :return: {object} - Returns an instance object of the model passed
        """
        assert obj_in, "Missing data to be saved"

        try:
            obj_data = dict(obj_in)
            db_obj = self.model(**obj_data)
            self.db.add(db_obj)
            self.db.commit()
            return db_obj
        except IntegrityError as exc:
            self.db.rollback()
            raise AppException.OperationError(error_message=exc.orig.args[0])
        except DBAPIError as exc:
            self.db.rollback()
            raise AppException.OperationError(error_message=exc.orig.args[0])

    def update_by_id(self, obj_id, obj_in) -> Base:
        """
        :param obj_id: {int} id of object to update
        :param obj_in: {dict} update data. This data will be used to update
        any object that matches the id specified
        :return: model_object - Returns an instance object of the model passed
        """
        assert obj_id, "Missing id of object to update"
        assert obj_in, "Missing update data"
        assert isinstance(obj_in, dict), "Update data should be a dictionary"

        db_obj = self.find_by_id(obj_id)
        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as exc:
            self.db.session.rollback()
            raise AppException.OperationError(error_message=exc.orig.args[0])

    def update(self, query_info, obj_in):
        """
        :param query_info: {dict}
        :param obj_in: {dict}
        :return: model_object - Returns an instance object of the model passed
        """
        db_obj = self.find(query_info)
        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as exc:
            self.db.session.rollback()
            raise AppException.OperationError(error_message=exc.orig.args[0])

    def find_by_id(self, obj_id) -> Base:
        """
        returns an object matching the specified id if it exists in the database
        :param obj_id: id of object to query
        :return: model_object - Returns an instance object of the model passed
        """
        assert obj_id, "Missing id of object for querying"

        try:
            db_obj = self.db.query(self.model).get(obj_id)
            if not db_obj:
                raise AppException.NotFoundException(error_message=None)
            return db_obj
        except DBAPIError as exc:
            raise AppException.OperationError(error_message=exc.orig.args[0])

    def find(self, filter_param: dict) -> Base:
        """
        This method returns the first object that matches the query parameters specified
        :param filter_param {dict}. Parameters to be filtered by
        """
        assert filter_param, "Missing filter parameters"
        assert isinstance(
            filter_param, dict
        ), "Filter parameters should be of type dictionary"

        try:
            db_obj = self.db.query(self.model).filter_by(**filter_param).first()
            if not db_obj:
                raise AppException.NotFoundException(error_message=None)
            return db_obj
        except DBAPIError as exc:
            raise AppException.OperationError(error_message=exc.orig.args[0])

    def find_all(self, filter_param) -> Base:
        """
        This method returns all objects that matches the query
        parameters specified
        """
        assert filter_param, "Missing filter parameters"
        assert isinstance(
            filter_param, dict
        ), "Filter parameters should be of type dictionary"

        try:
            db_obj = self.model.query.filter_by(**filter_param).all()
            return db_obj
        except DBAPIError as exc:
            raise AppException.OperationError(error_message=exc.orig.args[0])

    def delete_by_id(self, obj_id):
        """
        :param obj_id:
        :return:
        """

        db_obj = self.find_by_id(obj_id)
        try:
            self.db.session.delete(db_obj)
            self.db.session.commit()
        except DBAPIError as exc:
            self.db.session.rollback()
            raise AppException.OperationError(error_message=exc.orig.args[0])
