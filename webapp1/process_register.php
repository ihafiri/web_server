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
<?php
$servername = "localhost";
$username = "root";
$password = "";
$db = "assignment1";

// Create connection
$conn = mysqli_connect($servername, $username, $password , $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$fname =$_POST['fname'];
$lname =  $_POST['lname'];
$email= $_POST['email'];
$user= $_POST['user'];
$pass= $_POST['pass'];

$sql = "insert into user(firstName,lastName,username,password) values('".$fname."','".$lname."','".$user."','".$pass."')";
$res=mysqli_query( $conn , $sql);
if($res)
{
	$msg="<h1>Congratulations! your account is ready</h1>";
}
else
{
	$msg="<h1>Oops! Something went wrong!";
}
echo $msg;

?>
		</div>
		<div id="footer">
			<p>
				Webpage made by <a href="/" target="_blank">[your name]</a>
			</p>
		</div>
	</div>
</body>
</html>




