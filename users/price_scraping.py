import requests
from bs4 import BeautifulSoup as soup
import re


def One_mg(serch_field, isList=False):

    url = f'https://www.1mg.com/search/all?filter=true&name={serch_field["searchField"]}'


    header = {'Origin': 'https://www.1mg.com',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }


    html = requests.get(url=url,headers=header)
    html.status_code

    bsobj = soup(html.content, 'lxml')
    # print(bsobj)



    mrp = []
    mrp_name = {}
    mrp_name_list = []
    product_names = bsobj.findAll('span',{'class':'style__pro-title___3zxNC'})
    mrps = bsobj.findAll('div',{'class':'style__price-tag___B2csA'})

    for mrp, name in zip(mrps, product_names):
        if isList:
            mrp_name_list.append(f"{name.text} : {float(re.findall('[0-9]+', mrp.text)[0])}")
        else:
            mrp_name.update({name.text:float(re.findall('[0-9]+', mrp.text)[0])})


    # print(mrp_name)
    if isList:
        return mrp_name_list
    else:
        return mrp_name


def pharm_easy(serch_field, isList=False):

    url = f'https://pharmeasy.in/search/all?name={serch_field["searchField"]}'

    header = {'Origin': 'https://pharmeasy.in',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }


    html = requests.get(url=url,headers=header)
    html.status_code

    bsobj = soup(html.content, 'lxml')
    # print(bsobj)

    mrp = []
    mrp_name = {}
    mrp_name_list = []
    product_names = bsobj.findAll('h1',{'class':'ProductCard_medicineName__8Ydfq'})
    mrps = bsobj.findAll('div',{'class':'ProductCard_ourPrice__yDytt'})

    for mrp, name in zip(mrps, product_names):
        if isList:
            mrp_name_list.append(f"{name.text} : {float(re.findall('[0-9]+', mrp.text)[0])}")
        else:
            mrp_name.update({name.text:float(re.findall('[0-9]+', mrp.text)[0])})


    # print(mrp_name)
    if isList:
        return mrp_name_list
    else:
        return mrp_name

def flipkart_health(serch_field, isList=False):

    url = f'https://healthplus.flipkart.com/search?q={serch_field["searchField"]}&api=o&skip=1'

    header = {'Origin': 'https://healthplus.flipkart.com/',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }


    html = requests.get(url=url,headers=header)
    html.status_code

    bsobj = soup(html.content, 'lxml')
    # print(bsobj)

    mrp = []
    mrp_name = {}
    mrp_name_list = []
    product_names = bsobj.findAll('h4',{'class':'product-name'})
    mrps = bsobj.findAll('span',{'class':'del-rs'})

    for mrp, name in zip(mrps, product_names):
        if isList:
            mrp_name_list.append(f"{name.text} : {float(re.findall('[0-9]+', mrp.text)[0])}")
        else:
            mrp_name.update({float(re.findall('[0-9]+', mrp.text)[0])})


    # print(mrp_name)
    if isList:
        return mrp_name_list
    else:
        return mrp_name