from docemul.generator import generate
from docemul.backgroundmodel import RealBackGound
from docemul.augment import data_augment

RealBackGound.dirname = 'EXAMPLES/Esposalles/BACKGROUND'

realSampler = RealBackGound.load_examples()

def run(dir, num=5, size=None, sampler=realSampler, greyscale=True,type='IMG',model='esposalles.xml',seed=2):
    generate(dir, num=num, size=size,sampler=sampler, greyscale=greyscale,type=type,model=model,seed=seed)

#generate dataset with background
#run('GENERATED/Esposalles/test')

#data_augmentation
data_augment('GENERATED/Esposalles/test/gt.csv', 'GENERATED/Esposalles/test_augmented',f_output = 'gt_augment.csv',resize=None,rotate=2, rotate_time=1, noise=1)




