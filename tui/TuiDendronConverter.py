import os, subprocess

# this function recursively searches for a directory and then returns its path
# a directory can be supplied as an argument or it will default to the current dir
def directory_find(dirName, root='.'):
    for path, dirs, files in os.walk(root):
        if dirName in dirs:
            return os.path.join(path, dirName)
# find the modules directory
modulesDir = directory_find('Modules')
syllabusDir = directory_find('Syllabus')

# make a temp working dir
script_temp_dir = "./tui/temp_working"
os.system("mkdir "+script_temp_dir)

def html_to_markdown(extension, out_dir):
    for name in files:
        if name.endswith(extension):
            if not path.endswith('Syllabus'):
                out_name = name[4:-5]+name[3:4]+".md"
            else:
                out_name = name[:-5]+".md"
            source_full_path = path+"/"+name
            out_full_path = out_dir+"/"+out_name
            print(out_name)
            os.system("pandoc --wrap=none --from html --to markdown_strict "+source_full_path+" -o "+out_full_path)

print('Converting Module Files...')
for path, dir, files in os.walk(modulesDir):
    html_to_markdown('.html', script_temp_dir)

print('Converting Syllabus Files...')
for path, dir, files in os.walk(syllabusDir):
    html_to_markdown('.html', script_temp_dir)
