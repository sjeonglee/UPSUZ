# Setting Libraries
import os
import geopandas as gpd
from shapely.geometry import Point, Polygon
from tqdm import tqdm
import geopandas as gpd
import matplotlib.pyplot as plt

class Molder:
    def __init__(self, interval:int, side_length:int, save_dir:str):        # interval(각 블럭 간 건너뛰기), side_length(The width of the generated image)
        self.interval = interval
        self.side_length = side_length
        self.save_dir = save_dir

    def is_in(self, polygon:gpd.GeoSeries, point:list):
        p = Point(point[0], point[1])
        if_contains = polygon.contains(p, align=False)
        return if_contains.any()

    def get(self, gdf:gpd.GeoDataFrame, city:str):        
        # def is_in(polygon:gpd.GeoSeries, point:list):
        #     p = Point(point[0], point[1])
        #     if_contains = polygon.contains(p, align=False)
        #     return if_contains.any()
        

        bounds = gdf.total_bounds
        i = 0   # 여기 바꾸는거 잊지말것!!!!!!!!!!!!!!!!!!!!!!!!!!
     
        print("Get the middle points of the boundary")
        for x in tqdm(range(int(bounds[0]), int(bounds[2]), self.interval)): # x coordinates:
            # if x == 174880:
                # for y in tqdm(range(456061, int(bounds[3]), self.interval)): # y coordinates:
                #     p = [x, y]
                #     if self.is_in(gdf['geometry'], p):
                #         self.cookie_baking(p, gdf, city, i)
                #         print(p)
                #         i = i + 1
            # else:
            for y in tqdm(range(int(bounds[1]), int(bounds[3]), self.interval)): # y coordinates:
                p = [x, y]
                if self.is_in(gdf['geometry'], p):
                    self.cookie_baking(p, gdf, city, i)
                    print(p)
                    i = i + 1
        return
    
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
        
        filename = path + "/" + city + "_" + str(i) + '.png'
        try:
            self.clip_and_save(gdf, mold, filename)
        except:
            print("Error occurred while saving mold " + str(i) + "in the city " + city)
    
    # def get_molds(self, middle_points:list):
    #     molds = []
    #     half_length = self.side_length / 2
        
    #     print("Getting molds")
    #     for point in tqdm(middle_points):
    #         middlex = point[0]
    #         middley = point[1]

    #         point1 = Point(middlex - half_length, middley - half_length)
    #         point2 = Point(middlex + half_length, middley - half_length)
    #         point3 = Point(middlex + half_length, middley + half_length)
    #         point4 = Point(middlex - half_length, middley + half_length)

    #         poly = Polygon([point1, point2, point3, point4])
    #         mpoly = gpd.GeoSeries(poly, crs="EPSG:5174")
    #         molds.append(mpoly)

    #     return molds            
    # path = self.save_dir + "/" + city
    # # Check whether the specified path exists or not
    # if not os.path.exists(path):
    #     # Create a new directory because it does not exist 
    #     os.makedirs(path)
    #     print("The new directory " + city + " is created!")

    # for i in tqdm(range(len(molds))):
    #     try:
    #         c = get_clipped(molds[i])
    #     except:
    #         print("Error occurred while clipping the mold.")
    #         continue

    #     filename = path + "/" + city + "_" + str(i) + '.png'
    #     try:
    #         save_to_pic(c, filename)
    #     except:
    #         print("Error occurred while saving mold " + str(i) + "in the city " + city)
    #         continue