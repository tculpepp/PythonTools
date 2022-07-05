# this code finds all the links in an html file then parses them for filenames
# once the filename is extracted, a new local (i.e. assets/CSC330/filename) can be built
# TO DO:
# determine proper format for dendron internal links
# how to write the html file back out
# clean this mess up!

from bs4 import BeautifulSoup

with open("./tui/CSC330/CSC330/Syllabus/MaterialsAndBiblio.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

for a in soup.findAll('a'):

    # this loop replaces all local file links with contents of new_tag
    # start by ignoring all web links
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

    new_tag['href'] = "local/directory/"+url_string[url_filename_index:]
    a.replace_with(new_tag)

    print(new_tag['href'])
    # print(a['href'])
    print('*************************')

result = str(soup)
# print(result)