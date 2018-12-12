import socket
import json
from collections import defaultdict

from employee import Employee
from nio.contract import Contract as C

class Connector:
    def __init__(self, server, port):
        self.__server = server
        self.__port = port
        self.__socket = socket.socket()
        self.__socket.setblocking(True)
        self.__buffer = bytes()

    def send(self, msg):
        if isinstance(msg, bytes):
            data = msg
        else:
            data = str(msg).encode(C.ENCODING)
        data += C.SEPARATOR
        self.__socket.sendall(data)

    def recv(self):
        while not self.__socket._closed:
            r = self.__socket.recv(2048)
            if len(r) == 0:
                raise Exception()
            if len(self.__buffer) + len(r) > 409600:
                raise Exception('buffer reached limit')
            self.__buffer += r
            i = self.__buffer.find(C.SEPARATOR)
            if i != -1:
                msg = self.__buffer[:i].decode(C.ENCODING)
                self.__buffer = self.__buffer[i + len(C.SEPARATOR):]
                return msg

    def __enter__(self):
        self.__socket.connect((self.__server, self.__port))
        return self

    def __exit__(self, *args):
        self.__socket.close()

class RequestHandler:
    def __init__(self, connector: Connector):
        self.__connector = connector

    def __s(self, o):
        self.__connector.send(json.dumps(o))

    def __r(self):
        try:
            return json.loads(self.__connector.recv())
        except:
            return False

    def check_server(self):
        self.__s({C.OPERATION: C.HELLO})
        return RequestHandler.__check_response(self.__r())

    @staticmethod
    def __check_response(response, types={}):
        if C.STATUS not in response or \
                response[C.STATUS] != C.SUCCESS:
            return False
        for k, v in types.items():
            if k not in response:
                return False
            if not isinstance(response[k], v):
                return False
        return True

    def add_employee(self, employee: Employee.Employee):
        self.__s({
            C.OPERATION: C.ADD_EMPLOYEE,
            C.EMPLOYEE: employee.to_dict()
        })
        return RequestHandler.__check_response(self.__r())

    def check_existence(self, id):
        self.__s({
            C.OPERATION: C.CHECK_EXISTENCE,
            C.ID: id
        })
        response = self.__r()
        if RequestHandler.__check_response(response, {C.EXISTENCE: bool}):
            return response[C.EXISTENCE]

    def get_by_id(self, id):
        self.__s({
            C.OPERATION: C.GET_BY_ID,
            C.ID: id
        })
        response = self.__r()
        if RequestHandler.__check_response(response, {C.EMPLOYEE: dict}):
            return Employee.make_employee(response[C.EMPLOYEE])

    def list_all(self):
        self.__s({C.OPERATION: C.LIST_ALL})
        response = self.__r()
        if RequestHandler.__check_response(response, {C.EMPLOYEES: list}):
            return response[C.EMPLOYEES]
        return None
    
    def delete_employee(self, id):
        self.__s({
            C.OPERATION: C.DELETE_BY_ID,
            C.ID: id
        })
        response = self.__r()
        return self.__check_response(response)
