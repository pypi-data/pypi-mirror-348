'''
This lib made for base64
Эта библиотека создана для работы с base64
made by: Wl13Poger9
'''
import json
import base64
import os
from PIL import Image
from io import BytesIO



def jsget(fp, key):
    try:
        with open(fp, 'r', encoding='utf-8') as file: 
            data = json.load(file)
            value = data.get(key, None) 
            if value is not None:return value
            else: return f'Key "{key}" not matching in JSON file.'
    except FileNotFoundError:return f'File {fp} not found.'
    except json.JSONDecodeError:return f'Error when parsing {fp}.'

def jsset(fp, key, new_value):
    try:
        with open(fp, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = new_value
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
            #print(f'Value "{key}" updated on {new_value}')
    except FileNotFoundError:return f'File {fp} not found.'
    except json.JSONDecodeError:return f'Error when parsing: {fp}.'



class imgb64:
    @staticmethod
    def decode(file_path, img): #set
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            #print(encoded_string.decode("utf-8"))
        jsset(file_path,
              os.path.basename(img).split('/')[-1],
              str(encoded_string))

    @staticmethod
    def encode(file_path, img_name): #get
        return jsget(file_path, img_name)

    @staticmethod
    def b64info(file_path, img_name, out="i`ll be back", lang='en'): #info
        base64_string = imgb64.encode(file_path, img_name)
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size
        file_kb = len(image_bytes) / 1024
        mode_to_bpp = {"RGB": 3, "RGBA": 4, "L": 1}
        bpp = mode_to_bpp.get(image.mode, 3)
        memory_kb = (width * height * bpp) / (1024**2)
        if out == "all":
            if lang == 'en':
                return f'''
                Image name: {img_name}
                Image size: {width}x{height} pixels
                Memory size (uncompressed): {memory_kb:.1f} MB
                File size on disk: {file_kb:.1f} KB'''
            else:
                return f'''
                Имя файла: {img_name}
                Размер изображения: {width}x{height} пикселей
                Размер в памяти(не сжатый): {memory_kb:.1f} МБ
                Размер файла на диске: {file_kb:.1f} КБ'''
        elif out == "img_name":return img_name
        elif out == "img_size":return f'{width}x{height}'
        elif out == "file_size":return f'{file_kb:.1f}'
        elif out == "memory_size":return f'{memory_kb:.1f}'
        else:
            return('''
            usage:
                img_name
                img_size
                file_size
                memory_size
                all''')    






'''
# Example usage
imgb64.decode('test.json', './test_img/0.jpg')
print(imgb64.encode('test.json', '0.jpg'))
print(imgb64.b64info('test.json','0.jpg'))
'''