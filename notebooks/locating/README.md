## Python Notebooks
#### Preparation Notebooks
- 1_angle_mode_train.pynb
> Script to train model.  Pickles model and scaler into files locating_angle_mode.gzip and locating_scaler.gzip

#### Application Notebooks
- 2_location_estimator.ipynb
> Contains a class that creates a camera_view object and triangulation function.  This object represent what the camera sees and the line of sight with the smoke or landmark of interest.  The triangulation function should be passed a list of tuples which each contain (camera_abbrev, direction, tile_num) ideally all of which have seen the smoke within a short time period of each other.  The triangulation function will see how many of these camera's view intersect with each other and perform triangulation on those pairs.
- 2_test_model

angle_model_train.ipynb - Script to train model.  Pickles model and scaler into files locating_angle_mode.gzip and locating_scaler.gzip
location_estimator - Model to perform estimation smoke location