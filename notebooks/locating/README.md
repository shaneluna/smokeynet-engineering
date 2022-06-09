## Python Notebooks
#### Preparation Notebooks
- **1_angle_model_train.ipynb** - Angle Regression Model Training
> Script to train model on landmark data and camera metadata using Ridge regression. Purpose of model is to understand relationship between pixel location + camera elevation and angle between camera centerline and smoke in image. Pickles model and scaler into files locating_angle_mode.gzip and locating_scaler.gzip.  Should be run whenever a new landmark is added to landmarks_manual.csv or an existing camera's metadata changes.

- **1_landmarks_prep.ipynb** - Process Landmarks Dataset for Testing
> Find distances between landmarks in landmarks_manual.csv and the cameras that saw them.  Also labels each with what pixel those landmarks would appear in within the preprocessed image fed into SmokeyNet.  Purpose is to prepare data to be used for testing as tiles are used as inputs for location_estimator, not pixel coordinates.  Should be run whenever a new landmark is added to landmarks_manual.csv or an existing camera's metadata changes.

#### Application Notebooks
- **2_location_estimator.ipynb** - Location Estimator/Triangulation Notebook
> Loads pickled model and scaler from angle_model_train.ipynb.  Contains a class that creates a camera_view object and triangulation function.  The camera_view object represent what the camera sees and the line of sight with the smoke or landmark of interest.  The triangulation function should be passed a list of tuples which each contain (camera_abbrev, direction, tile_num) ideally all of which have seen the smoke within a short time period of each other.  The triangulation function will see how many of these camera's view intersect with each other and perform triangulation on those pairs.
- **2_test_locating_model.ipynb** - Model Testing Notebook
> Runs 2_location_estimator.ipynb to load camera_view class and triangulation function and performs test using landmarks in landmarks_manual.csv dataset where intersection column = 1.
- **3_locating_demo.ipynb** - Locating Demo
> Performs demo to visualizae location estimation practice within map.  Loads
