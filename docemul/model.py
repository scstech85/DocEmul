import dexml
from dexml import fields


class Cell(dexml.Model):
    x = fields.Float()
    x_random = fields.Float()
    y_random = fields.Float()
    width = fields.Float()
    height = fields.Integer()
    #n_words = fields.Integer()
    probability = fields.Float()
    type_text = fields.Integer()
    type_font = fields.Integer()




class Line(dexml.Model):
    #id = fields.Integer(attrname="id")
    height = fields.Integer()
    text_min_height_prob = fields.Float()

    y_space_step = fields.Integer()
    cells = fields.List(Cell)
    type = fields.String()
    probability = fields.Float()
    repeat = fields.Integer()



class Lines(dexml.Model):

    textlines = fields.Dict(Line, key='id')


class TextLine(dexml.Model):

    text_line = fields.Integer()
    separator_line = fields.Integer()
    number_lines = fields.Integer()

class TextAndSeparatorLine(dexml.Model):
    composite_line = fields.List(Line)
    repeat_lines = fields.Integer()

    def __init__(self, repeat_lines=None):
        self.lines = []
        self.repeat_lines = repeat_lines

class GroupTextLine(dexml.Model):
    lines = fields.List(Line)
    probability = fields.Float()
    type = fields.String()
    def __init__(self, probability= 0.0, type='NULL'):
        self.probability = probability
        self.type = type
        self.real_lines = []

class Object(dexml.Model):
    command = fields.String()

    left = fields.Integer()
    top = fields.Integer()
    right = fields.Integer()
    bottom = fields.Integer()

    fill = fields.String()

    probability = fields.Float()


class Document(dexml.Model):
    id = fields.String(attrname='id')

    rotate = fields.Integer()

    max_append_records = fields.Integer()
    probability = fields.Float()
    height = fields.Integer()
    width = fields.Integer()

    corpus_top = fields.Integer()
    corpus_left = fields.Integer()

    corpus_width = fields.Integer()
    corpus_min_height = fields.Integer()
    corpus_max_height = fields.Integer()

    #record_type = fields.String()
    header = fields.List(GroupTextLine, tagname='header')
    record = fields.List(GroupTextLine, tagname='record')

    background = fields.List(Object, tagname='background')

class Dictonary(dexml.Model):
    path = fields.String()
    number_words = fields.Integer()

class Font(dexml.Model):
    path = fields.String()





class Documents(dexml.Model):
    documents = fields.List(Document)
    dictionaries = fields.List(Dictonary, tagname='dictonaries')
    fonts = fields.List(Font, tagname='fonts')

'''
l = Line(height=0,type = 'TextLine', y_space_step=40, probability=1)

l.cells.append(Cell(x=10, y_random=0.10, width=200, height=-1, n_words=5, probability=1))
l.cells.append(Cell(x=10, y_random=0.10, width=200, height=-1, n_words=5, probability=1))

s = Line(height=0, type = 'SeparatorLine', y_space_step=40, probability=1)

s.cells.append(Cell(x=10, y_random=0.10, width=200, height=-1, n_words=5, probability=1))
s.cells.append(Cell(x=10, y_random=0.10, width=200, height=-1, n_words=5, probability=1))


lines = Lines()

lines.textlines[1] = l
lines.textlines[2] = s

r =  lines.render()

document = Document(id=3, number_records=5, probability=1, height=3000, width=2400, corpus_top=100, corpus_left=100, corpus_width=1000, corpus_min_height = 300, corpus_max_height = 500, record_type="RAW")

document.record.append(Row(text_line=1,separator_line = 2))

docs = Documents()

docs.documents.append(document)

print r

l = Line( height=90, text_min_height_prob=0.9,
     y_space_step=70, type='TextLine', probability=0.9, repeat = 1)

l.cells.append(Cell(x=10, y_random=0.10, width=200, height=-1,  probability=1, x_random=0.10, type_text=0,type_font=1))
l.cells.append(Cell(x=10, y_random=0.10, width=200, height=-1,  probability=1, x_random=0.10, type_text=0,type_font=1))


textSepLines = TextAndSeparatorLine(repeat_lines=3)
textSepLines.composite_line.append(l)

g = GroupTextLine(probability=0.9, type="RAW")
g.lines.append(l)
g.lines.append(l)
#print g.render()

document = Document(id=3, max_append_records=15, number_records=5, probability=1, height=3000, width=2400, corpus_top=100, corpus_left=100, corpus_width=1000, corpus_min_height = 300, corpus_max_height = 500, rotate=5)
document.header.append(g)
document.record.append(g)
document.background.append(Object(command='line', left=0,top=0,right=0,bottom=0,fill='noise', probability=1))



docs = Documents()
docs.dictionaries.append(Dictonary(path='divina.txt',number_words=1))
docs.dictionaries.append(Dictonary(path='extra.txt',number_words=1))
docs.dictionaries.append(Dictonary(path='numbers.txt',number_words=1))

docs.fonts.append(Font(path='extra.txt'))

docs.documents.append(document)

#print docs.render()
'''


def read_xml(cla, file):
    f = open(file)
    txt = f.read()
    print txt
    return cla.parse(txt)


def read_docs(file_docs, file_lines):
    docs = read_xml(Documents, file_docs)
    lines = read_xml(Lines, file_lines)

    dataset = []
    for doc in docs.documents:
        lines_list = []
        sep_list = []
        for group_text in doc.record:
            for row in group_text:
                t_l = row.text_line
                s_l = row.separator_line

                if t_l != -1 or s_l != -1:

                    if t_l != -1:
                        lines_list.append(lines.textlines[t_l])
                    else:
                        lines_list.append(None)

                    if s_l != -1:
                        sep_list.append(lines.textlines[s_l])
                    else:
                        sep_list.append(None)

        dataset.append((doc, zip(lines_list, sep_list)))

    return dataset

def model_docs(file_docs):
    docs = read_xml(Documents, file_docs)
    documents = []

    for doc in docs.documents:
        for header_text in doc.header:
            for l in header_text.lines:
                rep = l.repeat
                l.repeat = 1
                lines = [l] * rep
                header_text.real_lines += lines

        for group_text in doc.record:
            for l in group_text.lines:
                rep = l.repeat
                l.repeat = 1
                lines = [l]*rep
                group_text.real_lines+=lines
        documents.append(doc)

    return documents, docs.dictionaries, docs.fonts

def read_dictonary(file):
    import re
    f = open(file)
    txt = f.read()


    wordList = re.sub("[^\w]", " ", txt).split()

    return wordList


