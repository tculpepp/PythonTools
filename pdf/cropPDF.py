from PyPDF2 import PdfWriter, PdfReader
from pathlib import Path
import copy

reader = PdfReader("./pdf/FL01-mission.pdf")
writer = PdfWriter()
numPages = reader.getNumPages()

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

# add page 1 from reader to output document, unchanged:
# writer.add_page(reader.pages[0])

# # add page 3 from reader, but crop it to half size:
# page2 = reader.pages[1]
# right_side = copy.deepcopy(page2) # get a pre-copy of the page for the other side
# page2.mediabox.upper_right = (
#     page2.mediabox.right,
#     page2.mediabox.top / 2,
# )

# page3 = right_side
# page3.mediabox.lower_left = (
#     page3.mediaBox.left,
#     page3.mediabox.top / 2,
# )
# print(page2.mediaBox)
# print(page3.mediaBox)
# writer.add_page(page2)
# writer.add_page(page3)


# add some Javascript to launch the print window on opening this PDF.
# the password dialog may prevent the print dialog from being shown,
# comment the the encription lines, if that's the case, to try this out:
# writer.add_js("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")

# write to document-output.pdf
with open("PyPDF2-output.pdf", "wb") as fp:
    writer.write(fp)