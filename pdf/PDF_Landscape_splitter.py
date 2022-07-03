from PyPDF2 import PdfWriter, PdfReader
from pathlib import Path
import copy

# set working directory to current dir
directory = '.' 
pdfList=[]
# find all files that match 'FL*-mission.pdf
files = Path(directory).glob('FL*-mission.pdf')
# loop through the files and add them to a list
for file in files:
    pdfList.append(file)

# setup to read and crop the PDFs
for pdf in pdfList:
    reader = PdfReader(pdf)
    writer = PdfWriter()
    numPages = reader.getNumPages()
    filename = str(pdf)
    # if a unique filename is needed rather than overwriting the original
    # also change the variable in the write command below
    # outFileName = str(filename)[:-4]+"-Cropped"+str(filename)[-4:]
    # loop through each page in the pdf file and split it into two
    for page in range(0,numPages):
        left_page = reader.pages[page]
        right_page = copy.deepcopy(left_page)
        left_page.mediabox.upper_right = (
            left_page.mediabox.right,
            left_page.mediabox.top / 2,
        )
        right_page.mediabox.lower_left = (
            right_page.mediaBox.left,
            right_page.mediabox.top / 2,
        )
        writer.add_page(left_page)
        writer.add_page(right_page)
    # write out the file
    # change the variable filename to outFileName for a unique name
    with open(filename, "wb") as fp:
        writer.write(fp)