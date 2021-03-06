# Data Catalog: /data/raw/

Some (but not all) data schemas have been provided below.

## camera_metadata_manual.csv

| Attribute      | Type | Description     |
| :---        | :----    | :---            |
| camera_id      | str       | Unique identifier for the camera consisting of station and direction. Originally comes from firemap pylaski api. For manual cameras added that do not exist in pylaski, "hpwren_missing#\_direction" was added. I.e. hpwren1_north, hpwren_missing1_north.   |
| image_id   | str        | Another form of camera identifer that is parsed from image urls, hence, calling it the image id. I.e. buff-n-mobo-c      |
| prev_image_ids   | str[]        | List of previous image ids or aliases that a camera has had.      |
| camera_name   | str        | Camera station name.      |
| direction   | str        | Direction of camera. North, east, south, west. All lowercase.      |
| gmap_lat   | float        | Corrected camera lat location with more precision determined via google maps.     |
| gmap_long   | float        | Corrected camera long location with more precision determined via google maps.      |
| elevation   | int        | Camera metadata. For manual inputs, taken from hpwren website for individual station (top of page, not lower section).      |
| x_resolution   | int        | Station camera image pixel size for x, taken by analyzing image/looking at image exif data.     |
| y_resolution   | int        | Station camera image pixel size for y, taken by analyzing image/looking at image exif data.      |
| center_lat   | float        | Lat of point along the camera field of view center line. Determined by looking at camera image, drawing vertical centerline at pixel center, and finding distinguishable landmark very close to centerline to take location of from google maps. Center point value used to calculate angle of camera away from its true_direction (north, east, south, west). I.e. Used to calculate correction to the direction documented.      |
| center_long   | float        | Long of point along the camera field of view center line. Determined by looking at camera image, drawing vertical centerline at pixel center, and finding distinguishable landmark very close to centerline to take location of from google maps. Center point value used to calculate angle of camera away from its true_direction (north, east, south, west). I.e. Used to calculate correction to the direction documented.       |

## camera_meatadata.csv
For HPWREN cameras, all columns after properties.description.latest-images also get stored in that same column--HPWREN camera json structured differently than Axis and doesn't parse properly by default.

| Attribute      | Type | Description     |
| :---        | :----    | :---            |
| type      | str       | Type of the return object. All are "Features."            |
| geometry.type      | str       | The geometry type of the object returned. All are "Points."            |
| geometry.coordinates      | float[]       | [long, lat, elevation]            |
| properties.description.name      | str       | Camera station name. I.e. Big Black Mountain            |
| properties.description.id      | str       | Camera id. I.e. hpwren1_north            |
| properties.description.url      | str       | URL for the camera description site. Site down for all HPWREN cameras.            |
| properties.description.latest-images      | str       | URL for viewing latest camera image.<br><br>**Note**: HPWREN data is structured differently than axis, asnd as a result this column doesn't parse properly with pd.json_normalize. All columns after are Axis related columns. HPWREN cameras have their own set of properties that are also stored within the latest-images attribute.            |
|       |        |           |
| COLUMNS BELOW ARE FOR AXIS ONLY AND WERE NOT FULLY ANALYZED AS RESULT      |        |           |
|       |        |           |
| properties.description.type      | na       |           |
| properties.description.ptz      | na       |             |
| properties.description.zoom_current      | na       |             |
| properties.description.attribution      | na       |             |
| properties.description.sponsor      | na       |             |
| properties.description.network      | na       |             |
| properties.description.isp      | na       |             |
| properties.description.fov_center      | na       |             |
| properties.description.last_movement_at      | na       |             |
| properties.description.fov_lft      | na       |             |
| properties.description.ProdNbr      | na       |             |
| properties.description.county      | na       |             |
| properties.description.is_patrol_mode      | na       |             |
| properties.description.lastupdate      | na       |             |
| properties.description.region      | na       |             |
| properties.description.fov      | na       |             |
| properties.description.activated_at      | na       |             |
| properties.description.is_currently_patrolling      | na       |             |
| properties.description.az_current      | na       |             |
| properties.description.state      | na       |             |
| properties.description.fov_rt      | na       |             |
| properties.description.tilt_current      | na       |             |

## landmarks_manual.csv

Manually found landmarks through images from cameras on the HPWREN network for testing locating approach. If a new landmark is to be added to the dataset, the following should be documented per the columns outlined.

