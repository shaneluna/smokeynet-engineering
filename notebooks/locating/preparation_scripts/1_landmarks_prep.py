import pandas as pd
from haversine import haversine, Unit
import cv2

lm_df = pd.read_csv("../../../data/raw/landmarks_manual.csv")
cam_meta = pd.read_csv("../../../data/processed/camera_metadata_hpwren.csv")

lm_df = lm_df.merge(cam_meta[['camera_abbrev', 'direction', 'lat', 'long']], left_on=['camera_abbrev', 'direction'], right_on=['camera_abbrev', 'direction'], how='left')
lm_df = lm_df.drop_duplicates().reset_index(drop=True)

lm_df['distance'] = lm_df.apply(lambda x: haversine((x['lat_x'], x['long_y']), (x['lat_y'], x['long_y'])), axis=1)
lm_df = lm_df.rename(columns={"lat_x":"lat", "long_x":"long"})
del lm_df['lat_y']
del lm_df['long_y']

def find_tile(x_pix, y_pix, x_tiles = 9, y_tiles = 5, img_size = (3072, 2048), dsize = (1856, 1392), cropped_size = (1856, 1040), tile_size = (224, 224), overlap = 20):
    x_ratio = img_size[0]/dsize[0]
    y_ratio = img_size[1]/dsize[1]
    step_x = (tile_size[0]/2) * x_ratio
    step_y = (tile_size[1]/2) * y_ratio
    y_start = img_size[1] - (img_size[1] * cropped_size[1]/dsize[1])

    x_centers = [step_x + i*(step_x*2 - overlap*x_ratio) for i in range(x_tiles)]
    y_centers = [step_y + y_start + i*(step_y*2 - overlap*y_ratio) for i in range(y_tiles)]
    
    x_scores = [abs(x_cent - x_pix) for x_cent in x_centers]
    y_scores = [abs(y_cent - y_pix) for y_cent in y_centers]
    
    return (y_scores.index(min(y_scores))*(x_tiles)) + (x_scores.index(min(x_scores)))

lm_df['tile'] = lm_df.apply(lambda x: find_tile(x['x_pixel'], x['y_pixel'], img_size = (x['x_res'], x['y_res'])), axis=1)

lm_df.to_csv("../../../data/raw/landmarks_manual.csv", index=False)