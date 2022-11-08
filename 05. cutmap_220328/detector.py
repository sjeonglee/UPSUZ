# import libraries
import geopandas as gpd
from tqdm import tqdm
import json

class Detector:
    # constructor
    def __init__(self, color_dir):
        self.color_dir = color_dir                                  # color dictionary directory
        with open(self.color_dir, 'r', encoding='utf-8') as f:      # load color dictionary
            self.color_dict = json.load(f)
        self.outliers = dict()                                      # detected outliers
                                                                    # (key(outlier): value(shapefile that contains the outlier))
                                                                   
    def check_outliers(self, shp_dir: str): # 튀는 용도지역이 있는지 체크
        shp = gpd.read_file(shp_dir, encoding = 'cp949')
        shp_yongdo = shp['A14'].unique()
        out = []
        for yongdo in shp_yongdo:
            if yongdo in self.color_dict:
                continue
            else:
                out.append(yongdo)
    
        # if any outlier is detected
        if out:
            for o in out:
                if o in self.outliers:
                    self.outliers[o].append(shp_dir)
                else:
                    self.outliers[o] = [shp_dir]
    
    def check_outliers_from_list(self, shp_list: list):   # 튀는 용도지역을 체크할 shapefile들의 list가 있을 경우
        for shp in tqdm(shp_list):
            self.check_outliers(shp)