# Smoke Locating
## Introduction
#### Summary
The goal of this project is to estimate the location in decimal gps coordinates of smoke within an image within a 3-mile accuracy of its actual location.  This method uses a method called triangulation to perform the locating process, which relies on data from two cameras that have seen the smoke. The model was developed to work with the output of the SmokeyNet smoke detection model.  

The intent is that the model is run at the same rate as SmokeyNet (1min) and at every iteration is given a list of all of the cameras wihin the past X minutes that have seen smoke and the tiles that the smoke appeareded in, according to the tiling of the SmokeyNet image preprocessing.  The model will compare all of the cameras in the list where triangulation is generally feasible, given those camera's locations, and perform triangulation for those pairs.

This notebook uses landmarks instead of smoke as there did not exist a reliable dataset to use historical smoke as data to train and test the model. The assumption is that these landmarks whose pixel locations and gps coordinates can easily be determined can be used as placeholders for smoke that appears in images.

#### Process - High Level Diagram
![triangulation_hl_diagram](../../data/images/triangulation_high_level.png)

#### Process - Detailed
1. The model is provided a list of all of the cameras that have seen smoke within the past X minutes and the tiles the smoke appeared in.
2. The list of cameras is processed to determine which of the cameras in the list are within a close enough are where triangulation is feasibly possible.  This is done because if two cameras in the list are geographically very far apart, it can be assumed that those cameras are observing different fires thus triangulation should not be performed.  After this, camera pairs are formed for which triangulation will be performed.
3. Camera view objects are created for cameras that are within the resulting list.  These objects contain the information of the camera's view at that given time and leverages a regression model that maps the 2d image to a bird's eye view angle between the camera's centerline of view and the item of interest(smoke). 
>#### Regression Model Mapping
![regression_mapping](../../data/images/regression_model_mapping.png)

4. Triangulation is then performed between the camera view objects whose cameras were determined as pairs in step 2.  This creates linear equations for each camera from the angles determined in step 3, whose intersection is the gps coordinate estimate of the item of interest (smoke).  
>#### Triangulation Process
![triangulation_process](../../data/images/triangulation_process.png)

---
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
> Performs demo to visualize location estimation practice within map.  Loads *landmarks_manual.csv* dataset where landmarks whose intersections attribute it 1 can be used.
---

## Maintenance
#### Adding New Landmarks for Reference
There currently exists and landmark dataset, *landmarks_manual.csv* that contains 132 landmarks that were manually found through images from cameras on the HPWREN network.  If a new landmark is to be added to the dataset, the following should be documented per the columns outlined.
1. **landmark**
>descriptor of the landmark
2. **camera_abbrev**
>abbreviation of camera that see the landmark
3. **direction**
>direction that the camera is facing
4. **lat**
>latitude of landmark.  This has previosuly been found through clicking the landmark in Google Maps
5. **long**
>longitude of landmark.  This has previosuly been found through clicking the landmark in Google Maps
6. **x_pixel**
>x pixel coordinate of which the landmark generally appears
7. **y_pixel**
>y pixel coodinate of which the landmark generally appears.  This should be closer to the bottom or base of the landmark
8. **x_res**
> x resolution of the camera that sees the landmark.  This is not taken from the camera metadata and is intead documented here in case the camera is ever retrofitted with a new camera of different resolution
9. **y_res**
> y resolution of the camera that sees the landmark.  This is not taken from the camera metadata and is intead documented here in case the camera is ever retrofitted with a new camera of different resolution
10. **intersection**
> 1 if this landmark is also seen by another camera and 0 if it does not.  0 can also be used as the label if another camera also sees the landmark, but the landmark is not to be used for model testing.

The **distance** and **tile** columns are calculated after running the *1_landmarks_prep.ipynb* script.  Only the other parameters listed above need to be recorded manually.

---

## Future Work
Although this model has been able to perform within the initial criteria, there are some suggestion for future improvements
1. **Analyze Camera Coverage**
>Research areas with less camera coverage for potential installation of new cameras.  Installing more cameras in these locations will increase the geographical area in which triangulation can be performed
2. **Collect More Accurate Camera Metadata(Location, Direction, and Tilt)**
>The gps coordinates of each camera in the original dataset were not precise enough and should be measured in field.  The true direction of the camera should also be measured as well.  Although the cameras are labelled with the cardinal directions, each camera on the network does not face in true cardinal directions and are slightly angled.  This has been rougly factored in the camera_metadata_hpwren.csv dataset as center_angle, but has room of more accuracy with a physical measurement.  Lastly, the tilt of the cameras is a feature that is expected to have an effect on the regression model to determine angle, but it was not recorded for these cameras.  In the future if this feature is physically measured, it can be leveraged as an input to the model.  Collecting all of this metadata should result in higher accuracy of the locating model
3. **Gathering More Data Points for Testing**
>This model can be tested on more landmarks to determine accuracy.  So far, 10 landmarks were found where triangulation could be performed.  More of these landmarks that are seen my multiple cameras whose locations can be definitively identified can be added to better determine the robustness of the model
4. **Evaluate Model on Future Controlled Fire Events**
>Since this model has only been tested on landmarks, in the future it should be tested on controlled fire events to verify if it can be scaled.  The future fire events would need to be documented well enough in the same way the landmarks were in order to test this model effectively.