| Attribute      | Type | Description     |
| :---        | :----    | :---            |
| landmark      | str       | Descriptive name of the landmark.            |
| camera_abbrev      | str       |  Official abbreviation of camera that sees the landmark.            |
| direction      | str       | Direction that the camera is facing.            |
| lat      | float       | Latitude coordinate of landmark. This has previosuly been found through clicking the landmark in Google Maps            |
| long      | float       | Longitude coordinate of landmark. This has previosuly been found through clicking the landmark in Google Maps            |
| x_pixel      | int       | X pixel coordinate of which the landmark generally appears in camera image.           |
| y_pixel      | int       | Y pixel coodinate of which the landmark generally appears in the camera. This should be closer to the bottom or base of the landmark.            |
| x_res      | int       | X resolution of the camera that sees the landmark. This is not taken from the camera metadata and is intead documented here in case the camera is ever retrofitted with a new camera of different resolution            |
| y_res      | int       | Y resolution of the camera that sees the landmark. This is not taken from the camera metadata and is intead documented here in case the camera is ever retrofitted with a new camera of different resolution            |
| intersection      | str       | 1 if this landmark is also seen by another camera and 0 if it does not. 0 can also be used as the label if another camera also sees the landmark, but the landmark is not to be used for model testing.            |

## smokeynet_test.json<br>smokeynet_train.json<br>smokeynet_valid.json

Smokeynet files are in json where each object represents 1 image prediction set.<br>
The attributes for each one of these objects are below:

| Attribute      | Type | Description     |
| :---        | :----    | :---            |
| camera_name      | str       | Full FIgLib fire event name (folder name) that the image came from. Follows **YearMonthDay\_\<Fire\_Name\>\_\<Camera_Name\>** where "camera_name" is also known as the "image_id" used in image url. I.e. buff-n-mobo-c.            |
| image_gt      | int       | Actual groundtruth smoke value. 1 for yes smoke, 0 for no smoke.            |
| tile_gt      | int[]       | Int list of groundtruth values for each tile of an image. As of now ALL will be empty list because not bounding box/contour mask labels were provided; only whole image labels. Placeholder for when additional labeling gets done.            |
| image_pred      | int       | Image prediction smoke value. 1 for yes smoke, 0 for no smoke.            |
| tile_pred      | int[]       | Int list of prediction values for each tile of an image. Currently, 45 tiles per image. 0 is top left tile of image. Goes left to right in row. Restarts left to right at each row.          |

## station_metadata.csv

Wide table. Not all attributes are included below, but only ones identified as most relevant to the analysis done.

| Attribute      | Type | Description     |
| :---        | :----    | :---            |
| MNET_SHORTNAME      | str       | Shortname of the network the station belongs to. I.e. HPWREN.            |
| TIMEZONE      | str       | The timezone that the station is located in.            |
| SHORTNAME      | str       | Shortname of the network the station belongs to. I.e. HPWREN.            |
| STID      | str       | Station ID. Unique identifier for station. TBD if fully unique across all networks. Was unique across SDGE, HPWREN, and SC-EDISON.            |
| MNET_LONGNAME      | str       | Full name of the network the station belongs to.            |
| STATUS      | str       | Current active status of the station.            |
| LONGITUDE      | float       | Longitude location of station.            |
| LATITUDE      | float       | Latitude location of station.            |
| COUNTY      | str       | County that the station resides in.            |
| STATE      | str       | State that the station resides in.            |
| MNET_ID      | int       | Int id of the network the station belongs to.            |
| NAME      | str       | The name of the station.            |
| PERIOD_OF_RECORD.start      | datetime       | The earliest datatime of records. I.e. install datetime.            |
| PERIOD_OF_RECORD.end      | datetime       | The latest datetime of records. If active today, should show todays date, but time may vary.            |

## weather_HPWREN.csv<br>weather_SC-EDISON.csv<br>weather_SDGE.csv

Only cols identified as most relevant to the analysis are included below.

**Note**: When querying stations, the data format returned may vary depending on the type of sensors available.

| Attribute      | Type | Description     |
| :---        | :----    | :---            |
| Station_ID      | str       | Weather station abbreviation name and id.            |
| Date_Time      | datetime as str       | The timestamp of the readings in UTC.            |
| air_temp_set_1      | float       | Air temperature value in celsius.            |
| relative_humidity_set_1      | float       | Relative humidity value in %.              |
| wind_speed_set_1      | float       | Wind speed value in m/s.            |
| wind_gust_set_1      | float       | Wind gust value in m/s.            |
| wind_direction_set_1      | float       | Wind meteorological direction value in degrees.             |
| dew_point_temperature_set_1d      | float       | Dew point temperature in Celsius.             |