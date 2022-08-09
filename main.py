from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from jinja2 import PackageLoader, select_autoescape
import datetime
import re
import pandas as pd
import pprint
from collections import defaultdict
import argparse
import os

WINERY_FOUNDATION_YEAR = 1920


def add_correct_suffix(number):
    suffix = ''
    number = number % 100
    if number > 19:
        number = number % 10
    if number == 1:
        suffix = 'год'
    elif 2 <= number <= 4:
        suffix = 'года'
    else:
        suffix = 'лет' 
    return suffix        
    

if __name__ == '__main__':
    
    default_path = os.path.abspath(os.curdir)+'\wine.xlsx'
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default=default_path)    
    user_path = parser.parse_args().path
    wine_df = pd.read_excel(user_path, na_values='').fillna('')
    wine_categories = list(set(wine_df['Категория']))

    beverages = defaultdict(list, [])

    beverage_description = [column for column in wine_df.columns
                            if column != 'Категория']
    
    for row in range(len(wine_df)):
        beverages[wine_df.loc[row, 'Категория']]\
            .append(wine_df.loc[row, beverage_description])
        
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        age=datetime.datetime.now().year-WINERY_FOUNDATION_YEAR,
        form=add_correct_suffix(datetime.datetime.now().year -
                                WINERY_FOUNDATION_YEAR),
        beverages=beverages
        )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

