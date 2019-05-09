from PIL import Image as Image
from PIL import ImageEnhance as ImageEnhance
import os
import tkinter as tk
from tkinter import ttk


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


def convert(img='DSC_10992.jpg', stimmung='hell'):
    im = Image.open('orig_'+stimmung+'/' + img)
    if stimmung == 'dunkel':
        mark = Image.open('watermark_dunkel.png')
    else:
        mark = Image.open('watermark_hell.png')
    print('start with: '+img)
    watermark(im, mark, (100, 100), 1).save('marked/'+stimmung[0]+'_'+img[:-4]+'.png')
    print(img+' Done')
    #watermark(im, mark, (100, 100), 0.75).save('marked/'+stimmung[0]+'_oc_75_'+img[:-4]+'.png')
    #watermark(im, mark, (100, 100), 0.25).save('marked/'+stimmung[0]+'_oc_25_'+img[:-4]+'.png')


def preview(img='DSC_10992.jpg', stimmung='hell'):
    '''
    Preview function
    '''
    im = Image.open('orig_'+stimmung+'/' + img)
    if stimmung == 'dunkel':
        mark = Image.open('watermark_dunkel.png')
    else:
        mark = Image.open('watermark_hell.png')
    watermark(im, mark, 'tile', 0.5).show()
    watermark(im, mark, 'scale', 0.5).show()
    watermark(im, mark, (100, 100), 1).show()
    watermark(im, mark, (100, 100), 0.75).show()


def orig_hell_to_marked():
    ls = os.listdir('orig_hell')
    for foto in ls:
        convert(img=foto)


def orig_dunkel_to_marked():
    ls = os.listdir('orig_dunkel')
    for foto in ls:
        convert(img=foto, stimmung='dunkel')


def orig_to_marked():
    orig_hell_to_marked()
    orig_dunkel_to_marked()


def main():
    root = tk.Tk()
    root.title('HP-Logo Klatscher')
    top = ttk.Frame(root)
    top['padding'] = (15, 10)
    top.pack()
    prev_btn = tk.Button(top, command=preview, text='Preview')
    prev_btn.pack()
    conv_btn = tk.Button(top, command=orig_to_marked, text='Convert all')
    conv_btn.pack()
###
#    Heller selector
###
    sel_hell_var = tk.StringVar()
    sel_hell_var.set('Helle Fotos dunkles Logo')

    def preview_hell(*args):
        '''
        Preview function
        '''
        img = sel_hell.get()
        im = Image.open('orig_hell/' + img)
        mark = Image.open('watermark_hell.png')
        mark_dark = Image.open('watermark_dunkel.png')
        watermark(im, mark, 'tile', 0.5).show()
        watermark(im, mark, 'scale', 0.5).show()
        watermark(im, mark, (100, 100), 1).show()
        watermark(im, mark_dark, (100, 100), 1).show()
        watermark(im, mark, (100, 100), 0.75).show()
    sel_hell = ttk.Combobox(top, textvariable=sel_hell_var)
    sel_hell.bind('<<ComboboxSelected>>', preview_hell)
    sel_hell['values'] = os.listdir('orig_hell')
    sel_hell.pack()
###
#    Dunkel selector
###
    sel_dark_var = tk.StringVar()
    sel_dark_var.set('Dunkle Fotos helles Logo')

    def preview_dark(*args):
        '''
        Preview function
        '''
        img = sel_dark.get()
        im = Image.open('orig_dunkel/' + img)
        mark = Image.open('watermark_dunkel.png')
        mark_hell = Image.open('watermark_hell.png')
        watermark(im, mark, 'tile', 0.5).show()
        watermark(im, mark, 'scale', 0.5).show()
        watermark(im, mark, (100, 100), 1).show()
        watermark(im, mark_hell, (100, 100), 1).show()
        watermark(im, mark, (100, 100), 0.75).show()
    sel_dark = ttk.Combobox(top, textvariable=sel_dark_var)
    sel_dark.bind('<<ComboboxSelected>>', preview_dark)
    sel_dark['values'] = os.listdir('orig_dunkel')
    sel_dark.pack()
    # Code to add widgets will go here...
    root.mainloop()


if __name__ == '__main__':
    main()
