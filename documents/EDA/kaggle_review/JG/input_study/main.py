from urllib.request import urlopen
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser

url = "https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html"

result = urlopen(url)
html = result.read()
soup = BeautifulSoup(html, 'html.parser')

temp = soup.find_all('table')

p = parser.make2d(temp[0])
print(p)

import pandas as pd

df = pd.DataFrame(p[1:],columns = p[0])
print(df)

