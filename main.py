from PIL import Image as Image
from PIL import ImageEnhance as ImageEnhance
import os

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(float(im.size[0])/mark.size[0], float(im.size[1])/mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, (int((im.size[0] - w) / 2), int((im.size[1] - h) / 2)))
    else:
        layer.paste(mark, [position[0], im.size[1] - (mark.size[1] +  position[1])])
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)


def test(img='DSC_10992.jpg', stimmung='hell'):
    im = Image.open('orig_'+stimmung+'/' + img)
    if stimmung == 'dunkel':
        mark = Image.open('watermark_dunkel.png')
    else:
        mark = Image.open('watermark_hell.png')
    #watermark(im, mark, 'tile', 0.5).show()
    #watermark(im, mark, 'scale', 0.5).show()
    #watermark(im, mark, (100, 100), 1).show()
    #watermark(im, mark, (100, 100), 0.75).show()
    watermark(im, mark, (100, 100), 1).save('marked/'+stimmung[0]+'_'+img[:-4]+'.png')
    #watermark(im, mark, (100, 100), 0.75).save('marked/'+stimmung[0]+'_oc_75_'+img[:-4]+'.png')
    #watermark(im, mark, (100, 100), 0.25).save('marked/'+stimmung[0]+'_oc_25_'+img[:-4]+'.png')

def orig_hell_to_marked():
    ls = os.listdir('orig_hell')
    for foto in ls:
        test(img=foto)

def orig_dunkel_to_marked():
    ls = os.listdir('orig_dunkel')
    for foto in ls:
        test(img=foto, stimmung='dunkel')

def orig_to_marked():
    orig_hell_to_marked()
    orig_dunkel_to_marked()

if __name__ == '__main__':
    orig_to_marked()
