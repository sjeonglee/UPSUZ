# Setting Libraries

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import os

class Cutter:
    def __init__(self, save_dir:str):
        self.save_dir = save_dir
    
    def get_mold(self, point:list):   #[x, y]
        half_length = self.side_length / 2
        
        print("Getting a mold")
        middlex = point[0]
        middley = point[1]

        point1 = Point(middlex - half_length, middley - half_length)
        point2 = Point(middlex + half_length, middley - half_length)
        point3 = Point(middlex + half_length, middley + half_length)
        point4 = Point(middlex - half_length, middley + half_length)

        poly = Polygon([point1, point2, point3, point4])
        mpoly = gpd.GeoSeries(poly, crs="EPSG:5174")
        return mpoly

    
    def clip_and_save(self, gdf:gpd.GeoDataFrame, mold:gpd.GeoSeries, filename:str):        # save the cutted shapefile to picture
        # clip
        clipped = gpd.clip(gdf, mold)
        
        plt.figure(figsize = (20, 20), dpi=200)
        # plt.rcParams['font.family'] = 'Malgun Gothic'
        sample_dis = clipped[['geometry', 'A14', 'use']]
        dis = sample_dis.dissolve(by='use')
        dis.reset_index(inplace=True)
        ax = plt.subplot(1, 1, 1)
        ax.axis('off')
        plt.margins(0,0)
        dis.plot(column = 'A14', legend = True, color=dis['use'], axes=ax)
        plt.savefig(filename, bbox_inches = 'tight', pad_inches = 0)
    
    def cookie_baking(self, point:list, gdf:gpd.GeoDataFrame, city:str, i:int):
        try:
            mold = self.get_mold(point)
        except:
            print("Error occurred while clipping the mold.")
        
        path = self.save_dir + "/" + city
        # Check whether the specified path exists or not
        if not os.path.exists(path):
            # Create a new directory because it does not exist 
            os.makedirs(path)
            print("The new directory " + city + " is created!")
        
        filename = path + "_" + str(i) + '.png'
        try:
            self.clip_and_save(gdf, mold, filename)
        except:
            print("Error occurred while saving mold " + str(i) + "in the city " + city)
            
    # def __init__(self, save_dir):
    #     self.save_dir = save_dir
    
    # def cut_map(self, gdf:gpd.GeoDataFrame, molds:list, city:str):   # 쿠키틀로 자르기
    #     def get_clipped(mold:gpd.GeoSeries):                                   # 자르기 함수
    #         clipped = gpd.clip(gdf, mold)
    #         return clipped
        
    #     def save_to_pic(gdf:gpd.GeoDataFrame, filename:str):        # save the cutted shapefile to picture
    #         plt.figure(figsize = (20, 20), dpi=200)
    #         # plt.rcParams['font.family'] = 'Malgun Gothic'
    #         sample_dis = gdf[['geometry', 'A14', 'use']]
    #         dis = sample_dis.dissolve(by='use')
    #         dis.reset_index(inplace=True)
    #         ax = plt.subplot(1, 1, 1)
    #         ax.axis('off')
    #         plt.margins(0,0)
    #         dis.plot(column = 'A14', legend = True, color=dis['use'], axes=ax)
    #         plt.savefig(filename, bbox_inches = 'tight', pad_inches = 0)
            
    #     path = self.save_dir + "/" + city
    #     # Check whether the specified path exists or not
    #     if not os.path.exists(path):
    #         # Create a new directory because it does not exist 
    #         os.makedirs(path)
    #         print("The new directory " + city + " is created!")
    
    #     for i in tqdm(range(len(molds))):
    #         try:
    #             c = get_clipped(molds[i])
    #         except:
    #             print("Error occurred while clipping the mold.")
    #             continue

    #         filename = path + "/" + city + "_" + str(i) + '.png'
    #         try:
    #             save_to_pic(c, filename)
    #         except:
    #             print("Error occurred while saving mold " + str(i) + "in the city " + city)
    #             continue
    
