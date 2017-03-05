<?php include $argv[1];?>

<?php
$user = $_POST['user'];
$pass = $_POST['pass'];

$servername = "localhost";
$username = "root";
$password = "";
$db = "assignment1";

$logged_in = False;

// Create connection
$conn = mysqli_connect($servername, $username, $password , $db);
$sql="select * from user where username='".$user."' and password='".$pass."'";
;

$res=mysqli_query( $conn , $sql);

if ($res ->num_rows >0)
{
	$logged_in=True;
	$uid = $res->fetch_row()[0];
	echo $uid;
	echo "<br>";
	echo $PHPESSID;
	$add_new_session="update user set session=".$PHPESSID." where id=".$uid;
	mysqli_query( $conn , $add_new_session);
}

?>


<?php
if ($logged_in==True)
{
	echo "Welcome";
}


?>
