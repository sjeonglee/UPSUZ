# Setting Libraries

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import glob
import matplotlib
import ast
from shapely.geometry import Point, LineString, Polygon
from tqdm import tqdm
import cv2 as cv
import PIL
import os
import json
import logging

# Setting matplotlib
plt.rcParams['axes.facecolor'] = 'black'

# functions
def get_yongdos(shplist:list):                         # [foldername] city의 shapefile의 용도지역 전부 가져오기
    yongdos = []
    for i in tqdm(shplist):
        temp = gpd.read_file(i, encoding = 'cp949')
        temp_yongdo = temp['A14'].unique()
        for j in temp_yongdo:
            if j not in yongdos:
                yongdos.append(j)
    return yongdos

def check_outliers(yongdo_list:list, color_dict:dict): # 튀는 용도지역이 있는지 체크
    outliers = []
    for yongdo in tqdm(yongdo_list):
        if yongdo in color_dict:
            continue
        else:
            outliers.append(yongdo)
    return outliers

def get_molds(middle_points:list, side_length = 500):  # 쿠키틀 만들기
    molds = []
    half_length = side_length / 2
        
    for point in tqdm(middle_points):
        middlex = point[0]
        middley = point[1]

        point1 = Point(middlex - half_length, middley - half_length)
        point2 = Point(middlex + half_length, middley - half_length)
        point3 = Point(middlex + half_length, middley + half_length)
        point4 = Point(middlex - half_length, middley + half_length)

        poly = Polygon([point1, point2, point3, point4])
        mpoly = gpd.GeoSeries(poly, crs="EPSG:5174")
        molds.append(poly)
            
    return molds

def get_clipped(gdf:gpd.GeoDataFrame, mold:gpd.GeoSeries):  # 쿠키틀로 자르기
    clipped = gpd.clip(gdf, mold)
    return clipped

def save_to_pic(gdf:gpd.GeoDataFrame, filename:str):        # save the cutted shapefile to picture
    plt.figure(figsize = (20, 20), dpi=200)
    # plt.rcParams['font.family'] = 'Malgun Gothic'
    sample_dis = gdf[['geometry', 'A14', 'use']]
    dis = sample_dis.dissolve(by='use')
    dis.reset_index(inplace=True)
    ax = plt.subplot(1, 1, 1)
    ax.axis('off')
    plt.margins(0,0)
    dis.plot(column = 'A14', legend = True, color=dis['use'], axes=ax)

    path = 'result/' + city

    # Check whether the specified path exists or not
    if not os.path.exists(path):
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print("The new directory is created!")

    plt.savefig(filename, bbox_inches = 'tight', pad_inches = 0)

def classify_pic(filename):                                 # check if the dominant color is white
    # Read pic
    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    # make copy and get dominant color
    img_temp = img.copy()
    unique, counts = np.unique(img_temp.reshape(-1, 3), axis=0, return_counts=True)
    img_temp[:,:,0], img_temp[:,:,1], img_temp[:,:,2] = unique[np.argmax(counts)]
    
    return np.array_equal(img_temp[0, 0], np.array([255, 255, 255]))

def get_shp(foldername:str, mainpath:str='Data')->gpd.GeoDataFrame:       # [foldername] city: load, concat and color shapefile
    def concat_shp()->gpd.GeoDataFrame:                       # shapefile 합치기
        file_directory = glob.glob(mainpath + "/*" + foldername + "/*")
        shps = [file for file in file_directory if file.endswith(".shp")]
        return gpd.GeoDataFrame(pd.concat([gpd.read_file(i, encoding = 'cp949') for i in shps], 
                            ignore_index=True), crs="EPSG:5174")
    
    def get_gdf_color(gdf:gpd.GeoDataFrame):                              # 각종 용도지역과 도로 구분해서 색칠
        def get_color(line):                               # 도로를 검은색으로 색칠
            isdoro = line['A11']
            if isdoro == '도로':
                return '#000000'
            
            name = line['A14']
            if name == 'None':
                name = ast.literal_eval(name)
            if name in color_dict:
                return color_dict[name]

        # get color based on yongdo
        gdf['use'] = gdf.apply(get_color, axis=1)
        
        return gdf
    
    print("============= Get the shapefile of the city " + foldername + " =============")    
    try:
        gdf = concat_shp()
    except:
        print("Error occurred while getting the shapefiles of " + foldername)
        logger.info(foldername + " error 1")
        return
    
    try:
        gdf_colored = get_gdf_color(gdf)
    except:
        print("Error occurred while coloring the shapefiles of " + foldername)
        logger.info(foldername + " error 2")
        return

    return gdf_colored
    
