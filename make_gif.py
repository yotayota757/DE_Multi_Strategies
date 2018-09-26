from PIL import Image
import glob
import os

os.chdir("./results/figure")
files = sorted(glob.glob('./*.png'))
images = list(map(lambda file: Image.open(file), files))

images[0].save('../gif/result.gif', save_all=True, append_images=images[1:], duration=400, loop=0)