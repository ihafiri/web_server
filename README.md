Vuln Web Server
A web server written entirely from scratch with the following features:
1- GET, POST, PUSH, DELETE, and CONNECT methods are supported. they can be enabled and disabled from the config file.
2- Static HTML, CSS, Javascript, and PHP are supported.
3- $_GET and $_POST parameters are supported in php
4- Limited support for session management. the server gives a cookie to every request made to a php script, and passes the cookie to the php interpreter using $PHPESSID variable.
5- http responses are implemented (200, 404, 400, 500, 505)
5- Multiple vulnerabilities :)

The server requires the following to run:
1- Python 2.7
2- PHP
3- mysql (if you are using database)

To run it:
python main.py sample.cnf

Final words:
This project was just an assignment for one of my courses. don't take me as someone who enjoys reinventing the wheel!



