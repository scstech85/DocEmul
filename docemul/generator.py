import os
import numpy as np
from .model import model_docs, read_dictonary
from .draw_document import DrawDocument
import csv

def resize(im, size):
    import PIL
    try:

        im = im.resize(size, PIL.Image.ANTIALIAS)
        return im
    except IOError as e:
        print(e)
        #print "cannot create thumbnail for '%s'" % infile


def generate(dir, num=10, size=(365, 256), sampler = None, greyscale=True, model='article_small.xml', type = 'TEXT', seed = None):

    if seed:
        np.random.seed(seed)


    docs, dictionaries, fonts = model_docs(model)
    # sampler = SampleColors.load(file='model/sampler.pkl')
    # sampler.load()
    #sta_tr, train, tt_ff = get_stat('/home1/shared-h1/GT_volumen208/train_list.csv', list_files=True)


    #sampler = RealBackGound.load_examples(tt_ff[:15])


    #dictonary = read_dictonary('divina.txt')

    f_csv = os.path.join(dir, 'gt.csv')
    f_csv_2 = os.path.join(dir, 'gt_2.csv')
    j = 0

    if not os.path.isdir(dir):
        print('NEW DIR: ', dir)
        os.makedirs(dir, exist_ok=True)
        os.mkdir(os.path.join(dir, 'imgs'))
        os.mkdir(os.path.join(dir, 'gt'))
        csv_f = open(f_csv, 'w')
        csv_f_2 = open(f_csv_2, 'w')

    else:
        print('OLD DIR: ', dir)
        csv_f = open(f_csv, 'r')
        reader = csv.reader(csv_f, delimiter=' ')
        for _ in reader:
            j += 1
        csv_f.close()
        print('number', j)
        csv_f = open(f_csv, 'a')
        csv_f_2 = open(f_csv_2, 'a')

    writer = csv.writer(csv_f, delimiter=' ')

    writer2 = csv.writer(csv_f_2, delimiter=' ')

    dicts = [{'words':read_dictonary(dictonary.path), 'number':dictonary.number_words} for dictonary in dictionaries]

    for d in docs:
        print(d.id)
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
                print('type err', type, '-', 'TXT, IMG, BKG')
                return

            if greyscale:
                img = img.convert('L')

            # A = 5
            # angle = np.random.randint(-1*A, A)

            # img = img.rotate(angle, resample=Image.BILINEAR)

            if size:
                img = resize(img, (size[1], size[0]))
            # img = img.resize((size[1],size[0]), PIL.Image.ANTIALIAS)

            fname = os.path.join(dir, 'imgs', 'type_'+str(d.id)+'-'+str(i + 1) + '_' + str(doc.num_records) + '.png')
            print(fname, 'num records', doc.num_records)
            img.save(fname)
            writer.writerow([fname, doc.num_records])
            writer2.writerow([fname, doc.num_records, d.id])


    csv_f.close()
    csv_f_2.close()


def merge_dataset_background(f_csv_argb, dir_back, dir, resize= (0.15,0.1),rotate=(-3,3),grayscale=True, size=None):
    from PIL import Image
    import PIL

    def get_files(dir):
        files = []
        for f in os.listdir(dir):

            ff = os.path.join(dir, f)

            files.append(ff)
        return files



    def merge_images(base, text, pos = (0, 0)):
        from .draw_document import watermark

        return watermark(base, text, pos)

    back_files = get_files(dir_back)

    f_csv = os.path.join(dir, 'gt.csv')
    f_csv_2 = os.path.join(dir, 'gt_2.csv')
    j = 0

    if not os.path.isdir(dir):
        print('NEW DIR: ', dir)
        os.makedirs(dir, exist_ok=True)
        os.mkdir(os.path.join(dir, 'imgs'))
        os.mkdir(os.path.join(dir, 'gt'))
        csv_f = open(f_csv, 'w')
        #csv_f_2 = open(f_csv_2, 'w')

    else:
        print('OLD DIR: ', dir)
        csv_f = open(f_csv, 'r')
        reader = csv.reader(csv_f, delimiter=' ')
        for _ in reader:
            j += 1
        csv_f.close()
        print('number', j)
        csv_f = open(f_csv, 'a')
        #csv_f_2 = open(f_csv_2, 'a')

    writer = csv.writer(csv_f, delimiter=' ')

    #writer2 = csv.writer(csv_f_2, delimiter=' ')

    with open(f_csv_argb, 'r') as csv_f:
        reader = csv.reader(csv_f, delimiter=' ')
        j = 0

        for row in reader:
            if len(row) >= 2 and os.path.isfile(row[0]):
                f_text, num = row[:2]
                num = int(num)

                a, b = os.path.split(f_text)

                key = b.split(':')[0]

                #imgs = back_dict[key]

                #print 'shuffle','list', len(imgs)

                f_back = None

                if j < len(back_files):
                    f_back = back_files[j]
                    j+=1
                else:
                    np.random.shuffle(back_files)
                    f_back = back_files[0]
                    j=1


                print('f_back', f_back)

                base = Image.open(f_back)

                text = Image.open(f_text)

                pos = (0,0)

                if resize:

                    back_w, back_h = base.size

                    width, height = text.size

                    if back_h < height:
                        print('back_ H W', back_h, back_w)
                        back_h = (back_h + height) / 2

                        back_w = max(back_w , width)

                        back_w +=np.random.randint(-50, 50)

                        print('back_ H w', back_h, back_w)

                        base = base.resize((back_w, back_h), PIL.Image.ANTIALIAS)


                    w = int(width*(resize[1]))
                    h = int(height * (resize[0]))
                    print(width, height)
                    width-=np.random.randint(0,w)
                    height-=np.random.randint(0,h)
                    print(width, height)

                    text = text.resize((width, height), PIL.Image.ANTIALIAS)

                    base_w, base_h =base.size

                    l = base_w - width
                    h = base_h - height

                    pos = (l,h)

                if rotate:
                    angle = np.random.randint(rotate[0], rotate[1])
                    print('angle', angle)
                    text = text.rotate(angle, resample=Image.NEAREST)


                img = merge_images(base, text, pos=pos)

                if grayscale:
                    img = img.convert('L')



                if size:
                    img = resize(img, (size[1], size[0]))

                N = b.split(':')[1].split('_')[0]

                fname = os.path.join(dir, 'imgs',key + ':' + N + '_' + str(num) + '.png')
                print('fname', fname, num)
                img.save(fname)



                writer.writerow([fname, num])

