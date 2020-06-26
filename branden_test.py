from synthetic import DrawDocument, read_dictonary, RealBackGound, SolidBackGroundback
from article import generate
import os
import numpy as np



def create_bf(dir='/home/scstech/PycharmProjects/synthetic_fonts/CNN_MODELS/test_set/F2-1'):
    files = [os.path.join(dir,f) for f in os.listdir(dir) if f.split('.')[-1] == 'jpg']
    np.random.shuffle(files)
    print len(files)

    realSampler = RealBackGound.create_bg(files=files[:15])

    return realSampler



def run_realbackground(dir, path_background,num=9, size=None, greyscale=False,type='TXT',model='branden.xml'):
    RealBackGound.dirname = path_background
    realSampler = RealBackGound.load_examples()

    generate(dir, num=num, size=size,sampler=realSampler, greyscale=greyscale,type=type,model=model)


#solidSampler = SolidBackGroundback(colors=[255])
#realSampler = RealBackGound.load_examples()

def run(dir, num=5, size=None, sampler=None, greyscale=False,type='TXT',model='branden2.xml',seed=2):
    generate(dir, num=num, size=size,sampler=sampler, greyscale=greyscale,type=type,model=model,seed=seed)



#run('BRANDEN/TEST1602')
