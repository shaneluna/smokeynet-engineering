import pandas as pd
import numpy as np

import sklearn.linear_model as lin_model

from haversine import haversine, Unit, inverse_haversine

import sklearn.model_selection as model
import sklearn.preprocessing as preprop
from sklearn.metrics import r2_score
import joblib
from ast import literal_eval

df_cameras = pd.read_csv(f"../../../data/processed/camera_metadata_hpwren.csv")
df_cameras = df_cameras.dropna(subset=['x_resolution', 'y_resolution', 'center_angle'])

df_lm = pd.read_csv('../../../data/raw/landmarks_manual.csv')
df_lm = df_lm.rename(columns={'lat': 'lm_lat', 'long': 'lm_long'})

def find_angle(ax, ay, bx, by, cx, cy):
    a = np.array([ax, ay])
    b = np.array([bx, by])
    c = np.array([cx, cy])

    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return angle

df_merged = df_cameras.merge(df_lm, left_on=['camera_abbrev', 'direction'], right_on=['camera_abbrev', 'direction'], how='inner')
df_merged = df_merged[['camera_abbrev', 'direction', 'landmark', 'lat', 'long', 'center_lat', 'center_long', 'lm_lat', 'lm_long', 'x_pixel', 'y_pixel', 'x_res', 'y_res', 'elevation', 'distance', 'intersection', 'center_angle']]
df_merged['angle'] = df_merged.apply(lambda x: find_angle(x['center_long'], x['center_lat'], x['long'], x['lat'], x['lm_long'], x['lm_lat']), axis=1)

def find_x_ratio(pix, res):
    return abs(pix-(res/2))/(res/2)

def find_y_ratio(pix, res):
    return abs(res-pix)/(res)

df_merged['x_ratio'] = df_merged.apply(lambda x: find_x_ratio(x['x_pixel'], x['x_res']), axis=1)
df_merged['y_ratio'] = df_merged.apply(lambda x: find_y_ratio(x['y_pixel'], x['y_res']), axis=1)


X_test = df_merged[['x_ratio', 'y_ratio', 'elevation']].loc[df_merged['intersection'] == 1]
X_test['elevation'] = X_test['elevation'] - np.median(X_test['elevation'])
y_test = df_merged['angle'].loc[df_merged['intersection'] == 1]

X_train = df_merged[['x_ratio', 'y_ratio', 'elevation']].loc[df_merged['intersection'] == 0]
X_train['elevation'] = X_train['elevation'] - np.median(X_train['elevation'])
y_train = df_merged['angle'].loc[df_merged['intersection'] == 0]

#Scale Data
scaler = preprop.StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)

#Fit Model
model = lin_model.Ridge(alpha=11.5, max_iter=1000)#, selection='random')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("R2 Score: ", r2_score(y_test, y_pred))

joblib.dump(model, '../pickled_files/locating_angle_model.gz')
joblib.dump(scaler, '../pickled_files/locating_scaler.gz')
joblib.dump(df_merged, '../pickled_files/test_df.gz')