# Vulnerable Web Server
A web server written entirely from scratch with the following features:

* GET, POST, PUSH, DELETE, and CONNECT methods are supported. they can be enabled and disabled from the config file.
* Static HTML, CSS, Javascript, and PHP are supported.
* $_GET and $_POST parameters are supported in php.
* Limited support for session management. the server gives a cookie to every request made to a php script, and passes the cookie to the php interpreter using $PHPESSID variable.
* HTTP responses are implemented (200, 404, 400, 500, 505).<return>
* Request and error logging
* Multiple vulnerabilities :)

The server requires the following to run:
* Python 2.7
* PHP 
* mysql (if you are using database)

## To run it: <return>
python main.py sample.cnf

## Final words:<return>
This project was just an assignment for one of my courses. don't take me as someone who enjoys reinventing the wheel!



