from PIL import Image
import io
import requests
import os
import time
import urllib.parse
import sys

from imgs import imgs_list

upload = '//upload.thwiki.cc'
quality = 50
start_time = time.time()
starts_from = int(input('starts from?: '))
num = starts_from

for img in imgs_list[starts_from:]:
    print('now_unquoted :', urllib.parse.unquote(img))
    print('num          :', num)
    if num>1:
        average_time = (time.time() - start_time) / num
        print('average_time :', average_time)
        print('images_left  :', len(imgs_list)-num)
        seconds_left = (len(imgs_list)-num) * average_time
        hours_left = int(seconds_left // 3600)
        minutes_left = int(seconds_left % 3600 // 60)
        print('time_left    :','%s:%s'% (hours_left, minutes_left))
    print('####################')


    full_img_name = 'https:' + img

    # 超时或者404,403等就放弃
    try:
        img_requests = requests.get(full_img_name,timeout=60)
        if not img_requests.ok:
            continue
    except TimeoutError:
        continue
    except :
        print('Unexpected error:',sys.exc_info()[0])
        continue

    img_object = Image.open(io.BytesIO(img_requests.content))
    img_RGB = img_object.convert('RGB')


    img_rear_path = img.replace(upload,'upload').replace('.png','.jpg').replace('.gif','.jpg').replace('.jpeg','.jpg')
    img_rear_path = urllib.parse.unquote(img_rear_path)
    img_path = os.path.join(os.path.abspath('.'),img_rear_path)
    img_dir , img_name = os.path.split(img_path)

    if not os.path.exists(img_dir):
        try:
            os.makedirs(img_dir)
        except OSError:
            print('文件名太长，跳过')
            continue

    img_RGB.save(img_path,quality = quality)
    num += 1




