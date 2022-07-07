import  requests,os,threading
from lxml import etree
from tqdm  import  tqdm

#网站:https://everia.club/ 
headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12A365 MicroMessenger/5.4.1 NetType/5G'}
def  path(title):
    path = title  # 设置输出文件夹
    if not os.path.exists(path):  # 判断文件夹不存在
        os.makedirs(path)  # 不存在则建立文件夹
        print('{}目录创建完成'.format(path))
    else:
        exit('已经下载过了哦!')

def run(i,url,path_title):#数量,链接,名称路径
    pic = requests.get(url,headers=headers)
    with open('{}\{}.jpg'.format(path_title, i), 'wb') as f:#二进制下载
        f.write(pic.content)

def download(url):
    r=requests.get(url=url,headers=headers,timeout=7)
    r.encoding=r.apparent_encoding
    r=etree.HTML(r.text)
    title=r.xpath('/html/body/div/main/div/div/article/div[2]/text()')[0]
    img_url=r.xpath('/html/body/div/main/div/div/article/div[2]/figure/figure[*]/img/@src')
    print('共有{}张图片'.format(len(img_url)))
    path(title)#创建文件夹
    threads = [] #创建数组多线程下载
    for i,url in enumerate(img_url):
        t=threading.Thread(target=run,args=(i,url,title))
        threads.append(t)
    for t in threads:
        t.start()
    for t in tqdm(threads):
        t.join()
    print('下载完成!')

if __name__=='__main__':
    download('https://everia.club/2022/06/29/xiuren%e7%a7%80%e4%ba%ba%e7%bd%91-2021-11-24-no-4264-%e7%8e%8b%e5%bf%83%e6%80%a1/')
