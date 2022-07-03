from pathlib import Path
directory = '.'
fileList=[]
files = Path(directory).glob('FL*.pdf')
for file in sorted(files):
    fileList.append(file)
    print(file)
    # filename = file
    # print(str(filename)[:-4]+"-temp"+str(filename)[-4:])

print(fileList)