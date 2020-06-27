from imageio import imread, imsave
from skimage.transform import resize as imresize
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
import numpy as np
from sklearn import mixture
from sklearn.externals import joblib
import os

class BackGroudModel:
    def sample_bgimage(self, size):
        pass


class SampleColors(BackGroudModel):

    def __init__(self, X,y, gmms=None):
        self.gmms = gmms
        self.X,self.y = (X, y)

    @classmethod
    def load_distr(cls, image_files):

        return cls(cls.__create_distribution__(image_files),None)



    def __compute_gmm__(self,X,comp=5,verbose=1):
        np.random.seed(1)
        g = mixture.GMM(n_components=comp, verbose=verbose)
        g.fit(X)

        return g

    def __create_distribution__(self,files):
        X = []
        y = []
        shapes = []
        for f in files:
            print(f)
            img = imread(f)

            gray = rgb2gray(img)

            shapes.append(gray.shape)

            th = threshold_otsu(gray)
            labels = (gray <= th).astype(np.uint8)

            l = img.shape[0] * img.shape[1]
            a = img.reshape(l, 3)

            l = labels.ravel()

            # print '1', len(filter(lambda v: v == 1, l))
            # print '0', len(filter(lambda v: v == 0, l))

            print(a.shape, l.shape)
            X.append(a)
            y.append(l)

        return np.concatenate(X), np.concatenate(y)

    def fit(self, label, n_components=5):
        assert label == 0 or label == 1

        i = np.where(self.y == label)[0]

        self.gmms[label] = self.__compute_gmm__(self.X[i], comp=n_components)

    def sample(self, label, size):
        assert label in self.gmms
        H,W = size

        img = self.gmms[label].sample_bgimage(W * H).astype(np.uint8).reshape(H, W, 3)

        return img

    def sample_bgimage(self, size):
        return self.sample(0, size)

    def save(self, file='sampler.pkl'):
        joblib.dump(self, file)

    @classmethod
    def load(cls, file='sampler.pkl'):
        obj = joblib.load(file)
        return cls(obj.X,obj.y,obj.gmms)


def get_background(file):
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

    from skimage.morphology import disk
    from skimage.filters import threshold_otsu
    from skimage.morphology import dilation

    th = threshold_otsu(img)

    selem = disk(3)

    fg_pos = (img <=th)

    fg_pos = dilation(fg_pos, selem).astype(np.bool)

    fg = fg_pos.astype(np.uint8)



    r,c = np.where(img <=th)

    pixels = sorted(zip(r,c))

    r = 10

    #pylab.imshow(img,cmap='Greys_r')
    #pylab.show()
    i = 0
    for y,x in pixels:
        i+=1
        print(i, len(pixels))
        if fg[y,x]==1:
            print(y,x)
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


    return img

def get_files(dir, ext='jpg'):
    for f in os.listdir(dir):
        f_name = os.path.join(dir, f)

        if os.path.isfile(f_name) and f.split('.')[1] == ext:
            print(f)
            yield f_name, f


def create_g_dataset(dir, target, ext='jpg'):
    if not os.path.isdir(target):
        os.mkdir(target)

        for src, fname in get_files(dir, ext=ext):
            print(src)
            bg_file = get_background(src)
            f_bg = os.path.join(target, fname)
            imsave(f_bg, bg_file)

    else:
        print('already done!!!')


class RealBackGound(BackGroudModel):
    basepath = '.'
    dirname = 'BG2_MODELS'
    def __init__(self, files, localdir):
        self.localdir = localdir
        self.files = files

    @classmethod
    def load_examples(cls):
        local_dir = os.path.join(cls.basepath, cls.dirname)
        files = [os.path.join(local_dir, f) for f in os.listdir(local_dir)]
        return cls(files, local_dir)


    @classmethod
    def create_bg(cls, files):

        local_dir = os.path.join(cls.basepath, cls.dirname)

        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)

            for src in files:
                _, fname = os.path.split(src)
                print(src)
                bg_file = get_background(src)
                f_bg = os.path.join(local_dir, fname)
                imsave(f_bg, bg_file)

        files = [os.path.join(local_dir, f) for f in os.listdir(local_dir)]

        return cls(files, local_dir)


    def sample_bgimage(self, size):
        np.random.shuffle(self.files)

        img = imread(self.files[0])

        img = imresize(img, size)

        return img


class RealBackGoundBack(BackGroudModel):
    basepath = '.'
    dirname = 'BG2_MODELS'
    def __init__(self, files, localdir):
        self.localdir = localdir
        self.files = files

    @classmethod
    def load_examples(cls, dir):

        local_dir = os.path.join(cls.basepath, cls.dirname)


        create_g_dataset(dir, local_dir)
        files = [os.path.join(local_dir, f) for f in os.listdir(local_dir)]

        return cls(files, local_dir)


    def sample_bgimage(self, size):
        np.random.shuffle(self.files)

        img = imread(self.files[0])

        img = imresize(img, size)

        return img


class SolidBackGroundback(BackGroudModel):
    def __init__(self,colors = [255]):
        self.colors = colors
    def sample_bgimage(self, size):
        bg = np.ones(size,dtype=np.uint8)
        np.random.shuffle(self.colors)

        return bg*self.colors[0]
