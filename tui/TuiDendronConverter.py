import os, subprocess

# this function recursively searches for a directory and then returns its path
# a directory can be supplied as an argument or it will default to the current dir
def directory_find(dirName, root='.'):
    for path, dirs, files in os.walk(root):
        if dirName in dirs:
            return os.path.join(path, dirName)
# find the modules directory
modulesDir = directory_find('Modules')

# make a temp working dir
script_temp_dir = "./tui/temp_working"
os.system("mkdir "+script_temp_dir)

def html_to_markdown(extension, out_dir):
    for name in files:
        if name.endswith(extension):
            out_name = name[4:-5]+name[3:4]+".md"
            source_full_path = path+"/"+name
            out_full_path = out_dir+"/"+out_name
            print('Converting '+out_name)
            os.system("pandoc --wrap=none --from html --to markdown_strict "+source_full_path+" -o "+out_full_path)

for path, dir, files in os.walk(modulesDir):
    html_to_markdown('.html', script_temp_dir)


# # this uses os.walk to recursively loop through the dir and find files with ____ extension
# for path, dir, files in os.walk(modulesDir):
#     for name in files:
#         # this renames the files and converts them to markdown with pandoc
#         if name.endswith('.html'):
#             # this complex sequence chops up the file name to match the structure
#             out_name = name[4:-5]+name[3:4]+".md"
#             print(new_name)
#             full_file_path=path+"/"+name
#             full_new_path = script_temp_dir+"/"+out_name
#             os.system("pandoc --wrap=none --from html --to markdown_strict "+full_file_path+" -o "+full_new_path)
