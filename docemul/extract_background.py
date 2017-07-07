from scipy.misc import imread, imsave, imresize

import numpy as np
import pylab

from skimage.morphology import disk
from skimage.filters import threshold_otsu
from skimage.morphology import dilation

from sauvola_binarization import compute_sauvola_binarization


def get_background_otsu(file):

    def get_bounds(y,x,r):
        left = x - r
        left = 0 if left < 0 else left

        right = x + r
        right = img.shape[1] if right > img.shape[1] else right

        top = y - r
        top = 0 if top < 0 else top

        bottom = y + r
        bottom = img.shape[0] if bottom > img.shape[0] else bottom

        return left, top, right, bottom

    def ok_bounds(patch):
        values = np.bincount(patch.flatten())
        return values[0]>0


    img = imread(file, flatten=True).astype(np.uint8)

    th = threshold_otsu(img)

    selem = disk(3)

    fg_pos = (img <=th)

    fg_pos = dilation(fg_pos, selem).astype(np.bool)

    fg = fg_pos.astype(np.uint8)


    r,c = np.where(img <=th)

    pixels = sorted(zip(r,c))

    r = 10

    i = 0

    for y,x in pixels:
        i+=1
        print i, len(pixels)
        if fg[y,x]==1:
            print y,x
            left, top, right ,bottom = get_bounds(y,x,r)
            while(ok_bounds(fg[top:bottom,left:right])==False):

                r+= r/2

                left, top, right, bottom = get_bounds(y, x, r)

            patch = img[top:bottom,left:right]



            fg_patch = fg[top:bottom, left:right]

            val = np.mean(patch[fg_patch == 0])



            fg_patch[fg_patch == 1]*=np.uint8(val)

            fg[top:bottom, left:right] = fg_patch

    img[fg_pos] = 0
    img+=fg

    return img




def get_background_sauvola(file):

    def get_bounds(y,x,r):
        left = x - r
        left = 0 if left < 0 else left

        right = x + r
        right = img.shape[1] if right > img.shape[1] else right

        top = y - r
        top = 0 if top < 0 else top

        bottom = y + r
        bottom = img.shape[0] if bottom > img.shape[0] else bottom

        return left, top, right, bottom

    def ok_bounds(patch):
        values = np.bincount(patch.flatten())
        return values[0]>0
    img = imread(file, flatten=True).astype(np.uint8)

    selem = disk(3)

    fg_all = compute_sauvola_binarization(img,resize=(1024,768))

    fg_pos = dilation(fg_all, selem).astype(np.bool)

    fg = fg_pos.astype(np.uint8)

    #fg = dilation(fg, selem)
    #bg = img >th

    r,c = np.where(fg_all>0)

    pixels = sorted(zip(r,c))

    r = 10

    #pylab.imshow(img,cmap='Greys_r')
    #pylab.show()
    i = 0
    for y,x in pixels:
        i+=1
        print i, len(pixels)
        if fg[y,x]==1:
            print y,x
            left, top, right ,bottom = get_bounds(y,x,r)
            while(ok_bounds(fg[top:bottom,left:right])==False):

                r+= r/2

                left, top, right, bottom = get_bounds(y, x, r)

            patch = img[top:bottom,left:right]

            #val = np.max(patch)

            fg_patch = fg[top:bottom, left:right]

            val = np.mean(patch[fg_patch == 0])

            #val = th * 1.40

            fg_patch[fg_patch == 1]*=np.uint8(val)

            fg[top:bottom, left:right] = fg_patch
    img[fg_pos] = 0
    img+=fg
    #pylab.imshow(img,cmap='Greys_r')
    #pylab.show()

    #img = median(img, disk(3))

    #pylab.imshow(img_a, cmap='Greys_r')
    #pylab.show()

    return img


import os


def create_background_dataset(dir, target, ext='jpg', type='otsu'):
    from util import get_files

    if not os.path.isdir(target):
        os.mkdir(target)

    for src, fname in get_files(dir,ext=ext):
        print src

        if type == 'otsu':
            bg_file = get_background_otsu(src)
        else:
            bg_file = get_background_sauvola(src)
        f_bg = os.path.join(target, fname)
        imsave(f_bg, bg_file)

