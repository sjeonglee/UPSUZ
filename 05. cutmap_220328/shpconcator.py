# Setting Libraries

import pandas as pd
import geopandas as gpd
import glob
import ast
import json
import os

class ShpConcator:
    def __init__(self, data_dir, color_dir):
        self.data_dir = data_dir
        self.color_dir = color_dir                                  # color dictionary directory
        with open(self.color_dir, 'r', encoding='utf-8') as f:      # load color dictionary
            self.color_dict = json.load(f)
    
    def make_dir(self, city, concat_or_color, save_dir):
        directory = save_dir + concat_or_color + city
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_shp(self, city, save_dir):                               # city: load, concat and color shapefile
        def concat_shp()->gpd.GeoDataFrame:                          # shapefile 합치기
            file_directory = glob.glob(self.data_dir + "/" + city + "/*")
            shps = [file for file in file_directory if file.endswith(".shp")]
            result_gdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(i, encoding = 'cp949') for i in shps], 
                                ignore_index=True), crs="EPSG:5174")
            self.make_dir(city, "/concat/", save_dir)
            result_gdf.to_file(save_dir + "/concat/" + city + "/" + city + "_concat.shp")
            print("The city " + city + " is concatenated.")
            return result_gdf
        
        def get_gdf_color(gdf:gpd.GeoDataFrame):                              # 각종 용도지역과 도로 구분해서 색칠
            def get_color(row):                                               # 도로를 검은색으로 색칠
                # check if 'A11' is '도로'
                isdoro = row['A11']
                if isdoro == '도로':
                    return '#000000'
                
                # check if 'A14' is None (용도지역)
                name = row['A14']
                if name == 'None':
                    name = ast.literal_eval(name)
                if name in self.color_dict:
                    return self.color_dict[name]

            # get color based on yongdo
            gdf['use'] = gdf.apply(get_color, axis=1)
            self.make_dir(city, "/color/", save_dir)
            gdf.to_file(save_dir + "/color/" + city + "/" + city + "_colored.shp")
            print("The city " + city + " is colored.")
        
        try:
            gdf = concat_shp()
        except:
            print("Error occurred while concatenating the shapefiles of " + city)
            return
        
        try:
            get_gdf_color(gdf)
        except:
            print("Error occurred while coloring the shapefiles of " + city)
            return