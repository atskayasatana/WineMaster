from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from jinja2 import PackageLoader, select_autoescape
import datetime
import re
import pandas as pd
import pprint
from collections import defaultdict


def end_form(number):
    end_form = ''
    num_string =str(number)
    num_string_len = len(num_string)
    if num_string_len < 2:
        if int(num_string) in [0, 5, 6, 7, 8, 9]:
            end_form = 'лет'
        elif int(num_string) in [2, 3, 4]:
            end_form = 'года'
        elif int(num_string) == 1:
            end_form = 'год'
    else:
        end_numbers = num_string[-2:]
        if re.match(r'^[^1]1{1}$', end_numbers):
            end_form = "год"
        if re.match(r'^[^1][2-4]{1}$', end_numbers):
            end_form = "года"   
        if re.match(r'^1{1}[0-9]{1}$', end_numbers):
            end_form = "лет"
        if re.match(r'^[^1][5-9]{1}$''', end_numbers):
            end_form = "лет"
    return end_form        
    
    
wine_df = pd.read_excel('wine.xlsx', na_values='').fillna('')
wine_categories = list(set(wine_df['Категория']))

wine_dict = defaultdict(list, [])

columns_for_value = ['Название', 'Сорт', 'Цена', 'Картинка', 'Акция']
for i in range(len(wine_df)):
    wine_dict[wine_df.loc[i, 'Категория']]\
        .append(wine_df.loc[i, columns_for_value])
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')
rendered_page = template.render(
    age=datetime.datetime.now().year-1920,
    form=end_form(datetime.datetime.now().year-1920),
    num_of_wine_categories=len(wine_categories),
    wine_categories=wine_categories,
    wine_dict=wine_dict 
    )
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

