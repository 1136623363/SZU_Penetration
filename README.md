# SZU_Penetration
记一次校园网内网渗透

某次做实验时观察到机房某台机器的ip为172.31.103.186

 1. 留意到实验室网段在172.31.0.0
	宿舍区网段在172.29.0.0
 2. nmap扫描80端口开放的主机保存到文本
![输入图片说明](/imgs/1.png)
 3.  python读取文本并提取ip
```
import re  
import json  
import requests  
import time  
import random  
import urllib.request

def ip_match(filename):  
  
    with open(filename, encoding='utf-8') as fh:  
        fstring = fh.readlines()  
  
    # declaring the regex pattern for IP addresses  
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')  
  
    # initializing the list object  
    lst = []  
  
    # extracting the IP addresses  
    for line in fstring:  
        match = pattern.search(line)  
        if match is not None:  
            lst.append(match[0])  
        else:  
            # lst.append(None)  
            continue  
  
    # displaying the extracted IP addresses  
    new_name = filename[:-4] + '_ip.txt'  
    print(new_name)  
    print(f'分离出{len(lst)}个ip写入到{new_name}')  
    with open(new_name, 'w') as fw:  
        json.dump(lst, fw)  
    return new_name
    
if __name__ == '__main__':  
    ip = ip_match('train.log')
```
得到纯ip文本 
![输入图片说明](/imgs/2.png)
 4. 用python的requests进行get请求，只取响应状态码200的ip，返回的几乎都是可以访问的url
![输入图片说明](/imgs/3.png)
 5. 因为url中含有无线AP、打印机等重复设备，故进行分类处理（未优化）
 完整代码：
