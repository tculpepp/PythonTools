##############################
# To Do:
#  dendron import command - doesn't create index file 
#  copy assets into repo w/user confirmation DRAFTED
#  generally clean things up
##############################

##############################
# Instructions
# Just run the command and follow the prompts
# location doesn't matter
# directory for the zip file is RELATIVE
# been copying to zip into the local dir to run from there
##############################

from operator import mod
import os, shutil
from bs4 import BeautifulSoup
from zipfile import ZipFile
# import youtubePlaylistmaker

#### Functions ####

def unzip_tui_file(filename, extract_dir):
    with ZipFile('../'+filename, 'r') as zipObj:
    # Extract all the contents of zip file in different directory
        zipObj.extractall(path = extract_dir)
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
    print(out_dir)
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

#  this function builds the index files for each section
def create_index_file(file_list, out_dir):
    cwd = os.getcwd()
    print(cwd)
    print(out_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    with open(out_dir+'/index.md', 'w') as outfile:
        for names in file_list:
            try:
                name_full_path = out_dir+'/'+names
                print(name_full_path)
                with open(name_full_path) as infile:
                    outfile.write(infile.read())
                outfile.write("\n\n**********************************\n\n")
                os.remove(name_full_path)
            except:
                print(names+" was not found so it was skipped.")

####### main execution starts here ##########

# make the working dir and move into it
workingDir = 'TuiConverterTemp'
os.mkdir(workingDir)
os.chdir(workingDir)

#  get the zip name and extract it
zipFileName = input('Zip file path/name?: ')
extractedDir = 'extracted'
unzip_tui_file(zipFileName, extractedDir)

#  set some directories
course = input("Course Number: ")
out_dir = 'out/school/'+course
assetsDir = "out/school/assets/"+course+"/"
script_temp_dir = "temp_working/"+course

os.makedirs(script_temp_dir, exist_ok=True)

# make output directory structure
i = 1
while (i <= 4):
    os.makedirs(out_dir+'/mod'+str(i), exist_ok=True)
    i += 1
os.makedirs(assetsDir, exist_ok=True)

print('Converting HTML to Markdown and moving asset files...')
for path, dir, files in os.walk(extractedDir):
    if "out" in dir: # this little IF causes the 'out' directory to be excluded
        dir.remove("out") 
    for name in files:
        source_full_path = path+"/"+name
        if name.endswith('.html'):
            with open(source_full_path) as fp:
                soup = BeautifulSoup(fp, 'html.parser')
            href_converter(soup)
            html_cleaner(soup)
            with open(source_full_path, "w") as file:
                file.write(str(soup))
            file_mod_num = name[3:4]
            if file_mod_num.isnumeric():
                html_to_markdown(out_dir+'/mod'+file_mod_num+'/')
            else:
                print('Syllabus File')
                html_to_markdown(out_dir)
        else:
            shutil.copy2(source_full_path, assetsDir)          
print('HTML to Markdown conversion complete')
shutil.rmtree('temp_working')

root_index_files = ['CourseOverview.md',
                    'SignificanceOfCourse.md',
                    'LearningOutcomes.md',
                    'MaterialsAndBiblio.md',
                    'CourseDescription.md',
                    'NameAndCredit.md']
create_index_file(root_index_files, './'+out_dir)

# create the module index files
moduleRange = range(1,5)
for mod in moduleRange:
    modNum = str(mod)
    mod_out_dir = out_dir+'/mod'+modNum
    module_index_files = ['home'+modNum+'.md',
                    'objectives'+modNum+'.md',
                    'background'+modNum+'.md']
    create_index_file(module_index_files, mod_out_dir)


import_dendron = input('Do you want to import into Dendron? (y/n): ').lower()

if import_dendron == 'y':
    dendron_src = os.getcwd()+"/out"#+"/"+out_dir
    print(dendron_src)
    print('Importing into Dendron')
    os.system("dendron importPod --podId dendron.markdown --wsRoot '/Users/tculpepp/Documents/repos/dendron' --config src="+dendron_src+",vaultName:vault,indexName:index.md,noAddUUID:true")
    print('Dendron import complete')
else:
    print('Skipping Dendron Import')

cleanup_decision = input('Cleanup temporary files? (y/n): ').lower()
if cleanup_decision == 'y':
    shutil.rmtree(extractedDir)
    os.chdir('..')
    shutil.rmtree(workingDir)
    print('temporary files deleted')
print('script complete.')
exit()
