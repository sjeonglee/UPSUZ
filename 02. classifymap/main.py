import os
import glob
import utils
import json
from tqdm import tqdm
import shutil

if __name__ == "__main__":
    # image size로 분류
    
    # main_dir = "../"
    # image_dir = main_dir + "01. cutmap/06. cookies/220328/"
    # cities = os.listdir(image_dir)
    
    # right_sized_images = dict()
    
    # for city in tqdm(cities):
    #     right_sized_images[city] = []
        
    #     image_list = glob.glob(image_dir + city + "/*")
    #     for img in tqdm(image_list):
    #         if utils.is_rightsize(img):
    #             right_sized_images[city].append(img)
    
    # with open('./data.json','w') as f:
    #     json.dump(right_sized_images, f)
    
    
    # road pixel로 분류
    
    # with open('rightsize.json', 'r') as f:
    #     color_dict = json.load(f)
    
    # right_colored_images = dict()
    
    # for city in tqdm(color_dict):
    #     image_list = color_dict[city]
    #     if len(image_list) == 0:
    #         continue
        
    #     right_colored_images[city] = []
        
    #     for img in tqdm(image_list):
    #         if utils.is_enoughroad(img, 0.1, 0.3):
    #             right_colored_images[city].append(img)
    
    # with open('./rightcolor_0103.json','w') as f:
    #     json.dump(right_colored_images, f)
        
    with open('rightcolor_0103.json', 'r') as f:
        right_dict = json.load(f)
    
    for city in right_dict:
        if len(city) == 0:
            continue
        
        image_list = right_dict[city]
        
        for img in image_list:
            shutil.copy(img, '/home/urban/Workspace/sjeong/vscode/thesis/dataprocessing/01. cutmap/06. cookies/right_cookies_0103')