```
import re  
import json  
import requests  
import time  
import random  
import urllib.request  
  
def ip_match(filename):  
  
    with open(filename, encoding='utf-8') as fh:  
        fstring = fh.readlines()  
  
    # declaring the regex pattern for IP addresses  
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')  
  
    # initializing the list object  
    lst = []  
  
    # extracting the IP addresses  
    for line in fstring:  
        match = pattern.search(line)  
        if match is not None:  
            lst.append(match[0])  
        else:  
            # lst.append(None)  
            continue  
  
    # displaying the extracted IP addresses  
    new_name = filename[:-4] + '_ip.txt'  
    print(new_name)  
    print(f'分离出{len(lst)}个ip写入到{new_name}')  
    with open(new_name, 'w') as fw:  
        json.dump(lst, fw)  
    return new_name  
  
  
def code_check(filename):  
    dict = {  
        'alist': {'feature': 'ALIST',  
                    'num': 0,  
                    'url': []  
                    },  
        '移动数据可视化系统': {'feature': '移动数据可视化系统',  
                  'num': 0,  
                  'url': []  
                  },  
        'Microsoft': {'feature': '<title>IIS Windows Server</title>',  
                   'num': 0,  
                   'url': []  
                   },  
        'Microsoft2': {'feature': 'Microsoft Windows Server',  
                      'num': 0,  
                      'url': []  
                      },  
  
        'H3C_AP': {'feature': 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd',  
                   'num': 0,  
                   'url': []  
                   },  
        'H3C_AP2': {'feature': 'Web网管',  
                   'num': 0,  
                   'url': []  
                   },  
  
        'HP_Printer': {'feature': '<link href="/hp/device/defaultScript.css" type="text/css" rel="stylesheet">',  
                       'num': 0,  
                       'url': []  
                       },  
        'HP_Printer2': {'feature': '黑色碳粉盒',  
                       'num': 0,  
                       'url': []  
                       },  
        'HP_Printer3': {'feature': '<p>Please enable JavaScript or use a browser that supports JavaScript.</p>',  
                        'num': 0,  
                        'url': []  
                        },  
        '松下_Printer': {'feature': '<title>KX-MB2138CN</title>',  
                       'num': 0,  
                       'url': []  
                       },  
  
        'Huawei_AP': {'feature': 'Huawei',  
                      'num': 0,  
                      'url': []  
                      },  
        'OpenWRT': {'feature': 'openwrt',  
                    'num': 0,  
                    'url': []  
                    },  
        'OpenWRT2': {'feature': 'OpenWrt',  
                    'num': 0,  
                    'url': []  
                    },  
        'OpenWRT3': {'feature': 'LuCI',  
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
        'ubuntu': {'feature': 'Apache2 Ubuntu',  
                    'num': 0,  
                    'url': []  
                    },  
  
        'fenbushi': {'feature': 'alert("用户不存在");',  
                    'num': 0,  
                    'url': []  
                    },  
        'tongxinji': {'feature': '通信管理机维护管理平台',  
                     'num': 0,  
                     'url': []  
                     },  
        '中易和': {'feature': 'expire = new Date((new Date()).getTime() + 24 * 3600000);',  
                      'num': 0,  
                      'url': []  
                      },  
  
        'canon': {'feature': 'canon',  
                    'num': 0,  
                    'url': []  
                    },  
        '海康威视': {'feature': 'window.location.href = "./doc/page/login.asp?_" + (new Date()).getTime();',  
                  'num': 0,  
                  'url': []  
                  },  
        '海康威视2': {'feature': 'window.location.href = "/doc/page/login.asp?_" + (new Date()).getTime();',  
                     'num': 0,  
                     'url': []  
                     },  
        'Nas': {'feature': 'DiskStation',  
                     'num': 0,  
                     'url': []  
                     },  
        'Nas2': {'feature': 'Web Station has been enabled',  
                'num': 0,  
                'url': []  
                },  
        'nextcloud': {'feature': 'https://nextcloud.com',  
                'num': 0,  
                'url': []  
                },  
        'Cloudam云端': {'feature': 'Cloudam云端',  
                      'num': 0,  
                      'url': []  
                      },  
        '锐取': {'feature': '互动教学调度平台',  
                        'num': 0,  
                        'url': []  
                        },  
        '进出纪录': {'feature': '<script> var pro_name = new Array( "OAO-MJ102","Webpass","BF50","BF333" ) ; </script>',  
                        'num': 0,  
                        'url': []  
                        },  
        'CALIS采编一体化平台': {'feature': 'CALIS采编一体化平台',  
                 'num': 0,  
                 'url': []  
                 },  
        'sewise直播服务器': {'feature': 'sewise直播服务器',  
                                'num': 0,  
                                'url': []  
                                },  
  
        'Unknow1': {'feature': 'You are using an unsupported or obsolete broswer which may cause errors or',  
                    'num': 0,  
                    'url': []  
                    },  
        'Unknow2': {'feature': 'If you are the Web site administrator',  
                    'num': 0,  
                    'url': []  
                    },  
        'Unknow3': {'feature': 'window.location = "/wcn/banner?lang=1";',  
                    'num': 0,  
                    'url': []  
                    },  
        'Unknow4': {'feature': '<img ID=pagerrorImg src="pagerror.gif" width=36 height=48>',  
                    'num': 0,  
                    'url': []  
                    },  
  
        'Unknow5': {'feature': 'window.location.href="/idp";',  
                    'num': 0,  
                    'url': []  
                    },  
        'Unknow6': {'feature': "</strong><font color='#ff0000' DESIGNTIMESP='4019'><strong DESIGNTIMESP='4018'></strong>",  
                    'num': 0,  
                    'url': []  
                    },  
        'Unknow7': {  
            'feature': "Welcome to nginx!",  
            'num': 0,  
            'url': []  
            },  
  
        'SZU1': {'feature': '深圳大学',  
                    'num': 0,  
                    'url': []  
                    },  
        'SZU2': {'feature': '图书馆',  
                'num': 0,  
                'url': []  
                },  
        'SZU3': {'feature': '港澳',  
                'num': 0,  
                'url': []  
                },  
        'SZU4': {'feature': '大成老旧刊全文数据库',  
                 'num': 0,  
                 'url': []  
                 },  
        'SZU5': {'feature': '党员姓名',  
                 'num': 0,  
                 'url': []  
                 },  
        'SZU6': {'feature': '违纪处分义工时系统',  
                 'num': 0,  
                 'url': []  
                 },  
        '天眼云镜': {'feature': 'if (local.pathname.indexOf(\'v3\') < 0) {',  
                     'num': 0,  
                     'url': []  
                     },  
        'GitLab': {'feature': '172.31.72.22',  
                     'num': 0,  
                     'url': []  
                     },  
        '纺织物缺陷检测': {'feature': '纺织物检测平台',  
                   'num': 0,  
                   'url': []  
                   },  
        '恒温恒湿培养箱': {'feature': '弹出窗口阴影层',  
                           'num': 0,  
                           'url': []  
                           },  
        'Dr.Huang': {'feature': 'lhuang@szu.edu.cn',  
                 'num': 0,  
                 'url': []  
                 },  
  
        'Can\'t classify': {'feature': 'xxxxxxxxxx',  
                            'num': 0,  
                            'url': []  
                            },  
    }  
  
  
    with open(filename, encoding='utf-8') as fh:  
        ip = json.load(fh)  
  
    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",  
                        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",  
                        "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",  
                        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",  
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",  
                        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",  
                        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",  
                        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",  
                        ]  
    headers = {'User-Agent': random.choice(user_agent_list)}  
  
    code = [200,401]  
  
    url_list=[]  
    for i in ip:  
        url_http = 'http://'+i  
        #url_https = 'https://' + i  
        # print(url_http)  
        try:  
            response_http = requests.get(url=url_http,headers=headers,timeout=2)  
            response_http.encoding = 'utf-8'  
            if response_http.status_code in code:  
                # result = response_http.text.rfind('http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')  
                # if result == -1:                #     #print(url_http)  
                for j in dict.keys():  
                    result = response_http.text.rfind(dict[j]['feature'])  
                    if result != -1:  
                        dict[j]['num'] += 1  
                        dict[j]['url'].append(url_http)  
                        print('Classified success')  
                        print(url_http)  
                        break  
                    elif j == 'Can\'t classify':  
                        dict['Can\'t classify']['num'] += 1  
                        dict['Can\'t classify']['url'].append(url_http)  
  
                        print(response_http.text)  
                        print('Classified faied')  
                        print(url_http)  
                        #input("Stop")  
  
                url_list.append(url_http)  
        except:  
            pass  
  
    new_name = filename[:-4] + '_url.txt'  
  
    print(f'{len(url_list)}个url写入到{new_name}')  
    #  
    # with open(new_name,'w') as fw:    #     json.dump(url_list,fw)  
    for i in dict.keys():  
        print(i,dict[i])  
  
    with open('dict','w') as fw:  
        json.dump(dict,fw)  
  
  
  
if __name__ == '__main__':  
    ip = ip_match('train.log')  
    code_check(ip)
```
![输入图片说明](/imgs/4.png)
![输入图片说明](/imgs/5.png)
![输入图片说明](/imgs/6.png)
![输入图片说明](/imgs/7.png)
![输入图片说明](/imgs/8.png)
![输入图片说明](/imgs/9.png)
![输入图片说明](/imgs/10.png)
![输入图片说明](/imgs/11.png)
![输入图片说明](/imgs/12.png)
