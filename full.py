from PIL import Image
import os
import numpy as np
import datetime
from netCDF4 import Dataset, date2num

DATE = "20220215"
TIME = "0030"
WIDTH = 800
HEIGHT = 750
RADIUS = 239
locate_x = {'pm': 283, 'ba': 200, 'va': 20}
locate_y = {'pm': 232, 'ba': 10, 'va': 260}
radars = ['va', 'ba', 'pm']

def check_pixels(pixel_map, x, y, width, height, filter_size, num_count):
    if x < filter_size or y < filter_size or x + filter_size // 2 >= width or y + filter_size // 2 >= height :
        return False, 0
    count = 0
    closest_pixel = 0
    dif = 999999
    for i in range(-filter_size//2, filter_size // 2):
        for j in range(-filter_size//2, filter_size // 2):
            if 100 < pixel_map[x - i, y - j] < 109:
                count += 1
            elif dif > i + j:
                dif = i + j
                closest_pixel = pixel_map[x - i, y - j]
    return bool(100 < pixel_map[x, y] < 109 and count < num_count), closest_pixel

def remove_interferences(orig_image, mod_image):
    orig_pixel_map = orig_image.load()
    mod_pixel_map = mod_image.load()
    width, height = orig_image.size
    for x in range(width):
        for y in range(height):
            is_interf, closest_pixel = check_pixels(orig_pixel_map, x, y, width, height, 16, 150)
            if is_interf:
                mod_pixel_map[x, y] = closest_pixel
    return mod_image

def overlap(names_radars):
    new_image = Image.new(mode='RGB', size=(WIDTH, HEIGHT))
    new_image_map = new_image.load()
    new_w, new_h = new_image.size
    for name, radar in names_radars:
        img = Image.open(name)
        orig_image = Image.open(name)
        mod_image = Image.open(name)
        img = remove_interferences(orig_image, mod_image)
        img = img.convert('RGB')
        img_map = img.load()
        put_x = locate_x[radar]
        put_y = locate_y[radar]
        cx = put_x + RADIUS
        cy = put_y + RADIUS

        for x in range(new_w):
            for y in range(new_h):
                if RADIUS ** 2 > ((x - cx) ** 2 + (y - cy) ** 2):
                    new_image_map[x, y] = img_map[x - put_x, y - put_y]
    return new_image


def create_ncdf():
    FOLDER_FROM = './joined'
    imgs_path = os.listdir(FOLDER_FROM)

    unout = 'days since 2000-01-01 00:00:00'
    ny, nx = (HEIGHT, WIDTH)

    img = Image.open('sample.gif')
    dataout = [np.asarray(Image.open(os.path.join(FOLDER_FROM, img_path)).convert(
        "P", palette=img.getpalette, colors=128)) for img_path in imgs_path]
    datesout = [datetime.datetime.strptime(img_path.split('.')[0].split('_')[-1][:8], '%Y%m%d')
                for img_path in imgs_path] 
    ncout = Dataset('myfile.nc', 'w', 'NETCDF3')
    ncout.createDimension('lon', nx)
    ncout.createDimension('lat', ny)
    ncout.createDimension('time', len(imgs_path))
    timevar = ncout.createVariable('time', 'float64', ('time'))
    timevar.setncattr('units', unout)
    timevar[:] = date2num(datesout, unout)
    myvar = ncout.createVariable('myvar', 'float32', ('time', 'lat', 'lon'))
    myvar.setncattr('units', 'km')
    myvar[:] = dataout
    ncout.close()


if __name__ == "__main__":
    main_radar = 'va'
    other_radars = ['ba', 'pm']
    save_folder = './joined'
    path = f"./transfer_221072_files_ec30eaf2/dataset_v1/aemet/10min/{main_radar}/"
    i = 0
    for dir in os.listdir(path):
        dir_path = os.path.join(path, dir)
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            names_radars = [(file_path, main_radar)]
            for other_radar in other_radars:
                other_file = file_path.replace('va', other_radar)
                names_radars.append((other_file, other_radar))
            new_image = overlap(names_radars)
            new_image.save(f'./joined/{file.split(".")[0]}.png')
            break
        break
    # create_ncdf()
