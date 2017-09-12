import  csv
import numpy as np
#import pylab
import os
from scipy.misc import imread,imsave
def gray_rgb(fcsv,dir_target,base='/home1/samuele-h1/PycharmProjects/synthetic_handwritten'):



    os.makedirs(dir_target)
    img_dir = os.path.join(dir_target, 'imgs')
    os.makedirs(img_dir)
    f_csv_o = os.path.join(dir_target, 'gt.csv')


    with open(fcsv, 'r') as csv_in:
        with open(f_csv_o, 'w') as csv_out:
            writer = csv.writer(csv_out, delimiter=' ')
            for f, r in csv.reader(csv_in, delimiter=' '):
                f = os.path.join(base,f)
                if os.path.isfile(f):
                    img = imread(f)
                    out = np.array([img]*3)
                    out = np.swapaxes(out, 0,2)
                    out = np.swapaxes(out, 1, 0)
                    #pylab.imshow(out)
                    #pylab.show()

                    a,b = os.path.split(f)
                    im_name = os.path.join(img_dir, b)
                    imsave(im_name, out)
                    writer.writerow([im_name, r])
                else:
                    print 'file non valid:', f



gray_rgb('/home/samuele/samuele-h1/PycharmProjects/synthetic_handwritten/ARTICLE_SPLIT/5/train_sauvola/gt_train_1.csv','/home/samuele/samuele-h1/PycharmProjects/synthetic_handwritten/ARTICLE_SPLIT/5/train_sauvola_rgb')
gray_rgb('/home/samuele/samuele-h1/PycharmProjects/synthetic_handwritten/ARTICLE_SPLIT/5/train_sauvola/gt_valid_1.csv','/home/samuele/samuele-h1/PycharmProjects/synthetic_handwritten/ARTICLE_SPLIT/5/validation_sauvola_rgb')
gray_rgb('/home/samuele/samuele-h1/PycharmProjects/synthetic_handwritten/ARTICLE_SPLIT/5/test_sauvola/gt.csv','/home/samuele/samuele-h1/PycharmProjects/synthetic_handwritten/ARTICLE_SPLIT/5/test_sauvola_rgb')


print 'fine'
