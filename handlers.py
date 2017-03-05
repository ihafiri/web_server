import time
import os
import socket
import subprocess
import random
import string
import md5

def file_name_gen(size=6):
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set*6, 6))

class Logger():
    def __init__(self,sock,parsed,cnf):
        self.sock = sock
        self.parsed_header=parsed
        self.cnf = cnf

    def access_log(self,code):
        file_ptr=open(self.cnf.get('LOG' , 'AccessLog'), "a")
        file_ptr.write("\n"+self.sock.getpeername()[0]+" - - ["+time.strftime("%d/%m/%Y:%H:%M:%S")+" "+code+" "+self.parsed_header.get_method()+" "+self.parsed_header.get_URI())
        file_ptr.close()

class HttpResponse():
    def __init__(self,sock,cnf):
        self.sock = sock
        self.cnf=cnf

    def not_found_404(self,body):
        self.sock.send("HTTP/1.1 404 Not Found\nConnection: close\n\n"
        +body+"\n")

    def forbidden_403(self , body="<h1>CANNOT ACCESS FILE</h1>"):
        self.sock.send("HTTP/1.1 403 Forbidden \n")
        self.sock.send("HTTP/1.1 200 OK\n"
        +"Content-Type: text/html\n"
        +"\n" # Important!
        +body+"\n")

    def bad_request_400(self):
        #browser has white screen
        self.sock.send("HTTP/1.1 400 Bad Request\n"
        +"Content-Type: text/html\n"
        +"\n"
        +"\n")

    def unauthorized_401(self):
        self.sock.send("HTTP/1.1 401 Unauthorized")

    def OK_200(self,body,res_type='html',spec_header=""):
        self.sock.send("HTTP/1.1 200 OK\n"
        +"Content-Type: text/"+res_type+"\n"
        +spec_header+"\n"
        +"\n" # Important!
        +body+"\n")

class POSTRequestHandler():
    def __init__(self, parsed_req,sock,cnf):
        self.parsed_req=parsed_req
        self.sock=sock
        self.cnf=cnf
        self.response_generator=HttpResponse(self.sock,self.cnf)

    def serve_static_content(self , file_path, res_type):
        try:
            page_ptr=open(file_path,"r")
            self.response_generator.OK_200(page_ptr.read() , res_type)
            Logger(self.sock,self.parsed_req,self.cnf).access_log("200")
                    #print self.parsed_req.get_host()
        except:
                self.response_generator.forbidden_403()
                Logger(self.sock,self.parsed_req,self.cnf).access_log("403")

    def serve_php(self , file_path):
        #generate a file with random name to pass for the php processor. this file contains GET, POST,and other params

        params = self.parsed_req.get_POST_params()
        cookie = None
        set_cookie=""
        if self.parsed_req.get_cookie() is None:
            #print self.parsed_req.get_cookie().split(": ")[1]
            m = md5.new()
            m.update(file_name_gen())
            cookie =m.hexdigest()
            set_cookie = "Set-Cookie: PHPESSID="+cookie+"\n"

        else:
            cookie = self.parsed_req.get_cookie().split(": ")[1].split("=")[1]

        read_php = open(file_path , "r")
        if read_php.readline() !="<?php include $argv[1];?>\n":
            read_php.seek(0)
            buff = read_php.read()
            read_php.close()
            modify_php = open(file_path , "w")
            modify_php.write("<?php include $argv[1];?>\n")
            modify_php.write(buff)
            modify_php.close()

        tmp = self.cnf.get('SRVCONF' , 'tmpDir')+"/"+file_name_gen()+".php"
        tmp_file = open( tmp, "w")
        tmp_file.write("<?php ")
        tmp_file.write("$_POST=array(")
        for key in params:
            tmp_file.write("'"+key+"'"+"=>"+"'"+params[key]+"',")
        tmp_file.write(");"+"$"+"PHPESSID='"+cookie+"';?>")
        tmp_file.close()
        #construct and execute php command
        command = 'php ' + file_path +' '+tmp
        data = subprocess.check_output(command, shell=True)
        self.response_generator.OK_200(data,spec_header=set_cookie)
        os.remove(tmp)

    def handle(self):
        res_type="html"
        file_name=self.parsed_req.get_resource()

        if file_name=="/":
            file_name="/"+self.cnf.get('SRVCONF' , 'IndexPage') # this is to be added to config file

        file_path=self.cnf.get('SRVCONF' , 'RootDIR')+file_name

        if not os.path.isfile(file_path):
            self.response_generator.not_found_404("<h1>NOT FOUND!</h1>")
            Logger(self.sock,self.parsed_req,self.cnf).access_log("403")

        elif file_name.find("css") !=-1: # change variable based on doc type (default is html)
            self.serve_static_content(file_path ,"css")

        elif file_name.find("htm") !=-1:
            self.serve_static_content(file_path,"html")

        elif file_name.find('php') !=-1:
            self.serve_php(file_path)


