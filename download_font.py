import urllib
import urllib.request
import zipfile
import shutil
import os


def download_font(url, final_dir, ttf_name,ext='ttf', fname='tmp.zip',max_attempt=3):

    def download(url):
        attempts = 0

        while attempts < max_attempt:
            try:
                response = urllib.request.urlopen(url, timeout = 5)
                content = response.read()
                f = open( fname, 'wb' )
                f.write( content )
                f.close()
                break
            except Exception as e:
                attempts += 1
                print(type(e))
                raise
                # return None
        return fname

    def unzip_move_delete(loc_name, final_path, directory_to_extract_to='tmp'):
        print('unzip dir', loc_name)
        zip_ref = zipfile.ZipFile(loc_name, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()

        files = [os.path.join(directory_to_extract_to,f) for f in os.listdir(directory_to_extract_to) if f.lower().endswith(ext)]
        print('list files')
        print(files)
        if len(files)>1:
            print('ATTENTION!!!!!!',files[0])
        print('move ttf file', files[0],)
        shutil.copy2(files[0], final_path)

        shutil.rmtree(directory_to_extract_to)
        return

    if not os.path.isdir(final_dir):
        os.makedirs(final_dir, exist_ok=True)

    loc_file = download(url)
    final_ttf = os.path.join(final_dir, ttf_name)
    print('final file', final_ttf)
    unzip_move_delete(loc_file, final_ttf)
    print('remove file', loc_file)
    os.remove(loc_file)
    return

#<Font path="fonts2/A_Glitch_In_Time.ttf" />
#<Font path="fonts2/Lovelt__.ttf" />
#<Font path="fonts2/WankstabergBattles.ttf" />
#<Font path="fonts2/SCRIPTIN.ttf" />
#<Font path="fonts2/kevinwildfont.ttf" />
#<Font path="fonts2/Mr_Fisherman_and_the_Shoemaker.ttf" />
#<Font path="fonts2/FountainPen.ttf" />
#<Font path="fonts2/Taken_by_Vultures_Demo.otf" />
#<Font path="fonts2/Lemon_Tuesday.otf" />




directory = 'fonts'

# Handwritten fonts
download_font('https://dl.dafont.com/dl/?f=a_glitch_in_time',directory, 'A_Glitch_In_Time.ttf')
download_font('https://dl.dafont.com/dl/?f=love_letter_tw',directory, 'Lovelt__.ttf')
download_font('https://dl.dafont.com/dl/?f=wankstaberg_battles',directory, 'WankstabergBattles.ttf')
download_font('https://dl.dafont.com/dl/?f=scriptina',directory, 'SCRIPTIN.ttf')
download_font('https://dl.dafont.com/dl/?f=kevinwild',directory, 'kevinwildfont.ttf')
download_font('https://dl.dafont.com/dl/?f=mr_fisherman_and_the_shoemaker',directory, 'Mr_Fisherman_and_the_Shoemaker.ttf')
download_font('https://dl.dafont.com/dl/?f=fountain_pen_frenzy',directory, 'FountainPen.ttf')
download_font('https://dl.dafont.com/dl/?f=taken_by_vultures',directory, 'Taken_by_Vultures_Demo.otf',ext='otf')
download_font('https://dl.dafont.com/dl/?f=lemon_tuesday',directory, 'Lemon_Tuesday.otf',ext='otf')

# Printing fonts
# download_font('https://www.cufonfonts.com/download/font/arial',directory, 'Arial.ttf')
