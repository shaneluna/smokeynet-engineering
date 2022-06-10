import numpy as np
import pandas as pd

from haversine import haversine, Unit, inverse_haversine
from shapely.geometry import Point, LineString
import joblib


cam_meta = pd.read_csv("../../../data/processed/camera_metadata_hpwren.csv")
model = joblib.load('../pickled_files/locating_angle_model.gz')
scaler = joblib.load('../pickled_files/locating_scaler.gz')

class camera_view:
    def __init__(self, camera_abbrev, direction, tile_num, processed_xres=1856, processed_yres = 1040, precrop_yres = 1392, overlap_size=20, tile_size = [224,224]):
        self.camera_abbrev = camera_abbrev
        self.direction = direction
        self.tile_num = tile_num
        self.processed_xres = processed_xres
        self.processed_yres = processed_yres
        self.precrop_yres = precrop_yres
        self.overlap_size = overlap_size
        self.tile_size = tile_size
        self.full_xres = cam_meta['x_resolution'].loc[(cam_meta['camera_abbrev'] == camera_abbrev) & (cam_meta['direction'] == direction)].iloc[0]#get from metadata
        self.full_yres = cam_meta['y_resolution'].loc[(cam_meta['camera_abbrev'] == camera_abbrev) & (cam_meta['direction'] == direction)].iloc[0]#get from metadata
        self.elevation = cam_meta['elevation'].loc[(cam_meta['camera_abbrev'] == camera_abbrev) & (cam_meta['direction'] == direction)].iloc[0]
        self.cl_angle = cam_meta['center_angle'].loc[(cam_meta['camera_abbrev'] == camera_abbrev) & (cam_meta['direction'] == direction)].iloc[0]
        self.cam_lat = cam_meta['lat'].loc[(cam_meta['camera_abbrev'] == camera_abbrev) & (cam_meta['direction'] == direction)].iloc[0]
        self.cam_long = cam_meta['long'].loc[(cam_meta['camera_abbrev'] == camera_abbrev) & (cam_meta['direction'] == direction)].iloc[0]
        self.pix_centers = self.find_tile_centers()
        self.angle = self.find_angle()
        self.converted_angle = self.convert_angle()
        self.slope = self.find_slope()
        self.y_int = self.cam_lat - (self.slope * self.cam_long)
                
    def find_tile_centers(self):
        num_tiles_x = int((self.processed_xres - self.overlap_size)/(self.tile_size[0] - self.overlap_size))
        num_tiles_y = int((self.processed_yres - self.overlap_size)/(self.tile_size[0] - self.overlap_size))
        full_y_crop = (self.precrop_yres / self.processed_yres)
        xres_ratio = self.full_xres/self.processed_xres
        yres_ratio = (self.full_yres*(self.processed_yres/self.precrop_yres))/self.processed_yres
        stepsize_x = (self.tile_size[0]*xres_ratio) - (self.overlap_size * xres_ratio)
        stepsize_y = (self.tile_size[1]*yres_ratio) - (self.overlap_size * yres_ratio)
        x_pix = [round(((self.tile_size[0]*xres_ratio)/2) + (i*stepsize_x)) for i in range(num_tiles_x)]
        y_pix = [round(((self.tile_size[1]*yres_ratio)/2) + (i*stepsize_y) + (((self.precrop_yres-self.processed_yres) / self.precrop_yres)*self.full_yres)) for i in range(num_tiles_y)]
        
        return [[x_pix[j],y_pix[i]] for i in range(len(y_pix)) for j in range(len(x_pix))]
    
    def find_angle(self):
        x_ratio = abs(self.pix_centers[self.tile_num][0]-(self.full_xres/2)) / (self.full_xres/2)
        y_ratio = abs(self.pix_centers[self.tile_num][1] -self.full_yres)/ self.full_yres
        ang1 = model.predict(scaler.transform([[x_ratio, y_ratio, self.elevation]]))
        return ang1
    
    def convert_angle(self):
        dir_dict = {'north': np.pi/2, 'west': np.pi, 'south': 3*np.pi/2, 'east': 0}
        if (self.pix_centers[self.tile_num][0]) <= (self.full_xres/2):
            return  self.cl_angle + dir_dict[self.direction] + self.angle
        else:
            return  self.cl_angle + dir_dict[self.direction] - self.angle
        
    def single_camera(self):
        cam_coord = (self.cam_lat, self.cam_long)
        cam_end = inverse_haversine(cam_coord, 30, self.angle)
        left_start = inverse_haversine(cam_coord, 3, self.angle+(np.pi/2))
        left_end = inverse_haversine(left_start, 30, self.angle)
        right_start = inverse_haversine(cam_coord, 3, self.angle-(np.pi/2))
        right_end = inverse_haversine(right_start, 30, self.angle)

        line_left = LineString([cam_coord, cam_end])
        line_center = LineString([left_start, left_end])
        line_right = LineString([right_start, right_end])

        return gpd.GeoDataFrame([line_left, line_center, line_right],  columns=['LineString_obj'],  geometry='LineString_obj')
    
    def find_slope(self):
        if self.direction == 'north':
            if self.pix_centers[self.tile_num][0] < (self.full_xres/2):
                return np.tan((np.pi/2)+self.angle+self.cl_angle)
            else:
                return np.tan((np.pi/2)-self.angle+self.cl_angle)
        if self.direction == 'east':
            if self.pix_centers[self.tile_num][0] < (self.full_xres/2):
                return np.tan(self.angle+self.cl_angle)
            else:
                return np.tan(-self.angle+self.cl_angle)
        if self.direction == 'south':
            if self.pix_centers[self.tile_num][0] < (self.full_xres/2):
                return np.tan((3*np.pi/2)+self.angle+self.cl_angle)
            else:
                return np.tan((3*np.pi/2)-self.angle+self.cl_angle)
        if self.direction == 'west':
            if self.pix_centers[self.tile_num][0] < (self.full_xres/2):
                return np.tan(np.pi+self.angle+self.cl_angle)
            else:
                return np.tan(np.pi-self.angle+self.cl_angle)


def triangulation(cam_list):
    #create list of camera_view objects
    cv_list = []
    for cam in cam_list:
        cv_list.append(camera_view(camera_abbrev=cam[0], direction=cam[1], tile_num=cam[2]))
    df_filt = cam_meta[cam_meta[['camera_abbrev', 'direction']].apply(tuple, axis=1).isin([(cv.camera_abbrev, cv.direction) for cv in cv_list])]
    pairs = []
    for i, base_cv in enumerate(cv_list):
        for cv in cv_list:
            if base_cv != cv:
                compare_cam = str((cv.camera_abbrev, cv.direction))
                if (compare_cam in df_filt['intersections'].iloc[0]) | (cv.camera_abbrev == base_cv.camera_abbrev):
                    pairs.append({base_cv, cv})
    triangulation_pairs = [i for n, i in enumerate(pairs) if i not in pairs[:n]]
    out_pairs = []
    for pair in triangulation_pairs:
        lpair = list(pair)
        lc1= lpair[0]
        lc2 = lpair[1]

        x_coord = ((lc2.y_int - lc1.y_int)/(lc1.slope-lc2.slope))[0]
        y_coord = ((lc1.slope * x_coord) + lc1.y_int)[0]
        out_pairs.append({'cam1': lc1.camera_abbrev, 'cam2': lc2.camera_abbrev, 'estimate': (x_coord, y_coord)})
        #print("Fire Estimate between {} and {} camera_abbrevs: {}".format(lc1.camera_abbrev, lc2.camera_abbrev, (x_coord[0], y_coord[0])))

    return(out_pairs)


