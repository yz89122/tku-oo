# from socketserver import BaseRequestHandler
# from socketserver import TCPServer
from collections import defaultdict
import json
import socket
import threading

from employee.EmployeeDBHandler import EmployeeDBHandler
from employee import Employee
from nio.contract import Contract as C

class RequestHandler:
    def __init__(self, db: EmployeeDBHandler, sock, addr):
        self.__db = db
        self.__data = bytes()
        self.__op = defaultdict(self.__unknown_op, {
            C.ADD_EMPLOYEE: self.__add_employee,
            C.CHECK_EXISTENCE: self.__check_exist,
            C.LIST_ALL: self.__list_all,
            C.GET_BY_ID: self.__get_by_id,
            C.DELETE_BY_ID: self.__delete_by_id,
            C.HELLO: self.__client_hello
        })
        self.__sock = sock
        self.__sock.setblocking(True)
        self.__addr = addr

    def __get_msg(self) -> str:
        while True:
            r = self.__sock.recv(2048)
            if len(r) == 0:
                raise Exception()
            if len(self.__data) + len(r) > 20480:
                self.__bad_request()
                raise Exception()
            self.__data += r
            i = self.__data.find(C.SEPARATOR)
            if i != -1:
                msg = self.__data[:i].decode(C.ENCODING)
                self.__data = self.__data[i + len(C.SEPARATOR):]
                return msg

    def __send_msg(self, msg):
        if isinstance(msg, bytes):
            data = msg
        else:
            data = str(msg).encode(C.ENCODING)
        data += C.SEPARATOR
        print('sent', self.__sock.getpeername(), data)
        self.__sock.sendall(data)

    def __not_correct_json(self):
        self.__send_msg(json.dumps({
            C.STATUS: C.FAILED,
            C.INFO: 'failed to parse json'
        }))

    def __missing_parameters(self):
        self.__send_msg(json.dumps({
            C.STATUS: C.FAILED,
            C.INFO: 'missing parameters'
        }))

    def __unknown_op(self, r=None):
        self.__send_msg(json.dumps({
            C.STATUS: C.FAILED,
            C.INFO: 'unknown operation'
        }))

    def __bad_request(self, r=None):
        self.__send_msg(json.dumps({
            C.STATUS: C.FAILED,
            C.INFO: 'WTF?'
        }))

    def __client_hello(self, r=None):
        self.__send_msg(json.dumps({C.STATUS: C.SUCCESS}))

    def __add_employee(self, request):
        if C.EMPLOYEE not in request:
            self.__missing_parameters()
            return
        e = Employee.make_employee(request[C.EMPLOYEE])
        if e is None:
            self.__missing_parameters()
            return
        self.__db.add_or_update(e)
        self.__send_msg(json.dumps({C.STATUS: C.SUCCESS}))

    def __check_exist(self, request):
        if C.ID not in request:
            self.__missing_parameters()
            return
        self.__send_msg(json.dumps({
            C.STATUS: C.SUCCESS,
            C.EXISTENCE: self.__db.exist(request[C.ID])
        }))

    def __list_all(self, r=None):
        self.__send_msg(json.dumps({
            C.STATUS: C.SUCCESS,
            C.EMPLOYEES: list(
                e.to_dict() for e in self.__db.list_all()
            )
        }))

    def __get_by_id(self, request):
        if C.ID not in request:
            self.__missing_parameters()
            return
        employee = self.__db.get_by_id(request[C.ID])
        if employee is None:
            self.__send_msg(json.dumps({C.STATUS: C.FAILED}))
            return
        self.__send_msg(json.dumps({
            C.STATUS: C.SUCCESS,
            C.EMPLOYEE: employee.to_dict()
        }))

    def __delete_by_id(self, request):
        if C.ID not in request:
            self.__missing_parameters()
            return
        id = request[C.ID]
        if self.__db.exist(id):
            self.__send_msg(json.dumps({
                C.STATUS: C.SUCCESS
            }))
            self.__db.delete(id)
        else:
            self.__send_msg(json.dumps({
                C.STATUS: C.FAILED,
                C.INFO: C.NOT_EXIST
            }))

    def __handle(self):
        peer = self.__sock.getpeername()
        print(peer, 'connected')
        try:
            while True:
                msg = self.__get_msg()
                print('recv', peer, msg)
                try:
                    request = json.loads(msg)
                except json.decoder.JSONDecodeError:
                    self.__not_correct_json()
                if C.OPERATION in request:
                    self.__op[request[C.OPERATION]](request)
                else:
                    self.__unknown_op()
        except:
            print(peer, 'closed')
            self.__sock.close()

    def handle(self):
        threading.Thread(target=self.__handle).start()

class Server:
    def __init__(self, db_path, port=20001):
        self.__port = port
        self.__db_path = db_path

    def serve_forever(self):
        with EmployeeDBHandler(self.__db_path) as db:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', self.__port))
            s.listen(8)
            while True:
                sock, addr = s.accept()
                handler = RequestHandler(db, sock, addr)
                handler.handle()
