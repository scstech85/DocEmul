import os

def get_files(dir, ext='jpg'):
    for f in os.listdir(dir):
        f_name = os.path.join(dir, f)

        if os.path.isfile(f_name) and f.split('.')[1] == ext:
            print f
            yield f_name, f

