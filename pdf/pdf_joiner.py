from pathlib import Path
from PyPDF2 import PdfMerger

# set to the current directory
directory = '.'
fileList=[]
# find all files that match
files = Path(directory).glob('FL*.pdf')
# sort the filenames and add them to a list
for file in sorted(files):
    fileList.append(file)

merger = PdfMerger()
for pdf in fileList:
    merger.append(pdf)

merger.write("PPL_FL_consolidated.pdf")
merger.close()