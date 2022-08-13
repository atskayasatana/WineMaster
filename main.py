import argparse
import datetime
import pandas as pd
import os

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

WINERY_FOUNDATION_YEAR = 1920


def set_noun_to_num(number):
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
    
    default_path = Path.cwd().joinpath('wine.xlsx')
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default=default_path)    
    user_path = parser.parse_args().path
    wine_df = pd.read_excel(user_path, na_values=None, keep_default_na=False)\
                .to_dict(orient='records')
    beverages = defaultdict(list)
    for wine in wine_df:
        beverages[wine['Категория']].append(wine)
        
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        age=datetime.datetime.now().year-WINERY_FOUNDATION_YEAR,
        form=set_noun_to_num(datetime.datetime.now().year -
                          WINERY_FOUNDATION_YEAR),
        beverages=beverages
        )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
