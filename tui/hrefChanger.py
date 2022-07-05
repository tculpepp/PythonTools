from bs4 import BeautifulSoup
import urllib.parse

with open("./tui/CSC330/CSC330/Syllabus/MaterialsAndBiblio.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
# soup = BeautifulSoup('./tui/CSC330/CSC330/Syllabus/MaterialsAndBiblio.html')
for a in soup.findAll('a'):
  a['href'] = a['href'].replace("youtube", "MYSITE")

# this loop replaces all local file links with contents of new_tag
  if not str(a['href']).startswith('http'):
    url_filename_index = str(a['href']).rfind('/')+1
    print(url_filename_index)
    new_tag = soup.new_tag("a")
    new_tag.string = str(a.string)
    # this is attempting to combine the existing filename with the new local URL
    # doesn't work for "content/enforced/..." urls
    new_tag['href'] = "local/directory/"+str(a['href'])[-url_filename_index:]
    a.replace_with(new_tag)

    print(new_tag['href'])
    print(a['href'])

result = str(soup)
# print(result)