
import PIL as Image

photo = Image.open('Orig/DSC_10992.jpg')
watermark = Image.open('watermark.jpg')
photo.paste(watermark, (25, 25), watermark)
