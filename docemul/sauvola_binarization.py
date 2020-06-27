import numpy as np
from scipy.ndimage import interpolation,filters
from skimage.transform import resize as imresize

def autoinvert(image):
    """Automatically invert document images, so that the majority of pixels
    (background pixels) are black."""
    if np.median(image)>np.mean([np.amax(image),np.amin(image)]):
        image = np.amax(image)-image
    return image

def gsauvola(image,sigma=150.0,R=None,k=0.3,filter='uniform',scale=1.0):
    """Perform Sauvola-like binarization.  This uses linear filters to
    compute the local mean and variance at every pixel."""
    if image.dtype==np.dtype('uint8'): image = image / 256.0
    if len(image.shape)==3: image = np.mean(image,axis=2)
    if filter=="gaussian":
        filter = filters.gaussian_filter
    elif filter=="uniform":
        filter = filters.uniform_filter
    else:
        pass
    scaled = interpolation.zoom(image,1.0/scale,order=0,mode='nearest')
    s1 = filter(np.ones(scaled.shape),sigma)
    sx = filter(scaled,sigma)
    sxx = filter(scaled**2,sigma)
    avg_ = sx / s1
    stddev_ = np.maximum(sxx/s1 - avg_**2,0.0)**0.5
    s0,s1 = avg_.shape
    s0 = int(s0*scale)
    s1 = int(s1*scale)
    avg = np.zeros(image.shape)
    interpolation.zoom(avg_,scale,output=avg[:s0,:s1],order=0,mode='nearest')
    stddev = np.zeros(image.shape)
    interpolation.zoom(stddev_,scale,output=stddev[:s0,:s1],order=0,mode='nearest')
    if R is None: R = np.amax(stddev)
    thresh = avg * (1.0 + k * (stddev / R - 1.0))
    return np.array(255*(image>thresh),'uint8')


def compute_sauvola_binarization(img_oo, resize=(1024, 768), scale=1):
    prev_size = None
    if resize:
        prev_size = img_oo.shape[:2]
        img_oo = imresize(img_oo, resize)

    img_oo = autoinvert(img_oo)
    img_inv = gsauvola(img_oo,scale=scale)

    if resize:
        img_inv = imresize(img_inv, prev_size, interp='nearest')

    return img_inv
