# 참고자료: https://qzqz.tistory.com/660

from tqdm import tqdm
import glob
from PIL import Image

print("Process Start")

image_list = glob.glob("/home/urban/Workspace/sjeong/vscode/thesis/01. dataprocessing/01. cutmap/06. cookies/right_cookies_0711/*")
save_dir = "/home/urban/Workspace/sjeong/vscode/thesis/01. dataprocessing/01. cutmap/06. cookies/right_cookies_0711_aug/"

# print(image_list)
def get_flip_topbottom(image_dir):
    image = Image.open(image_dir)
    new_image_name = image_dir.split("/")[-1].split(".")[0] + "_topbottom.png"
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(save_dir + new_image_name)
    image.close()

def get_flip_leftright(image_dir):
    image = Image.open(image_dir)
    new_image_name = image_dir.split("/")[-1].split(".")[0] + "_leftright.png"
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image.save(save_dir + new_image_name)
    image.close()

def get_rotate(image_dir):
    for rotate in [90, 180, 270]:
        image = Image.open(image_dir)
        Xdim, Ydim = image.size
        new_image_name = image_dir.split("/")[-1].split(".")[0] + "_rotate" + str(rotate) + ".png"        
        image = image.rotate(rotate)
        image = image.resize((Xdim, Ydim))
        image.save(save_dir + new_image_name)
        image.close()

for image in tqdm(image_list):
    get_flip_topbottom(image)
    get_flip_leftright(image)
    get_rotate(image)
