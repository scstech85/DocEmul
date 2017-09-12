import PIL,Image
from skimage.color import rgb2grey
import os
import csv
from scipy.misc import imread,imsave
import numpy as np
def augment_img(img, rotate=3, rotate_time=2, noise=2):
    imgs = [img]

    from scipy.misc import imrotate
    for _ in range(rotate_time):

        rotation = np.random.random()*rotate*2 - rotate
        print rotation
        M = 255

        im = PIL.Image.fromarray(np.uint8(img))
        # converted to have an alpha layer
        im2 = im.convert('RGBA')
        # rotated image
        rot = im2.rotate(rotation, expand=1)
        # a white image same size as rotated image
        fff = Image.new('RGBA', rot.size, (np.uint8(M),) * 4)
        # create a composite image using the alpha layer of rot as a mask
        out = Image.composite(rot, fff, rot)
        # save your work (converting back to mode='1' or whatever..)
        out = out.convert(im.mode)

        im = np.asarray(out).copy()
        im = rgb2grey(im)
        part = 20

        top = im[:part,:]
        v = np.mean(top[top!=M])
        im[:part, :][top == M] = v

        bottom = im[-part:,:]
        v = np.mean(bottom[bottom != M])
        im[-part:, :][bottom == M] = v

        left = im[:,:part]
        v = np.mean(left[left != M])
        im[:, :part][left == M] = v

        right = im[:,-part:]
        v = np.mean(right[right != M])
        im[:, -part:][right == M] = v

        imgs.append(im)

    for i in imgs[:rotate_time+1]:
        for _ in range(noise):
            mod = generate_noise(i)
            inv_mod = (mod==0).astype(np.uint8)

            im = i*inv_mod

            #pylab.imshow(im, cmap='Greys_r')
            #pylab.show()
            imgs.append(im)

    return imgs

def generate_noise(img, rand_no_noise=0.9, max_rand_distr=0.03, step=16):

    mod = np.zeros_like(img)
    for w in range(0, img.shape[0], img.shape[0] / step):

        for h in range(0, img.shape[1], img.shape[1] / step):
            if np.random.random() <= rand_no_noise:
                v = 0

            else:
                v = np.random.random() * max_rand_distr

            m = mod[w:w + img.shape[0] / (step / 2), h:h + img.shape[1] / (step / 2)]
            noise = (np.random.rand(m.shape[0], m.shape[1]) < v).astype(np.uint8)

            mod[w:w + img.shape[0] / (step / 2), h:h + img.shape[1] / (step / 2)] += noise

    return (mod>0).astype(np.uint8)

def data_augment(fcsv, dir_target,f_output = 'gt_augment.csv',resize=(450,190),rotate=2, rotate_time=1, noise=1):
    os.makedirs(dir_target)
    img_dir = os.path.join(dir_target, 'imgs')
    os.makedirs(img_dir)
    f_csv_o = os.path.join(dir_target, f_output)


    with open(fcsv, 'r') as csv_in:
        with open(f_csv_o, 'w') as csv_out:
            writer = csv.writer(csv_out, delimiter=' ')
            for f, r in csv.reader(csv_in, delimiter=' '):
                if os.path.isfile(f):
                    img = imread(f)
                    if resize:
                        img = imresize(img, resize)
                    a, b = os.path.split(f)

                    fname = b.split('.')[0]
                    ext = b.split('.')[1]

                    imgs = augment_img(img,rotate=rotate, noise=noise, rotate_time=rotate_time)



                    for j, ii in enumerate(imgs):
                        im_name = os.path.join(img_dir, fname+'_'+str(j)+'.'+ext)
                        imsave(im_name, ii)
                        print im_name
                        writer.writerow([im_name, r])
                else:
                    print 'file non valid:', f

