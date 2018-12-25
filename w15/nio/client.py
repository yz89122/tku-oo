# import socket
import http.client
import urllib.parse
import json
from collections import defaultdict

from employee import Employee
from nio.contract import Contract as C

class RequestHandler:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port

    def request(self, path, args):
        list_args = list()
        for k, v in args.items():
            list_args.append(str(k) + '=' + str(v))
        a = '&'.join(list_args)
        connection = http.client.HTTPConnection(self.host, self.port, timeout=10)
        connection.request(
            'GET',
            path + '?' + a,
            headers={
                'Host': self.host
            }
        )
        with connection.getresponse() as response:
            try:
                return json.loads(response.read().decode(C.ENCODING))
            except:
                return dict()

    def post_request(self, path, args):
        connection = http.client.HTTPConnection(self.host, self.port, timeout=10)
        connection.request(
            'POST',
            path,
            headers={
                'Host': self.host,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body=urllib.parse.urlencode(args)
        )
        with connection.getresponse() as response:
            try:
                return json.loads(response.read().decode(C.ENCODING))
            except:
                return dict()

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
        e = employee.to_dict()
        response = self.post_request('/add', e)
        return RequestHandler.__check_response(response)

    def check_existence(self, id):
        response = self.request('/exist', {'id': id})
        if RequestHandler.__check_response(response, {C.EXISTENCE: bool}):
            return response[C.EXISTENCE]

    def get_by_id(self, id):
        response = self.request('/get_by_id', {'id': id})
        if RequestHandler.__check_response(response, {C.EMPLOYEE: dict}):
            return Employee.make_employee(response[C.EMPLOYEE])

    def list_all(self):
        return self.request('/list_all', {})
    
    def delete_employee(self, id):
        response = self.request('/delete', {'id': id})
        return self.__check_response(response)
