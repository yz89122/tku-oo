
from collections import defaultdict
import json
import threading

import tornado.web
import tornado.ioloop

from employee.EmployeeDBHandler import EmployeeDBHandler
from employee import Employee
from nio.contract import Contract as C

class RequestHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def missing_arg(self, key):
        self.clear()
        self.set_status(400)
        self.finish(json.dumps({
            C.STATUS: C.FAILED,
            C.INFO: 'missing ' + str(key)
        }))

class TestHandler(RequestHandler):
    def get(self):
        self.write("Hello world!")

class EmployeeListAllHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(
            e.to_dict() for e in self.db.list_all()
        )))

class EmployeeAddHandler(RequestHandler):

    REQUIRED_ARGS = (
        'id',
        'type',
        'name',
    )
    WORKER_REQUIRED = (
        'shift',
        'rate'
    )
    SUPERVISOR_REQUIRED = (
        'salary',
        'bonus'
    )

    def __init__(self, *args, **kwargs):
        self.get = self.handle
        self.post = self.handle
        super().__init__(*args, **kwargs)

    def handle(self):
        args_result = dict()
        for required in EmployeeAddHandler.REQUIRED_ARGS:
            a = self.get_argument(required, None)
            if a is None:
                self.missing_arg(required)
                return
            args_result[required] = a
        if args_result['type'] == 'worker':
            for required in EmployeeAddHandler.WORKER_REQUIRED:
                a = self.get_argument(required, None)
                if a is None:
                    self.missing_arg(required)
                    return
                args_result[required] = a
        else:
            for required in EmployeeAddHandler.SUPERVISOR_REQUIRED:
                a = self.get_argument(required, None)
                if a is None:
                    self.missing_arg(required)
                    return
                args_result[required] = a
        e = Employee.make_employee(args_result)
        self.db.add_or_update(e)
        self.set_status(200)
        self.write(json.dumps({C.STATUS: C.SUCCESS}))

class EmployeeExistHandler(RequestHandler):
    def get(self):
        id = self.get_argument('id', None)
        if id is None:
            self.missing_arg('id')
            return
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({
            C.STATUS: C.SUCCESS,
            C.EXISTENCE: self.db.exist(id)
        }))

class EmployeeGetById(RequestHandler):
    def get(self):
        id = self.get_argument('id', None)
        if id is None:
            self.missing_arg('id')
            return
        e = self.db.get_by_id(id)
        if e is None:
            self.write(json.dumps({C.STATUS: C.FAILED}))
            return
        self.write(json.dumps({
            C.STATUS: C.SUCCESS,
            C.EMPLOYEE: e.to_dict()
        }))

class EmployeeDelete(RequestHandler):
    def get(self):
        id = self.get_argument('id', None)
        if id is None:
            self.missing_arg('id')
            return
        self.db.delete(id)
        self.write(json.dumps({
            C.STATUS: C.SUCCESS
        }))

class Server:
    def __init__(self, db_path='Employee.db', port=8080):
        self.__port = port
        self.__db_path = db_path

    def serve_forever(self):
        with EmployeeDBHandler(self.__db_path) as db:
            app = tornado.web.Application([
                (r"/", TestHandler, dict(db=db)),
                (r"/list_all", EmployeeListAllHandler, dict(db=db)),
                (r"/add", EmployeeAddHandler, dict(db=db)),
                (r"/exist", EmployeeExistHandler, dict(db=db)),
                (r"/get_by_id", EmployeeGetById, dict(db=db)),
                (r"/delete", EmployeeDelete, dict(db=db)),
            ])
            app.listen(self.__port)
            tornado.ioloop.IOLoop.current().start()
