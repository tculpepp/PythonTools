# Python program to
# demonstrate merging of
# two files

import os

indexDir = 'tui/indexFiles'
os.chdir(indexDir)
root_index_files = ['CourseOverview.md',
                    'SignificanceOfCourse.md',
                    'LearningOutcomes.md',
                    'MaterialsAndBiblio.md',
                    'CourseDescription.md',
                    'NameAndCredit.md']



def create_index_file(file_list, out_dir):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    with open(out_dir+'/index.md', 'w') as outfile:
        for names in file_list:
            with open(names) as infile:
                outfile.write(infile.read())
            outfile.write("\n\n**********************************\n\n")
            os.remove(names)

# create_index_file(root_index_files, 'out')
# create_index_file(module_index_files, 'out'+modNum)

moduleRange = range(1,5)
for mod in moduleRange:
    modNum = str(mod)
    module_index_files = ['home'+modNum+'.md',
                    'objectives'+modNum+'.md',
                    'background'+modNum+'.md']
    create_index_file(module_index_files, 'out'+modNum)
# # Open file3 in write mode
# with open('rootIndex.md', 'w') as outfile:
  
#     # Iterate through list
#     for names in filenames:
  
#         # Open each file in read mode
#         with open(names) as infile:
  
#             # read the data from file1 and
#             # file2 and write it in file3
#             outfile.write(infile.read())
  
#         # Add '\n' to enter data of file2
#         # from next line
#         outfile.write("\n\n**********************************\n\n")