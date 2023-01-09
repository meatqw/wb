import csv
import requests
from bs4 import BeautifulSoup

# link example 
# https://basket-03.wb.ru/vol322/part32297/32297690/info/ru/card.json
# fields
# - Состав
# - Вес с упаковкой(кг)
# - Тип плетения постельного белья
# - Размер натяжной простыни

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}


def get_data_from_csv():
    data = []
    
    with open('data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            
            data.append(row)
    
    return data
   
def add_to_csv(data, olddata, filename):
    composition = data['composition']
    if len(composition) < 3:
        while len(composition) != 3:
            composition.append(0)
            
    weight = data['weight']
    type = data['type']
    if len(type) < 4:
        while len(type) != 4:
            type.append(0)
            
    size = data['size']
    if len(size) < 3:
        while len(size) != 3:
            size.append(0)
            
    
    for i in composition:
        olddata.append(i)
    
    for i in weight:
        olddata.append(i)
    
    for i in type:
        olddata.append(i)
        
    for i in size:
        olddata.append(i)
    
    # print(composition, weight, type, size)
    
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(olddata)         
        
        
        
def get_content(url):

    try:
        request = requests.get(url, headers=headers)
        # redirect check
        if request.status_code == 200:
            content = request.json()
            return content
        else:
            print(request.status_code)
            return None

    except Exception as e:
        print(e)
        return None 
            
def wb_parser(link, olddata, filename):
    content = get_content(link)
    if content:
        try:
            composition = [i['name'] for i in content['compositions']]
        except:
            composition = [0]
            
        options = content['options']
        
        weight = [i['value'] for i in options if i['name'] == 'Вес с упаковкой (кг)']
        if len(weight) == 0:
            weight = [0]
        
        type = [i['value'].split(';') for i in options if i['name'] == 'Тип плетения постельного белья']
        if len(type) == 0:
            type = [0]
        else:
            type = type[0]
            
        size = [i['value'].split(';') for i in options if i['name'] == 'Размер натяжной простыни']
        if len(size) == 0:
            size = [0]
        else:
            size = size[0]
        
        data = {'composition': composition, 'weight': weight, 'type': type, 'size': size }
        print(data)
        
        add_to_csv(data, olddata, filename)


def create_head(filename):
    head = ['Thumb', 'SKU', 'Name', 'Color', 'Category', 'Category Position',
            'Brand', 'Seller', 'Balance', 'First Date', 'Comments', 'Rating',
            'Final price', 'SPP Price', 'Revenue potential', 'Days in stock',
            'Sales', 'Sales Per Day Average', 'Revenue', 'Pics Count',
            'Hax Video', 'Categories Last Count',
            'Composition 1', 'Composition 2', 'Composition 3', 'Weight', 'Type 1', 'Type 2', 'Type 3', 'Type 4', 'Size 1', 'Size 2', 'Size 3']

    with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(head)  
            
            
def main(filename):
    create_head(filename)
    for i in get_data_from_csv():
        try:
            link = f"{i[0].split('images')[0]}info/ru/card.json"
            print(link)
            wb_parser(link, i, filename)
        except Exception as e:
            print(e)
            
main('newdata.csv')