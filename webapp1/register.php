<?php include $argv[1];?>
<!DOCTYPE html>
<html>
<head>

<!-- your webpage info goes here -->

    <title>My First Website</title>

	<meta name="author" content="your name" />
	<meta name="description" content="" />

<!-- you should always add your stylesheet (css) in the head tag so that it starts loading before the page html is being displayed -->
	<link rel="stylesheet" href="style.css" type="text/css" />

</head>
<body>

<!-- webpage content goes here in the body -->

	<div id="page">
		<div id="logo">
			<h1><a href="/" id="logoLink">My First Website</a></h1>
		</div>
		<div id="nav">
			<ul>
				<li><a href="/home.php">Home</a></li>
				<li><a href="/register.php">Register</a></li>
				<li><a href="/login.php">Login</a></li>
			</ul>
		</div>
		<div id="content">
			<h2>Register</h2>
			<form method='POST' action=process_register.php>
			<table>

			<tr>
			<td><label>First Name:</label></td>
			<td><input type="text" name="fname"></td>
			</tr>

			<tr>
 			<td><label>Last Name:</label></td>
 			<td><input type="text" name="lname"></td>
 			</tr>

 			<tr>
  			<td><label>Username:</label></td>
  			<td><input type="text" name="user"></td>
  			</tr>

  			<tr>
  			<td><label>Password:</label></td>
  			<td><input type="password"  name="pass"></td>
  			</tr>
  			<tr>
 			 <td><input type="submit" id="submit" name="submit" value="sign up"></td>
 			 </tr>
 			 </table>
			</form>
		</div>
		<div id="footer">
			<p>
				Webpage made by <a href="/" target="_blank">[your name]</a>
			</p>
		</div>
	</div>
</body>
</html>
