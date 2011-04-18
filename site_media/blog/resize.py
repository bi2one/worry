import os
from PIL import Image

RESIZE_SIZE = 550

def handle_image(i, f_type) :
    resize_size = RESIZE_SIZE

    path = os.getcwd()+ '/' + str(i)
    print path
    im = Image.open(path)

    width = im.size[0] * 1.0
    height = im.size[1] * 1.0

    ratio = height / width

    if width > resize_size :
        new_width = resize_size
        new_height = new_width * ratio
    else :
        new_width = width;
        new_height = height;

    new = im.resize((new_width, new_height))
    new.save(os.getcwd()+'/' + str(i), f_type)


if __name__ == '__main__' :
    lst = os.listdir('.')
    for f in lst:
        f_type = f.split('.')[1].upper()
        if f_type == "PY" or f_type == "PY~" :
            continue
        if f_type == "JPG" :
            f_type = "JPEG"
        handle_image(f, f_type)
