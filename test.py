import requests

def classify(url,str):
    dict = {
        'H3C_AP':{'feature':'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd',
              'num':0,
              'url':[]
              },
        'HP_Printer': {'feature': '<link href="/hp/device/defaultScript.css" type="text/css" rel="stylesheet">',
               'num': 0,
               'url': []
               },
        'Huawei_AP': {'feature': 'huawei',
               'num': 0,
               'url': []
               },
        'OpenWRT': {'feature': 'openwrt',
               'num': 0,
               'url': []
               },
        'Pandavan': {'feature': '401 Unauthorized',
               'num': 0,
               'url': []
               },
        'Tp-link': {'feature': 'http://www.tp-link.com.cn',
                     'num': 0,
                     'url': []
                     },
        'Can\'t classify': {'feature': '',
                    'num': 0,
                    'url': []
                    },
    }

    for i in dict.keys():
        result = str.rfind(dict[i]['feature'])
        if result != -1:
            dict[i]['num']+=1
            dict[i]['url'].append(url)
            break
        elif i == 'Can\'t classify':
            dict['Can\'t classify']['num'] += 1
            dict['Can\'t classify']['url'].append(url)

    for i in dict.keys():
        print(i,dict[i])




url = 'http://172.31.124.23/'

response = requests.get(url)

str = response.text

#print(str)


#print(result)
#print(type(response.text))

classify(url,str)