def get_molds(gdf:gpd.GeoDataFrame):
    def get_bounds()->np.array:                  # get the boundary
        bounds = gdf.total_bounds
        return bounds
    
    def is_in(polygon:gpd.GeoSeries, point:list):
        p = Point(point[0], point[1])
        if_contains = polygon.contains(p, align=False)
        return if_contains.any()
    
    def get_points(polygon:gpd.GeoSeries, bounds, interval:int):                  # get the middle points of the boundary
        middle_points = []

        for x in range(int(bounds[0]), int(bounds[2]), interval): # x coordinates:
            for y in range(int(bounds[1]), int(bounds[3]), interval): # y coordinates:
                p = Point(x, y)
                if is_in(polygon, p):
                    middle_points.append([x, y])
        
        return middle_points
    
    # def get_onlyinmap(polygon:gpd.GeoSeries, points:list): # find the points only in map
    #     # def is_in(polygon:gpd.GeoSeries, point:list):
    #     #     p = Point(point[0], point[1])
    #     #     if_contains = polygon.contains(p, align=False)
    #     #     return if_contains.any()

    #     for point in tqdm(points[:]):
    #         if not is_in(polygon, point):
    #             points.remove(point)
        
    #     return points
    
    try:
        poly = get_bounds(gdf)
    except:
        print("Error occurred while find the whole cover of the shapefiles of " + city)
        logger.info(city + " error 5")
        return
    
    try:
        middle_points = get_points(poly, grid_size)
    except:
        print("Error occurred while getting the middle points of " + city)
        logger.info(city + " error 6")
        return
    
    try:
        molds = get_molds(middle_points_renew, side_length)
    except:
        print("Error occurred while getting the molds of " + city)
        logger.info(city + " error 8")
        return
    

def total_func(city):
    print("========= 1. get and concat shapefiles of " + city + " =========")
    # try:
    #     shplist = get_shplist(city)
    # except:
    #     print("Error occurred while get the shapefiles of " + city)
    #     logger.info(city + " error 1")
    #     return
    
    # print("========= 2. check if any outliers of uses =========") : 없음!
    # yongdo_list = get_yongdos(shp)
    
    # outliers = check_outliers(yongdo_list, color_dict)
    # print(outliers)
    
    # try:
    #     gdf = concat_shp(shplist)
    # except:
    #     print("Error occurred while concat the shapefiles of " + city)
    #     logger.info(city + " error 3")
    #     return
    

    print("========= 4. Color the shapefile =========")
    # try:
    #     gdf = get_gdf_color(gdf)
    # except:
    #     print("Error occurred while coloring the shapefiles of " + city)
    #     logger.info(city + " error 4")
    #     return
    
    gdf = get_shp(city)
    print("========= 5. Find the whole cover of the shapefile =========")
    try:
        poly = get_bounds(gdf)
    except:
        print("Error occurred while find the whole cover of the shapefiles of " + city)
        logger.info(city + " error 5")
        return
    
    print("========= 6. Find the middle points =========")
    print("The grid interval is " + str(grid_size))
    try:
        middle_points = get_points(poly, grid_size)
    except:
        print("Error occurred while getting the middle points of " + city)
        logger.info(city + " error 6")
        return
    
    try:
        middle_points_renew = get_onlyinmap(gdf['geometry'], middle_points)
    except:
        print("Error occurred get the points only in map of " + city)
        logger.info(city + " error 7")
        return
    
    print("========= 7. Cut the shapefile cookies of " + city + " =========")
    try:
        molds = get_molds(middle_points_renew, side_length)
    except:
        print("Error occurred while getting the molds of " + city)
        logger.info(city + " error 8")
        return
    
    print("The number of molds are " + str(len(molds)))
    return molds, gdf


if __name__ == "__main__":
    # set logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(u'%(asctime)s %(message)s')
    
    # FileHandler
    file_handler = logging.FileHandler('logs/output.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info("Start!")
    
    # variables
    grid_size = 500
    side_length = 3000
    result_path = 'result/'
    
    print("========= 0. Get the list of cities =========")
    folders = os.listdir("Data")
    print(folders)
    
    # color dictionary loading

    with open('color.json', 'r', encoding='utf-8') as f:
        color_dict = json.load(f)
    
    for city in folders:
        try:
            molds, gdf = total_func(city)
        except:
            print("Nothing returned")
            continue
        
        print("========= 8. Save the shapefile cookies of " + city + " =========")
        for i in tqdm(range(len(molds))):
            try:
                c = get_clipped(gdf, molds[i])
            except:
                print("Error occurred while clipping the mold " + str(i) + " in the city " + city)
                logger.info(city + " error 9")
                continue
            
            filename = result_path + "/" + city + "/" + city + "_" + str(i) + '.png'
            try:
                save_to_pic(c, filename)
                del c
            except:
                print("Error occurred while saving mold " + str(i) + "in the city " + city)
                logger.info(city + " error 10")
                continue
                
        
    # print("========= 9. Check if the dominant color is black =========")
        