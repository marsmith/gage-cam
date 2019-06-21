
<!doctype html>
<html>
    <head>
		<!-- <link href='https://cdnjs.cloudflare.com/ajax/libs/simplelightbox/1.17.1/simplelightbox.min.css' rel='stylesheet'>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/simplelightbox/1.17.1/simple-lightbox.min.js"></script>
        
        <style>
		.container .gallery a img {
		  float: left;
		  width: 20%;
		  height: auto;
		  border: 2px solid #fff;
		  -webkit-transition: -webkit-transform .15s ease;
		  -moz-transition: -moz-transform .15s ease;
		  -o-transition: -o-transform .15s ease;
		  -ms-transition: -ms-transform .15s ease;
		  transition: transform .15s ease;
		  position: relative;
		}

		.container .gallery a:hover img {
		  -webkit-transform: scale(1.05);
		  -moz-transform: scale(1.05);
		  -o-transform: scale(1.05);
		  -ms-transform: scale(1.05);
		  transform: scale(1.05);
		  z-index: 5;
		}

		.clear {
		  clear: both;
		  float: none;
		  width: 100%;
		}
		
		</style> -->
    </head>
    <body>
        <div class='container'>
            <div class="gallery">

            <?php
							// $server = $_SERVER['SERVER_NAME'];
							// if (strpos($server,'staging') !== false) {
							// $dbh = new PDO('sqlite:/afs/.usgs.gov/www/staging-ny.water/htdocs/maps/gage-cam/gage-cam.db');
							// } else {
							// $dbh = new PDO('sqlite:/afs/.usgs.gov/www/ny.water/htdocs/maps/gage-cam/gage-cam.db');
							// }

							// $sql = "SELECT * FROM images";
							// $query = $dbh->query($sql);

							// foreach ($query as $image) {
							// 		//echo '<img src="img.php?name='.$image['image_name'].'" /><br>';
							// 		echo ' <a href="img.php?name='.$image['image_name'].'"><img src="img.php?name='.$image['image_name'].'" alt="" title=""/>
							// 		</a>';
							// }

							

							$files = glob("uploads/*.jpg");

							for ($i=0; $i<count($files); $i++) {
									$image = $files[$i];
									print $image ."<br />";
									echo '<img src="'.$image .'" alt="Random image" />'."<br /><br />";
							}


            ?>

			</div>
        </div>

        
        <!-- Script -->
        <!-- <script type='text/javascript'>
        $(document).ready(function(){

            // Intialize gallery
            var $gallery = $('.gallery a').simpleLightbox();
        });
        </script> -->
    </body>
</html>