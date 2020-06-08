# -*- coding: utf-8 -*-
"""
Modul Name:

Created on Tue May 14 13:15:55 2019

@author: matthias.schara
"""
import ffmpeg

ffmpeg -f image2 -r 1/5 -i image%05d.png -vcodec mpeg4 -y movie.mp4