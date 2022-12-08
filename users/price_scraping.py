import requests
from bs4 import BeautifulSoup as soup


def One_mg(serch_field):

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
    product_names = bsobj.findAll('div',{'class':'style__pro-title___3G3rr'})
    mrps = bsobj.findAll('div',{'class':'style__price-tag___KzOkY'})

    for mrp, name in zip(mrps, product_names):
        mrp_name.update({name.text:mrp.text})


    # print(mrp_name)
    return mrp_name