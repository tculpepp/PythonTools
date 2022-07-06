# this code finds all the links in an html file then parses them for filenames
# once the filename is extracted, a new local (i.e. assets/CSC330/filename) can be built
# TO DO:
# dendron link format: /assets/CSC330/filename.ext
# how to write the html file back out
# clean this mess up!

from bs4 import BeautifulSoup

with open("./tui/CSC330/CSC330/Syllabus/MaterialsAndBiblio.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
working_dir = "/assets/CSC330/"
for a in soup.findAll(attrs={"class" : "linkBottom"}):
    print(a)
    a.decompose()
result = str(soup)
print(result)

#     # this loop replaces all local file links with contents of new_tag
#     # start by ignoring all web links
#   if not str(a['href']).startswith('http'):
#     url_string = str(a['href'])
#     # strip extra parameters off URLs that have them
#     if url_string.find('?') > 0:
#         url_index = url_string.find('?')
#         url_string = url_string[:url_index]
#     # cut out everything that isn't the filename
#     url_filename_index = url_string.rfind('/')+1
#     new_tag = soup.new_tag("a")
#     new_tag.string = str(a.string)

#     new_tag['href'] = working_dir+url_string[url_filename_index:]
#     a.replace_with(new_tag)

#     print(new_tag['href'])
#     # print(a['href'])
#     print('*************************')

# # result = str(soup)
# # print(result)
# with open('corected_href.html', "w") as file:
#     file.write(str(soup))

# def href_converter(html_file):
#     with open(html_file) as fp:
#         soup = BeautifulSoup(fp, 'html.parser')
#     for a in soup.findAll('a'):
#         print(a)
#         url_string = ""
#         print(url_string)
#         # this loop replaces all local file links with contents of new_tag
#         # start by ignoring all web links
#         if not str(a['href']).startswith('http'):
#             url_string = str(a['href'])
#             print(url_string)
#             # strip extra parameters off URLs that have them
#             if url_string.find('?') > 0:
#                 url_index = url_string.find('?')
#                 url_string = url_string[:url_index]
#             # cut out everything that isn't the filename
#             url_filename_index = url_string.rfind('/')+1
#             new_tag = soup.new_tag("a")
#             new_tag.string = str(a.string)
#             new_tag['href'] = assetsDir+url_string[url_filename_index:]
#             a.replace_with(new_tag)
#     #  overwrite the original file with the changes
#     with open(html_file+'_temp.html', "w") as file:
#         file.write(str(soup))
# assetsDir = "/assets/CSC330"
# href_converter("./tui/CSC330/CSC330/Modules/Module4/Mod4Background.html")