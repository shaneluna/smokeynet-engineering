# Data Catalog: /data/raw/


## camera_metadata_manual

| Column      | Type | Description     |
| :---        | :----    | :---            |
| camera_id      | str       | Unique identifier for the camera consisting of station and direction. Originally comes from firemap pylaski api. For manual cameras added that do not exist in pylaski, "hpwren_missing#\_direction" was added. I.e. hpwren1_north, hpwren_missing1_north.   |
| image_id   | str        | Another form of camera identifer that is parsed from image urls, hence, calling it the image id. I.e. buff-n-mobo-c      |
| camera_name   | str        | Camera station name.      |
| direction   | str        | Direction of camera. North, east, south, west. All lowercase.      |
| gmap_lat   | float        | Corrected camera lat location with more precision determined via google maps.     |
| gmap_long   | float        | Corrected camera long location with more precision determined via google maps.      |
| elevation   | int        | Camera metadata. For manual inputs, taken from hpwren website for individual station (top of page, not lower section).      |
| x_resolution   | int        | Station camera image pixel size for x, taken by analyzing image/looking at image exif data.     |
| y_resolution   | int        | Station camera image pixel size for y, taken by analyzing image/looking at image exif data.      |
| center_lat   | float        | Lat of point along the camera field of view center line. Determined by looking at camera image, drawing vertical centerline at pixel center, and finding distinguishable landmark very close to centerline to take location of from google maps. Center point value used to calculate angle of camera away from its true_direction (north, east, south, west). I.e. Used to calculate correction to the direction documented.      |
| center_long   | float        | Long of point along the camera field of view center line. Determined by looking at camera image, drawing vertical centerline at pixel center, and finding distinguishable landmark very close to centerline to take location of from google maps. Center point value used to calculate angle of camera away from its true_direction (north, east, south, west). I.e. Used to calculate correction to the direction documented.       |