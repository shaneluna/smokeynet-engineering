import joblib
import numpy as np
import pandas as pd

from haversine import haversine, Unit, inverse_haversine
from shapely.geometry import Point, LineString
from ast import literal_eval

loc_est = __import__("2_location_estimator")

df = pd.read_csv("../../../data/raw/landmarks_manual.csv")
df_intersections = df.loc[df['intersection'] == 1].reset_index(drop=True)
test_lms = set(df_intersections['landmark'])

acc_list = []
for lm in test_lms:
    data1 = df_intersections.loc[df_intersections['landmark'] == lm].iloc[0]
    data2 = df_intersections.loc[df_intersections['landmark'] == lm].iloc[1]
    
    cam_input = [(data1['camera_abbrev'], data1['direction'], data1['tile']), (data2['camera_abbrev'], data2['direction'], data2['tile'])]
    
    tri_pairs = loc_est.triangulation(cam_input)
    dist_acc = haversine((data1['long'], data1['lat']), (tri_pairs[0]['estimate'][0], tri_pairs[0]['estimate'][1]), unit=Unit.MILES)
    acc_list.append(dist_acc)
    
    print("Test Point: ",lm)
    print("X: {:2f}, Y: {:2f}".format(tri_pairs[0]['estimate'][0], tri_pairs[0]['estimate'][1]))
    #print("X: {}, Y: {}".format(x_coord, y_coord))
    print("Estimate Distance From Actual: {:2f}mi".format(dist_acc))
    print("\n")


results_df = pd.DataFrame()
results_df['samples'] = [len(acc_list)]
results_df['mean'] = [np.mean(acc_list)]
results_df['median'] = [np.median(acc_list)]
results_df['max'] = [np.max(acc_list)]
results_df['min'] = [np.min(acc_list)]
results_df['% < 3mi'] = [(len([x for x in acc_list if x < 3])/len(acc_list)) * 100]
print(results_df)