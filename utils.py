import time
from handlers import *



class HeaderParser():
    def __init__(self, req):
        self.req = req
        body_index = self.req.find('\r\n\r\n')
        if body_index>=0:
            self.body=self.req[body_index+4:]
        else:
            self.body=""
        self.req = self.req.split('\n')

    def get_method(self):
        #try to parse http method, if failed then return None
        try:
            method = self.req[0].split()[0]
            if method=='GET' or method=='POST' or method=='PUT' or method=='CONNECT' or method=='DELETE':
                return method
        except:
            pass
        return None

    def get_URI(self):
        return self.req[0].split()[1]

    def get_resource(self):
        return self.req[0].split()[1].split("?")[0]

    def get_host(self):
        return self.req[1].split(":")[1].strip()

    def get_GET_params(self):
        #attempt to obtain GET params. returns a dictionary if paramters are parsed correctly
        #otherwise the method reutrns None.
        buff = None
        try:
            buff={}
            #parse the first line of the HTTP request and look for parameters
            #in the URI, by using ? as a delimeter for the split function
            parsed=self.req[0].split()[1].split("?")[1]
            for param in parsed.split("&"):
                param_name=param.split("=")[0]
                param_val=param.split("=")[1]
                buff.update({param_name: param_val})
        except:
            pass
        return buff

    def get_body(self):
        return self.body

    def get_POST_params(self):
        #attempt to obtain POST request parameters. and then return the result in
        # dictionary, otherwise return None
        buff=None
        try:
            buff={}

            for param in self.body.split("&"):
                param_name=param.split("=")[0]
                param_val=param.split("=")[1]
                buff.update({param_name: param_val})
        except:
            pass
        return buff

    def get_cookie(self):
        cookie = None
        for line in self.req:
            if line.find("Cookie")!=-1:
                cookie=line
                break
        return cookie 


class RequestHandler():
    def __init__(self, sock, req, cnf):
        self.sock = sock
        self.req = req
        self.cnf = cnf

    def serve(self):
        #HttpResponse(self.sock).not_found_404()
        parsed = HeaderParser(self.req)
        res_type="html"
        response_generator=HttpResponse(self.sock,self.cnf)

        if parsed.get_method()=='GET' and self.cnf.get('METHODS' , 'GET')=='enabled':
            GETRequestHandler(parsed,self.sock,self.cnf).handle()

        elif parsed.get_method()=='DELETE' and self.cnf.get('METHODS' , 'DELETE')=='enabled':
            DELETERequestHandler(parsed,self.sock,self.cnf).handle()

        elif parsed.get_method()=='PUT' and self.cnf.get('METHODS' , 'PUT')=='enabled':
            PUTRequestHandler(parsed,self.sock,self.cnf).handle()

        elif parsed.get_method()=='POST' and self.cnf.get('METHODS' , 'POST')=='enabled':
            POSTRequestHandler(parsed,self.sock,self.cnf).handle()

        elif parsed.get_method()=='CONNECT' and self.cnf.get('METHODS' , 'CONNECT')=='enabled':
            CONNECTRequestHandler(parsed,self.sock,self.cnf).handle()

        else:
            HttpResponse(self.sock, self.cnf).not_found_404("<h1>METHOD NOT FOUND</h1>")

        self.sock.close()

def multi_threading_wrapper(connection , data , config):
    RequestHandler(connection , data , config).serve()
