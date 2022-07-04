import os

#  this function recursively searches for a directory and then returns its path
def directory_find(dirName, root='.'):
    for path, dirs, files in os.walk(root):
        if dirName in dirs:
            return os.path.join(path, dirName)

#  here we call the function and then change to that directory
modulesDir = directory_find('Modules')
print(modulesDir)
print(os.getcwd())
os.chdir(modulesDir)
print(os.getcwd())
            