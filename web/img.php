<?php
  $server = $_SERVER['SERVER_NAME'];
  if (strpos($server,'staging') !== false) {
	$dbh = new PDO('sqlite:/afs/.usgs.gov/www/staging-ny.water/htdocs/maps/gage-cam/gage-cam.db');
  } else {
	$dbh = new PDO('sqlite:/afs/.usgs.gov/www/ny.water/htdocs/maps/gage-cam/gage-cam.db');
  }

  if(isset($_GET['name'])) {
    $query = $_GET['name'];

    //if all return array of all images, otherwise just show image
    if ($query == 'all') {
      $sql = "SELECT * FROM images";
      $query = $dbh->query($sql);

      foreach ($query as $image) {
        echo ' <a href="./img.php?name='.$image['image_name'].'"><img src="./img.php?name='.$image['image_name'].'" alt="" title=""/>
        </a>';
      }
  
    }
  
    else {
      $sql = "SELECT * FROM images WHERE image_name = '".$query. "'";
      $query = $dbh->query($sql);
      $result = $query->fetch(PDO::FETCH_ASSOC);
      header("Content-Type: image/png");
      echo $result['image_bin'];
    }
  }




?>