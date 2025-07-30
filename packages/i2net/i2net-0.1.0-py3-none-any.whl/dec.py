import numpy as np
from PIL import Image
import os
import re
import ipaddress

# --- lib.py content ---
def hash(n):
    return ((0x0000FFFF & n) << 16) + ((0xFFFF0000 & n) >> 16)

def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue

def getIfromRGB(rgb):
    red, green, blue = rgb
    return (red << 16) + (green << 8) + blue

def macToInt(mac):
    res = re.match(r'^((?:(?:[0-9a-f]{2}):){5}[0-9a-f]{2})$', mac.lower())
    if res is None:
        raise ValueError('invalid mac address')
    return int(res.group(0).replace(':', ''), 16)

def int_to_mac(macint):
    if type(macint) != int:
        raise ValueError('invalid integer')
    return ':'.join(['{}{}'.format(a, b)
                     for a, b
                     in zip(*[iter('{:012x}'.format(macint))]*2)])

def ipToInt(ip_address):
    return int(ipaddress.ip_address(ip_address))

def int_to_ip(int_number):
    return str(ipaddress.ip_address(int_number))

# --- image_translator.py content ---
def translateBySingleImage(image_dir):
    img = Image.open(image_dir)
    array = np.array(img)
    result = []
    xx = array[::6, ::150]

    for x in xx:
        my_string = ','.join(map(str, x[0]))
        my_list = [int(i) for i in my_string.split(",")]
        value = getIfromRGB(my_list)
        result.append(value)

    def doMac(mac1, mac2):
        mac1_str = int_to_mac(mac1).replace('00:00:00:', '')
        mac2_str = int_to_mac(mac2).replace('00:00:00:', '')
        return [mac1_str, mac2_str]

    mac = doMac(result[5], result[6])
    mac = mac[0] + ":" + mac[1]

    ip1 = f"{result[1]}.{result[2]}.{result[3]}.{result[4]}"
    ip2 = f"{result[7]}.{result[8]}.{result[9]}.{result[10]}"

    for _ in range(0, 4): result.pop(1)
    for _ in range(0, 2): result.pop(1)
    for _ in range(0, 4): result.pop(1)

    result.insert(1, ip2)
    result.insert(1, mac)
    result.insert(1, ip1)

    return result

def translateByMultiImages(images_dir):
    with open('from_image.csv', 'w') as new_file:
        images = sorted(os.listdir(images_dir))
        for image in images:
            if image != '.DS_Store':
                line = translateBySingleImage(os.path.join(images_dir, image))
                new_file.write(','.join(map(str, line)) + '\n')

# --- decrypt.py content ---
if __name__ == "__main__":
    translateByMultiImages('data')
