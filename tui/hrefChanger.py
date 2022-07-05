from bs4 import BeautifulSoup

with open("./tui/CSC330/CSC330/Syllabus/MaterialsAndBiblio.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
# soup = BeautifulSoup('./tui/CSC330/CSC330/Syllabus/MaterialsAndBiblio.html')
for a in soup.findAll('a'):
  a['href'] = a['href'].replace("youtube", "MYSITE")

result = str(soup)
print(result)