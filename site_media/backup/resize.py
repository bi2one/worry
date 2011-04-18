import os
from PIL import Image

RESIZE_SIZE = 550

def handle_image(i, f_type) :
    resize_size = RESIZE_SIZE

    im = Image.open(str(i))

    width = im.size[0] * 1.0
    height = im.size[1] * 1.0

    ratio = height / width

    if width > resize_size :
        new_width = resize_size
        if width > height :
            new_height = new_width / ratio
        else :
            new_height = new_width * ratio
    else :
        new_width = width;
        new_height = height;

    new = im.resize((new_width, new_height))
    new.save(str(i), f_type)


if __name__ == '__main__' :
    lst = os.listdir()
    for f in lst:
        f_type = f.split('.')[1].upper()
        if f_type != "JPG" or f_type != "PNG" :
            continue
        handle_image(f, f_type)
