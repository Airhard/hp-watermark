photo = Image.open('original_photo.jpg')
watermark = Image.open('watermark.png')
photo.paste(watermark, (25, 25), watermark)