class GETRequestHandler():
    def __init__(self, parsed_req,sock,cnf):
        self.parsed_req=parsed_req
        self.sock=sock
        self.cnf=cnf
        self.response_generator=HttpResponse(self.sock,self.cnf)

    def serve_static_content(self , file_path, res_type):
        try:
            page_ptr=open(file_path,"r")
            self.response_generator.OK_200(page_ptr.read() , res_type)
            Logger(self.sock,self.parsed_req,self.cnf).access_log("200")
                    #print self.parsed_req.get_host()
        except:
                self.response_generator.forbidden_403()
                Logger(self.sock,self.parsed_req,self.cnf).access_log("403")

    def serve_php(self , file_path):
        #generate a file with random name to pass for the php processor. this file contains GET, POST,and other params
        set_cookie=""
        cookie= None
        params = self.parsed_req.get_GET_params()

        if self.parsed_req.get_resource()=="/logout.php":
            print "dead!"

            #set a new if not already or a logout page was requested
        if self.parsed_req.get_cookie() is None or self.parsed_req.get_resource()==self.cnf.get('SESSION','LOGOUT'):
            #print self.parsed_req.get_cookie().split(": ")[1]
            m = md5.new()
            m.update(file_name_gen())
            cookie =m.hexdigest()
            set_cookie = "Set-Cookie: PHPESSID="+cookie+"\n"

        else:
            cookie = self.parsed_req.get_cookie().split(": ")[1].split("=")[1]

        read_php = open(file_path , "r")
        if read_php.readline() !="<?php include $argv[1];?>\n":
            read_php.seek(0)
            buff = read_php.read()
            read_php.close()
            modify_php = open(file_path , "w")
            modify_php.write("<?php include $argv[1];?>\n")
            modify_php.write(buff)
            modify_php.close()
        read_php.close()

        tmp = self.cnf.get('SRVCONF' , 'tmpDir')+"/"+file_name_gen()+".php"
        tmp_file = open( tmp, "w")
        tmp_file.write("<?php ")
        tmp_file.write("$_GET=array(")
        for key in params:
            tmp_file.write("'"+key+"'"+"=>"+"'"+params[key]+"',")
        tmp_file.write(");"+"$"+"PHPESSID='"+cookie+"';?>")
        tmp_file.close()
        #construct and execute php command
        command = 'php ' + file_path +' '+tmp
        data = subprocess.check_output(command, shell=True)
        self.response_generator.OK_200(data , spec_header=set_cookie)
        os.remove(tmp)

    def handle(self):
        res_type="html"
        file_name=self.parsed_req.get_resource()

        if file_name=="/":
            file_name="/"+self.cnf.get('SRVCONF' , 'IndexPage') # this is to be added to config file

        file_path=self.cnf.get('SRVCONF' , 'RootDIR')+file_name

        if not os.path.isfile(file_path):
            self.response_generator.not_found_404("<h1>NOT FOUND!</h1>")
            Logger(self.sock,self.parsed_req,self.cnf).access_log("403")

        elif file_name.find("css") !=-1: # change variable based on doc type (default is html)
            self.serve_static_content(file_path ,"css")

        elif file_name.find("htm") !=-1:
            self.serve_static_content(file_path,"html")

        elif file_name.find('php') !=-1:
            self.serve_php(file_path)

class DELETERequestHandler():
    def __init__(self, parsed_req,sock,cnf):
        self.parsed_req=parsed_req
        self.sock=sock
        self.cnf=cnf
        self.response_generator=HttpResponse(self.sock,self.cnf)

    def handle(self):
        file_name=self.parsed_req.get_resource()
        file_path=self.cnf.get('SRVCONF' , 'RootDIR')+file_name

        try:
            os.remove(file_path)
            self.response_generator.OK_200("File "+file_path+" deleted","html")
            Logger(self.sock,self.parsed_req,self.cnf).access_log("200")
        except OSError:
            self.response_generator.not_found_404("<h1>NOT FOUND!</h1>")
            Logger(self.sock,self.parsed_req,self.cnf).access_log("404")

class PUTRequestHandler():
    def __init__(self, parsed_req,sock,cnf):
        self.parsed_req=parsed_req
        self.sock=sock
        self.cnf=cnf
        self.response_generator=HttpResponse(self.sock,self.cnf)

    def handle(self):
        file_name=self.parsed_req.get_resource()
        file_path=self.cnf.get('SRVCONF' , 'RootDIR')+file_name
        body =self.parsed_req.get_body()
        try:
            file_ptr=open(file_path, "w")
            file_ptr.write(body)
            file_ptr.close()
            self.response_generator.OK_200("PUT OPERATION SUCCESSFUL","html")
            Logger(self.sock,self.parsed_req,self.cnf).access_log("200")
        except:
            self.response_generator.not_found_404("<h1>NOT FOUND!</h1>")
            Logger(self.sock,self.parsed_req,self.cnf).access_log("404")

class CONNECTRequestHandler():
    def __init__(self, parsed_req,sock,cnf):
        self.parsed_req=parsed_req
        self.sock=sock
        self.cnf=cnf
        self.response_generator=HttpResponse(self.sock,self.cnf)

    def handle(self):
#CONNECT tunneling handles one request at a time.
        uri = self.parsed_req.get_URI()

        try:
            dest_host = uri.split(":")[0]
            dest_port = uri.split(":")[1]
            dest_addr = (dest_host ,int(dest_port))
            prox_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            prox_sock.connect(dest_addr)
            self.response_generator.OK_200("")
            data = self.sock.recv(2048)
            prox_sock.send(data)
            data= prox_sock.recv(2048)
            self.sock.send(data)
            prox_sock.close()
        except:
            self.response_generator.bad_request_400()
