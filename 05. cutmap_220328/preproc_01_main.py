# Setting Libraries
import glob
import utils as ut
import detector as dt
import shpconcator as sc

if __name__ == "__main__":
    # global variables
    main_dir = "../"
    data_dir = main_dir + "01. Data_original"
    color_dir = main_dir + "color.json"
    
    # classes
    detector = dt.Detector(color_dir)
    concator = sc.ShpConcator(data_dir, color_dir)
    
    # code starts
    print("0. Get the list of the cities")
    cities = ut.get_cities(data_dir)
    
    # detect outliers (outliers are saved in the object 'detector')
    for city in cities:
        file_directory = glob.glob(data_dir + "/" + city + "/*")
        shps = [file for file in file_directory if file.endswith(".shp")]
    
        detector.check_outliers_from_list(shps)
    
    print(detector.outliers)
    
    # concat and color all shapefiles for each cities
    for city in cities:
        concator.get_shp(city, '../03. Data_shapefile')