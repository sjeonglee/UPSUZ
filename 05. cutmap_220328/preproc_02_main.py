# Setting Libraries

import geopandas as gpd
import mold as mold
import cutter as cut
import utils as ut
import tqdm as tqdm

if __name__ == "__main__":
    # global variables
    main_dir = "../"
    data_dir = main_dir + "03. Data_shapefile/02. color"
    save_dir = main_dir + "06. cookies/220328"
    
    # classes
    molder = mold.Molder(500, 3000, save_dir)
 
    # code starts
    print("0. Get the list of the cities")
    cities = ut.get_cities(data_dir)
    print(cities)
    
    city = 'Yangju' # Asan(v) Bundang(v) Doan(v) Dongtan(v) Geomdan(v) Godeog(v) Gwanggyo(v) Hangang(v) Ilsan(v) Joongdong(v) Pyeongchon(v) Sanbon(v) Uirye(v) Woonjeong(v) Yangju(v)
    shp_dir = data_dir + "/" + city + "/" + city + "_colored.shp"
    gdf = gpd.read_file(shp_dir, encoding = 'cp949')
    
    # get molds
    molder.get(gdf, city)