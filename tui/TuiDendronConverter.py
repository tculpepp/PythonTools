##############################
# To Do:
#  clean footer from HTML pages
#  organize files for import
#  create module index file
#  dendron import command
#  copy assets into repo w/user confirmation
#  cleanup w/user confirmation
##############################
import os, subprocess
from bs4 import BeautifulSoup

#### Functions ####

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
course = input("Course Number: ")
assetsDir = "/assets/"+course+"/"
#  where the program will store files temporarily while modifying them
script_temp_dir = "tui/temp_working/"+course
os.makedirs(script_temp_dir, exist_ok=True)
# list of what directories to look for to convert to markdown (DirHumanNameString, DirName)
dir_list = [('Modules', modulesDir), ('Syllabus', syllabusDir)]

# here we start executing
for dir in dir_list:
    print('Converting '+dir[0]+' files...')
    for path, dir, files in os.walk(dir[1]):
        for name in files:
            if name.endswith('.html'):
                source_full_path = path+"/"+name
                with open(source_full_path) as fp:
                    soup = BeautifulSoup(fp, 'html.parser')
                href_converter(soup)
                html_cleaner(soup)
                with open(source_full_path, "w") as file:
                    file.write(str(soup))
                html_to_markdown(script_temp_dir)