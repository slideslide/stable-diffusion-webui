import base64
import random
from PIL import Image
from io import BytesIO
import os
import numpy as np
import cv2
import requests

def to_datauri(image:Image) -> str:
    image_format = image.format
    mime_types = {
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        # 根据需要添加更多格式
    }
    mime_type = mime_types.get(image_format.lower(), 'application/octet-stream')
    buffered = BytesIO()
    format = 'JPEG'  # 根据你的图片格式选择合适的格式
    image.save(buffered, format=format)  # 保存图片到字节流中
    img_data = buffered.getvalue()
    base64_encoded = base64.b64encode(img_data).decode('utf-8')
    data_uri = f"data:image/{format.lower()};base64,{base64_encoded}"
    print(data_uri)
    return data_uri


def from_datauri(data_uri: str) -> Image:
    # 解析Data URI，分割出Base64编码的数据部分
    if data_uri.startswith('data:image'):
        start = data_uri.find(',') + 1
        # 去除Base64编码的数据部分
        image_data = data_uri[start:]
    else:
        raise ValueError("Invalid Data URI format")

    # 对数据进行Base64解码
    image_data_bytes = base64.b64decode(image_data)

    # 使用BytesIO创建一个可读的字节流
    image_stream = BytesIO(image_data_bytes)

    # 使用Pillow从字节流中加载图像
    image = Image.open(image_stream)

    return image

def get_random_image(matchID:int):
    if matchID in [2,4,5,6]:
        image_dir=f"images/{matchID}"
        files = os.listdir(image_dir)
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if image_files:
            selected_image = random.choice(image_files)
            print(selected_image)
            file = f"{image_dir}/{selected_image}"
            image = Image.open(file)
            return image

def download_image(image_url):
    watermark_position=(0,40)
    watermark_size=(0,40)
    # 使用requests获取图片数据
    response = requests.get(image_url)

    # 确保请求成功
    if response.status_code == 200:
        # 将获取的二进制数据包装在BytesIO对象中
        image_data = BytesIO(response.content)
        # 使用Pillow打开图片数据
        image = Image.open(image_data)
        width, height = image.size
        # 确定裁剪区域
        left = 0
        top = 0
        right = width - watermark_position[0] - watermark_size[0]
        bottom = height - watermark_position[1] - watermark_size[1]
        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image


def modify_color_temperature(img):
    cold_p1 = random.randint(10,100)
    cold_p2 = random.randint(10,100)
    # ---------------- 冷色調 ---------------- #

    height = img.shape[0]
    width = img.shape[1]
    dst = np.zeros(img.shape, img.dtype)

    # 1.計算三個通道的平均值，並依照平均值調整色調
    imgB = img[:, :, 0]
    imgG = img[:, :, 1]
    imgR = img[:, :, 2]

    # 調整色調請調整這邊~~
    # 白平衡 -> 三個值變化相同
    # 冷色調(增加b分量) -> 除了b之外都增加
    # 暖色調(增加r分量) -> 除了r之外都增加
    bAve = cv2.mean(imgB)[0]
    gAve = cv2.mean(imgG)[0] + cold_p1
    rAve = cv2.mean(imgR)[0] + cold_p2
    aveGray = (int)(bAve + gAve + rAve) / 3

    # 2. 計算各通道增益係數，並使用此係數計算結果
    bCoef = aveGray / bAve
    gCoef = aveGray / gAve
    rCoef = aveGray / rAve
    imgB = np.floor((imgB * bCoef))  # 向下取整
    imgG = np.floor((imgG * gCoef))
    imgR = np.floor((imgR * rCoef))

    # 3. 變換後處理
#     for i in range(0, height):
#         for j in range(0, width):
#             imgb = imgB[i, j]
#             imgg = imgG[i, j]
#             imgr = imgR[i, j]
#             if imgb > 255:
#                 imgb = 255
#             if imgg > 255:
#                 imgg = 255
#             if imgr > 255:
#                 imgr = 255
#             dst[i, j] = (imgb, imgg, imgr)

    # 將原文第3部分的演算法做修改版，加快速度
    imgb = imgB
    imgb[imgb > 255] = 255

    imgg = imgG
    imgg[imgg > 255] = 255

    imgr = imgR
    imgr[imgr > 255] = 255

    cold_rgb = np.dstack((imgb, imgg, imgr)).astype(np.uint8)
    image = Image.fromarray(cold_rgb)
    return image
 