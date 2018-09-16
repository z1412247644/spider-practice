import tesserocr
from PIL import Image

'''
感觉对于扭曲的验证码识别效果很差
'''
image = Image.open('timg.jpeg')
image = image.convert('L')
threshold = 120
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else :
        table.append(1)
image = image.point(table, '1')
image.show()

print(tesserocr.image_to_text(image))