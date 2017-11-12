import urllib2
import zipfile
import shutil
import os



def download_font(url, final_dir, ttf_name,ext='ttf', fname='tmp.zip',max_attempt=3):

    def download(url):
        attempts = 0

        while attempts < max_attempt:
            try:
                response = urllib2.urlopen(url, timeout = 5)
                content = response.read()
                f = open( fname, 'w' )
                f.write( content )
                f.close()
                break
            except urllib2.URLError as e:
                attempts += 1
                print type(e)
                return None
        return fname

    def unzip_move_delete(loc_name, final_path, directory_to_extract_to='tmp'):
        print 'unzip dir', loc_name
        zip_ref = zipfile.ZipFile(loc_name, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()

        files = [os.path.join(directory_to_extract_to,f) for f in os.listdir(directory_to_extract_to) if f.endswith(ext)]
        print 'list files'
        print files
        if len(files)>1:
            print 'ATTENTION!!!!!!',files[0]
        print 'move ttf file', files[0],
        shutil.copy2(files[0], final_path)

        shutil.rmtree(directory_to_extract_to)

    if not os.path.isdir(final_dir):
        os.makedirs(final_dir)

    loc_file = download(url)
    final_ttf = os.path.join(final_dir, ttf_name)
    print 'final file',
    unzip_move_delete(loc_file, final_ttf)
    print 'remove file', loc_file
    os.remove(loc_file)

#<Font path="handwritten2/A_Glitch_In_Time.ttf" />
#<Font path="handwritten2/Lovelt__.ttf" />
#<Font path="handwritten2/WankstabergBattles.ttf" />
#<Font path="handwritten2/SCRIPTIN.ttf" />
#<Font path="handwritten2/kevinwildfont.ttf" />
#<Font path="handwritten2/Mr_Fisherman_and_the_Shoemaker.ttf" />
#<Font path="handwritten2/FountainPen.ttf" />
#<Font path="handwritten2/Taken_by_Vultures_Demo.otf" />
#<Font path="handwritten2/Lemon_Tuesday.otf" />




directory = 'handwritten'

download_font('https://dl.dafont.com/dl/?f=a_glitch_in_time',directory, 'A_Glitch_In_Time.ttf')
download_font('https://dl.dafont.com/dl/?f=love_letter_tw',directory, 'Lovelt__.ttf')
download_font('https://dl.dafont.com/dl/?f=wankstaberg_battles',directory, 'WankstabergBattles.ttf')
download_font('https://dl.dafont.com/dl/?f=scriptina',directory, 'SCRIPTIN.ttf')
download_font('https://dl.dafont.com/dl/?f=kevinwild',directory, 'kevinwildfont.ttf')
download_font('https://dl.dafont.com/dl/?f=mr_fisherman_and_the_shoemaker',directory, 'Mr_Fisherman_and_the_Shoemaker.ttf')
download_font('https://dl.dafont.com/dl/?f=fountain_pen_frenzy',directory, 'FountainPen.ttf')
download_font('https://dl.dafont.com/dl/?f=taken_by_vultures',directory, 'Taken_by_Vultures_Demo.otf',ext='otf')
download_font('https://dl.dafont.com/dl/?f=lemon_tuesday',directory, 'Lemon_Tuesday.otf',ext='otf')

