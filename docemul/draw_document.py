from model import Document, Lines, read_xml
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw,ImageEnhance

import numpy as np




import os

def confirm(prob):
    val = np.random.random()
    if val <= prob:
        return True
    return False

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))

    layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)


class DrawCell:
    def __init__(self,left,top,right,bottom,text_height, index_dict, index_font):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.text_height = text_height
        self.type_dictonary = index_dict
        self.type_font = index_font
        #self.n_words = n_words

class DrawRecord:

    def __init__(self):
        self.cells = list()
        self.lines = list()

    def get_bounds(self):
        loc_left, loc_top, loc_right, loc_bottom = None
        for c in self.cells:
            if loc_left is None:
                loc_left, loc_top, loc_right, loc_bottom = (c.left,c.top,c.right,c.bottom)
            else:
                loc_left = min(loc_left, c.left)
                loc_top = min(loc_top, c.top)
                loc_right = max(loc_right, c.right)
                loc_bottom = max(loc_bottom, c.bottom)

        return loc_left, loc_top, loc_right, loc_bottom

class DrawDocument:

    def __init__(self, document, sampler, dicts, fonts):
        self.width, self.height = (document.width, document.height)
        #self.record_type = document.record_type
        self.dicts = dicts
        self.fonts = fonts

        self.background_objs = document.background


        self.rotate = document.rotate

        self.sampler = sampler

        self.top = self.corpus_top = document.corpus_top

        self.corpus_left = document.corpus_left
        self.corpus_width = document.corpus_width
        self.corpus_min_height = document.corpus_min_height
        self.corpus_max_height = document.corpus_max_height

        self.records = []

        print 'document.max_append_records', document.max_append_records

        check_to_fill = np.random.randint(0, document.max_append_records) if document.max_append_records > 0 else 0

        header, self.corpus_top = self.__draw_record__(document.header, self.corpus_top)

        self.records.append(header)

        num_records = 0

        while (True):

            record, corpus_top = self.__draw_record__(document.record, self.corpus_top)
            loc_width = corpus_top - self.top

            print '--', corpus_top, loc_width, corpus_top - self.corpus_top, '::', self.corpus_min_height, self.corpus_max_height

            if loc_width < self.corpus_max_height:
                self.records.append(record)

                print 'record', num_records + 1, 'append!!!'

                self.corpus_top = corpus_top

                num_records += 1

            if loc_width >= self.corpus_min_height:
                check_to_fill -= 1
                if check_to_fill <= 0:
                    break

        self.num_records = num_records

        print 'final num records', self.num_records



    def __draw_record__(self, groups, corpus_top):

        record = DrawRecord()
        print 'num groups', len(groups)

        for g, textgroup in enumerate(groups):
            print 'group', g+1

            if confirm(textgroup.probability):

                print 'num lines', len(textgroup.real_lines)
                for l, line in enumerate(textgroup.real_lines):
                    print 'line', l+1
                    if line.type == 'TextLine':

                        if confirm(line.probability):
                            loc_new_top = self.__append_text__(corpus_top, line, record)
                            corpus_top = loc_new_top

                        elif textgroup.type=='FULL':
                            break

                    elif line.type == 'SeparatorLine':
                        y_step = np.random.randint(int(line.text_min_height_prob*line.y_space_step),line.y_space_step)
                        corpus_top += y_step

        return record, corpus_top

    def __append_text__(self, corpus_top, line, record):
        record.lines.append((corpus_top, corpus_top + line.height))
        print 'num cells', len(line.cells)
        text_min_height_prob = line.text_min_height_prob

        for cell in line.cells:
            index_dict = cell.type_text
            index_font = cell.type_font

            cell_x = int(cell.x * self.corpus_width)
            cell_width = int(cell.width*self.corpus_width)

            c, d = map(int, (cell.x_random * cell_width * -1, cell.x_random * cell_width * 1))

            if c != d:
                x_step = np.random.randint(c, d)

                cell_x += x_step

            print 'cell_x', cell_x, 'cell_width', cell_width
            loc_top = corpus_top

            loc_left = self.corpus_left + cell_x
            loc_right = loc_left + cell_width

            loc_height = line.height if cell.height == -1 else line.height

            a,b = map(int, (cell.y_random * loc_height * -1, cell.y_random * loc_height * 1))

            if a!= b:
                y_step = np.random.randint(a,b)

                loc_top +=y_step

            loc_bottom = loc_top + loc_height

            #n_words = cell.n_words
            prob = cell.probability


            if confirm(prob):
                text_height = loc_height
                if text_min_height_prob < 1:
                    text_height = np.random.randint(int(text_min_height_prob * loc_height) ,  loc_height)


                record.cells.append(DrawCell(loc_left, loc_top, loc_right, loc_bottom, text_height, index_dict, index_font))

        #self.top+=line.y_space_step

        return corpus_top + line.y_space_step

    def image(self):
        img = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))


        for record in self.records:
            for line_top, line_bottom in record.lines:
                draw = ImageDraw.Draw(img)
                draw.rectangle([0, line_top, self.width, line_bottom], fill=(0, 0, 255, 255))

            for cell in record.cells:

                draw = ImageDraw.Draw(img)
                draw.rectangle([cell.left, cell.top, cell.right, cell.bottom],outline=(255,0,0,255))


        return img

    def text(self):
        def create_row(dictonary, number_words, cell, font, max_step=1,min_lenght_first_word = 3):



            if number_words<=0:
                number_words = np.inf

            print 'number words', number_words


            np.random.shuffle(dictonary)

            width = cell.right - cell.left

            phrase = ''

            j = max_step

            o = iter(dictonary)
            i = 0
            while(True):
                word = o.next()

                # se siamo alla prima parola rispetto ad aspettarmene almeno 2, allora controllo la lunghezza
                if i == 0 and len(word)<min_lenght_first_word and number_words>1:
                    continue

                w, h = draw.textsize(phrase+word, font=font)

                print 'text dimension', w, h

                if i == 0 and w>width:
                    continue

                if w<=width:
                    phrase+=(word + ' ')
                    #if i == 0 and len(word)>min_lenght_first_word:
                    i+=1

                    j = max_step
                else:
                    j-=1

                if j <= 0 or i==number_words:
                    break

            if len(phrase)<min_lenght_first_word:
                print 'error phrase', len(phrase)
            print 'phrase', phrase

            return phrase

        def draw_text(phrase, cell, font):
            draw.text((cell.left, cell.top), phrase, (0, 0, 0), font=font)

        img = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)



        print 'num_records', len(self.records)
        #index = 0
        for i, record in enumerate(self.records):
            print 'record', i+1
            print 'num_cells', len(record.cells)
            for cell in record.cells:


                point_pixel = 16

                text_height = int(cell.text_height / float(point_pixel) * 12)

                #fonts_path = 'handwritten2', text_font = "FountainPen.ttf"

                font_path = self.fonts[cell.type_font].path


                font = ImageFont.truetype(font_path, text_height)

                #draw.rectangle([cell.left, cell.top, cell.right, cell.bottom], outline=(0, 0, 0, 255))

                #(cell.left + cell.right)/2

                #cY = (cell.top + cell.bottom)/2

                #text = dictonary[index:index+cell.n_words]
                print 'cell', cell.left, cell.top, cell.right, cell.bottom, 'T H', text_height

                dictonary = self.dicts[cell.type_dictonary]

                phrase = create_row(dictonary['words'],dictonary['number'], cell, font)

                draw_text(phrase, cell, font)

                #index += cell.n_words
        if self.rotate > 0:
            angle = (np.random.random()*self.rotate * 2) - self.rotate
            #angle = np.random.randint(self.rotate*(-1), self.rotate)

            img = img.rotate(angle, resample=Image.BILINEAR)
        return img

    def create_background(self,make_lines=False):
        background = self.sampler.sample_bgimage((self.height, self.width))
        img = Image.fromarray(background)
        if make_lines:
            img = self._create_background(img)
        return img

    def _create_background(self,img):

        pillow_types = ['line','rectangle']
        for object in self.background_objs:
            if object.command in pillow_types and confirm(object.probability):
                draw = ImageDraw.Draw(img)
                fill = str(object.fill)

                if str(object.command) == 'line':

                    draw.line((object.left,object.top, object.right,object.bottom),fill=fill)
                    #draw.line((0, im.size[1], im.size[0], 0), fill=128)
                elif str(object.command) == 'rectangle':
                    if fill.startswith('noise'):
                        pxl = float(fill.split('_')[1])
                        w = object.right - object.left
                        h = object.bottom - object.top
                        M = np.random.rand(h, w)
                        M = (M>pxl).astype(np.uint8)

                        im = np.array(img)
                        if im.ndim> 2:
                            im[object.top:object.bottom, object.left:object.right, 3] = M * 255
                            M_ = np.invert(M)
                            for j in range(im.shape[2]-1):
                                im[object.top:object.bottom,object.left:object.right,j]= M_*255
                        else:
                            im[object.top:object.bottom, object.left:object.right] *= M
                        img = Image.fromarray(im)
                    else:
                        draw.rectangle([object.left, object.top, object.right, object.bottom], fill=fill, outline=fill)



        return img

    def create_image(self):
        background = self.sampler.sample_bgimage((self.height, self.width))
        img = Image.fromarray(background)

        img_base = self.create_background(img)
        #img_base.show()
        img_text = self.text()

        return watermark(img_base, img_text, (0,0))

    def create_only_text(self):

        img_base = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        img_base = self._create_background(img_base)

        img_text = self.text()


        return watermark(img_base, img_text, (0, 0))

    def __append_separator__(self, corpus_top,line):
        print 'no method'
        pass