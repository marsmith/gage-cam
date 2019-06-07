<html>
	<body>
		<form action="" method="POST" enctype="multipart/form-data">
			Select image to upload:<br>
			<input type="file" name="fileToUpload"/><br>
			Site ID:<br>
			<input type="text" name="site_id"/><br>
			Date:<br>
			<input type="text" name="date_time"/><br>
			Water Level:<br>
			<input type="text" name="water_level"/><br>
			<br>
			<input type="submit"/>
		</form>

	</body>
</html>

<?php
$uploadOk = 1;
if(isset($_FILES['fileToUpload'])){
	// Check if image file is a actual image or fake image
	if(isset($_POST["submit"])) {
		$check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
		if($check !== false) {
			echo "File is an image - " . $check["mime"] . ".";
			$uploadOk = 1;
		} else {
			echo "File is not an image.";
			$uploadOk = 0;
		}
	}
	// Check file size
	if ($_FILES["fileToUpload"]["size"] > 1000000) {
		echo "Sorry, your file is too large.";
		$uploadOk = 0;
	}
	// Allow certain file formats
	$filename = $_FILES['fileToUpload']['name'];
	$imageFileType = strtolower(pathinfo($filename,PATHINFO_EXTENSION));
	if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
	&& $imageFileType != "gif" ) {
		echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
		$uploadOk = 0;
	}
	// Check if $uploadOk is set to 0 by an error
	if ($uploadOk == 0) {
		echo "Sorry, your file was not uploaded.";
	// if everything is ok, try to upload file
	} else {

		try {
		  $server = $_SERVER['SERVER_NAME'];
		  if (strpos($server,'staging') !== false) {
			$dbh = new PDO('sqlite:/afs/.usgs.gov/www/staging-ny.water/htdocs/maps/gage-cam/gage-cam.db');
		  } else {
			$dbh = new PDO('sqlite:/afs/.usgs.gov/www/ny.water/htdocs/maps/gage-cam/gage-cam.db');
		  }


			$dbh->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );//Error Handling


			// create our table, if it doesn't exist yet
			$dbh->exec("CREATE TABLE IF NOT EXISTS images (site_id VARCHAR(20), date_time VARCHAR(255) NOT NULL, water_level DOUBLE, image_bin LONGBLOB, image_name VARCHAR(255), remote_ip VARCHAR(45));");
		
			// Initialize variables
			// $site_id = 'martyOffice';
			$site_id = $_REQUEST['site_id'];

			// $date = new DateTime();
			// $date = $date->format('Y-m-d H:i:s');    // MySQL datetime format
			$date_time = $_REQUEST['date_time'];

			//$water_level = null;
			$water_level = $_REQUEST['water_level'];

			$image = file_get_contents($_FILES["fileToUpload"]["tmp_name"]);
			$image_name = addslashes($filename);

			//log IP address
			if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
				$ip = $_SERVER['HTTP_CLIENT_IP'];
			} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
					$ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
			} else {
					$ip = $_SERVER['REMOTE_ADDR'];
			}

			$query = $dbh->prepare("INSERT INTO images (site_id, date_time, water_level, image_bin, image_name, remote_ip) VALUES (?,?,?,?,?,?)");
			$query->bindParam(1, $site_id);
			$query->bindParam(2, $date_time);
			$query->bindParam(3, $water_level);
			$query->bindParam(4, $image);
			$query->bindParam(5, $image_name);
			$query->bindParam(6, $ip);

			$query->execute();
	
			echo "<p>The file ". basename($image_name). " has been uploaded succesfully:</p>";

			echo '<img width="300" src="./img.php?name='.$image_name.'"><br>';

		} 
			catch (PDOException $e) {
				print "Error!: " . $e->getMessage() . "
			";
				die();
		}
	}	
}

?>