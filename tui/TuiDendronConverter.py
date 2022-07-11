##############################
# To Do:
#  clean footer from HTML pages DONE
#  organize files for import IN PROCESS
#  create module index file DRAFTED
#  dendron import command
#  copy assets into repo w/user confirmation DRAFTED
#  cleanup w/user confirmation DRAFTED
#  unzipper DRAFTED
##############################
import os, subprocess, shutil
from bs4 import BeautifulSoup
from zipfile import ZipFile

#### Functions ####

def unzip_tui_file(filename)
    with ZipFile(filename, 'r') as zipObj:
    # Extract all the contents of zip file in different directory
        zipObj.extractall()
        # try to add a temp dir to capture everything into for ease later
    print('File is unzipped in temp folder') 

# this function recursively searches for a directory and then returns its path
# a directory can be supplied as an argument or it will default to the current dir
def directory_find(dirName, root='.'):
    for path, dirs, files in os.walk(root):
        if dirName in dirs:
            return os.path.join(path, dirName)

# this converts the internal document links to match the dendron file structure (assetsDir)
def href_converter(soup):
    for a in soup.findAll('a'):
        url_string = "" # can this be removed?
        # this loop replaces all local file links with contents of new_tag
        # start by ignoring all web links (href)
        try:
            if not str(a['href']).startswith('http'):
                url_string = str(a['href'])
                # strip extra parameters off URLs that have them
                if url_string.find('?') > 0:
                    url_index = url_string.find('?')
                    url_string = url_string[:url_index]
                # cut out everything that isn't the filename
                url_filename_index = url_string.rfind('/')+1
                new_tag = soup.new_tag("a")
                new_tag.string = str(a.string)
                new_tag['href'] = assetsDir+url_string[url_filename_index:]
                a.replace_with(new_tag)
        except:
            print('a strange tag was skipped')
    return(soup)

# This function standardizes the filenames and calls pandoc to convert html to MD
def html_to_markdown(out_dir):
    if not path.endswith('Syllabus'):
        out_name = name[4:-5]+name[3:4]+".md"
    else:
        out_name = name[:-5]+".md"
    out_full_path = out_dir+"/"+out_name
    print(out_name)
    os.system("pandoc --wrap=none --from html --to markdown_strict "+source_full_path+" -o "+out_full_path)

# this function removes the footer from the HTML doc (or anything else specified)
def html_cleaner(soup):
    for a in soup.findAll(class_="rowBottom"):
        a.decompose()
    return(soup)


# let's set some variables before we start executing
# find the modules and syllabus directories
# set the assets dir and make the script working dir
modulesDir = directory_find('Modules')
syllabusDir = directory_find('Syllabus')
zipFileName = input('Zip file path/name?: ')
course = input("Course Number: ")
os.mkdir('TuiConverterTemp')
os.chdir('TuiConverterTemp')


#  where the program will store files temporarily while modifying them
script_temp_dir = "tui/temp_working/"+course
os.makedirs(script_temp_dir, exist_ok=True)
# list of what directories to look for to convert to markdown (DirHumanNameString, DirName)
dir_list = [('Modules', modulesDir), ('Syllabus', syllabusDir)]
out_dir = 'out/'+course
assetsDir = "out/assets/"+course+"/"
# make output directory structure
i = 1
while (i <= 4):
    os.mkdirs(out_dir+'/mod'+i, exist_ok=True)
    i += 1
os.mkdirs(assetsDir, exist_ok=True)

# here we start executing
for dir in dir_list:
    # print('Converting '+dir[0]+' files...')
    # for path, dir, files in os.walk(dir[1]):
    print('Converting HTML to Markdown and moving asset files...')
    for path, dir, files in os.walk('.'):
        for name in files:
            source_full_path = path+"/"+name
            if name.endswith('.html'):
                with open(source_full_path) as fp:
                    soup = BeautifulSoup(fp, 'html.parser')
                href_converter(soup)
                html_cleaner(soup)
                with open(source_full_path, "w") as file:
                    file.write(str(soup))
                match name[-6:-5]:
                    case '1':
                        # shutil.copy2(source_full_path, out_dir+'/mod1/')
                        html_to_markdown(out_dir+'/mod1/')
                    case '2':
                        # shutil.copy2(source_full_path, out_dir+'/mod2/')
                        html_to_markdown(out_dir+'/mod2/')
                    case '3':
                        # shutil.copy2(source_full_path, out_dir+'/mod3/')
                        html_to_markdown(out_dir+'/mod3/')
                    case '4':
                        # shutil.copy2(source_full_path, out_dir+'/mod4/')
                        html_to_markdown(out_dir+'/mod4/')
                    case other:
                        print('no mod found')
                        html_to_markdown(out_dir)
                # html_to_markdown(script_temp_dir)
            else:
                shutil.copy2(source_full_path, assetsDir)          
print('HTML to Markdown conversion complete')
import_dendron = lower(input('Do you want to import into Dendron? (y/n): '))

if import_dendron == 'y':
    print('Importing into Dendron')
    #insert dendron import command here
    print('Dendron import complete')
else:
    print('Skipping Dendron Import')

cleanup_decision = lower(input('Cleanup temporary files? (y/n): '))

# # should this function be built into the initial save rather than after the fact?
# # this should move all the files to the correct directory structure for import
# for path, dir, file in os.walk(script_temp_dir):
#     source_full_path = path+"/"+name
#     match file[3:4]:
#         case '1':
#             shutil.copy2(source_full_path, out_dir+'/mod1/' )
#         case '2':
#             shutil.copy2(source_full_path, out_dir+'/mod2/' )
#         case '3':
#             shutil.copy2(source_full_path, out_dir+'/mod3/' )
#         case '4':
#             shutil.copy2(source_full_path, out_dir+'/mod4/' )
#         case other:
#             print('no mod found')
# print ('Files moved into directory structure')

