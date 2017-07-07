import os
import numpy as np
from model import model_docs,read_dictonary
from draw_document import DrawDocument
import csv

def resize(im, size):
    import PIL
    try:

        im = im.resize(size, PIL.Image.ANTIALIAS)
        return im
    except IOError as e:
        print e
        #print "cannot create thumbnail for '%s'" % infile





def generate(dir, num=10, size=(365, 256), sampler = None, greyscale=True, model='article_small.xml', type = 'TEXT', seed = None):

    if seed:
        np.random.seed(seed)


    docs,dictionaries, fonts = model_docs(model)
    # sampler = SampleColors.load(file='model/sampler.pkl')
    # sampler.load()
    #sta_tr, train, tt_ff = get_stat('/home1/shared-h1/GT_volumen208/train_list.csv', list_files=True)


    #sampler = RealBackGound.load_examples(tt_ff[:15])


    #dictonary = read_dictonary('divina.txt')

    f_csv = os.path.join(dir, 'gt.csv')
    f_csv_2 = os.path.join(dir, 'gt_2.csv')
    j = 0

    if not os.path.isdir(dir):
        print 'NEW DIR: ', dir
        os.makedirs(dir)
        os.mkdir(os.path.join(dir, 'imgs'))
        os.mkdir(os.path.join(dir, 'gt'))
        csv_f = open(f_csv, 'w')
        csv_f_2 = open(f_csv_2, 'w')

    else:
        print 'OLD DIR: ', dir
        csv_f = open(f_csv, 'r')
        reader = csv.reader(csv_f, delimiter=' ')
        for _ in reader:
            j += 1
        csv_f.close()
        print 'number', j
        csv_f = open(f_csv, 'a')
        csv_f_2 = open(f_csv_2, 'a')

    writer = csv.writer(csv_f, delimiter=' ')

    writer2 = csv.writer(csv_f_2, delimiter=' ')

    dicts = [{'words':read_dictonary(dictonary.path), 'number':dictonary.number_words} for dictonary in dictionaries]

    for d in docs:
        print d.id
        for c in range(num):
            i = j + c

            doc = DrawDocument(d, sampler,dicts, fonts)
            if type == 'TXT':
                img = doc.create_only_text()
            elif type == 'IMG':
                img = doc.create_image()
            elif type == 'BKG':
                img = doc.create_background()
            else:
                print 'type err',type,'-', 'TXT, IMG, BKG'
                return

            if greyscale:
                img = img.convert('L')

            # A = 5
            # angle = np.random.randint(-1*A, A)

            # img = img.rotate(angle, resample=Image.BILINEAR)

            if size:
                img = resize(img, (size[1], size[0]))
            # img = img.resize((size[1],size[0]), PIL.Image.ANTIALIAS)

            fname = os.path.join(dir, 'imgs', 'type_'+str(d.id)+':'+str(i + 1) + '_' + str(doc.num_records) + '.png')
            print fname, 'num records', doc.num_records
            img.save(fname)
            writer.writerow([fname, doc.num_records])
            writer2.writerow([fname, doc.num_records, d.id])


    csv_f.close()
    csv_f_2.close()
