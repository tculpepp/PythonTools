import os, subprocess
from bs4 import BeautifulSoup

# this function recursively searches for a directory and then returns its path
# a directory can be supplied as an argument or it will default to the current dir
def directory_find(dirName, root='.'):
    for path, dirs, files in os.walk(root):
        if dirName in dirs:
            return os.path.join(path, dirName)
# find the modules and syllabus directories
# set the assets dir and make the script working dir
modulesDir = directory_find('Modules')
syllabusDir = directory_find('Syllabus')
course = input("Course Number: ")
assetsDir = "/assets/"+course+"/"
script_temp_dir = "tui/temp_working/"+course
os.makedirs(script_temp_dir, exist_ok=True)

def href_converter(html_file):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    for a in soup.findAll('a'):
        url_string = ""
        # this loop replaces all local file links with contents of new_tag
        # start by ignoring all web links
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
        #  overwrite the original file with the changes
        with open(html_file, "w") as file:
            file.write(str(soup))

def html_to_markdown(out_dir):
    if not path.endswith('Syllabus'):
        out_name = name[4:-5]+name[3:4]+".md"
    else:
        out_name = name[:-5]+".md"
    # source_full_path = path+"/"+name
    out_full_path = out_dir+"/"+out_name
    print(out_name)
    # href_converter(source_full_path)
    
    os.system("pandoc --wrap=none --from html --to markdown_strict "+source_full_path+" -o "+out_full_path)

dir_list = [('Modules', modulesDir), ('Syllabus', syllabusDir)]

for dir in dir_list:
    print('Converting '+dir[0]+' files...')
    for path, dir, files in os.walk(dir[1]):
        for name in files:
            if name.endswith('.html'):
                source_full_path = path+"/"+name
                href_converter(source_full_path)
                html_to_markdown(script_temp_dir)
