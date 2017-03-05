# Vulnerable Web Server
A web server written entirely from scratch with the following features:
<return>
* GET, POST, PUSH, DELETE, and CONNECT methods are supported. they can beenabled and disabled from the config file.<return>
* Static HTML, CSS, Javascript, and PHP are supported.<return>
* $_GET and $_POST parameters are supported in php.<return>
* Limited support for session management. the server gives a cookie to every request made to a php script, and passes the cookie to the php interpreter using $PHPESSID variable.<return>
* HTTP responses are implemented (200, 404, 400, 500, 505).<return>
* Request and error logging
* Multiple vulnerabilities :)<return>

## The server requires the following to run:
1- Python 2.7<return>
2- PHP <return>
3- mysql (if you are using database)<return>

## To run it: <return>
python main.py sample.cnf<return>

## Final words:<return>
This project was just an assignment for one of my courses. don't take me as someone who enjoys reinventing the wheel!



