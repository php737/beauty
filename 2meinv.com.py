import requests,os,time,threading
from lxml import etree
from tqdm  import  tqdm
start = time.perf_counter()
#https://www.2meinv.com/

headers={'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
proxy='' #本地 127.0.0.1:10809  120.42.46.226:6666
proxies = {'http': proxy, 'https': proxy}

def  path(title):
    path = title  # 设置输出文件夹
    if not os.path.exists(path):  # 判断文件夹不存在
        os.makedirs(path)  # 不存在则建立文件夹
        print('{}目录创建完成'.format(path))
    else:
        exit('已经下载过了哦!')

def run(i,url,path_title):#数量,链接,路径
    pic = requests.get(url,headers=headers)
    with open('{}\{}.jpg'.format(path_title, i), 'wb') as f:
        f.write(pic.content)

def title_img():
    r=requests.get(url=url,headers=headers,proxies=proxies)
    r.encoding=r.apparent_encoding
    r=etree.HTML(r.text)
    title=r.xpath('/html/body/div[2]/div/h1/text()')[0]
    img_urlnum=r.xpath('/html/body/div[6]/div/a[8]/text()')[0]
    img_page=r.xpath('/html/body/div[5]/a/@href')[0][:-6]
    print('共有{}张图片'.format(img_urlnum))
    img_urls=[] #图片链接
    for i in range(1,int(img_urlnum)+1):  #生成整个图片的页面
        img_urls.append(img_page+str(i)+'.html')
    return title,img_urls

def imguls(i,urls,path_title):#图片链接
    r1 = requests.get(url=urls, headers=headers, proxies=proxies)
    r1.encoding=r1.apparent_encoding
    r1=etree.HTML(r1.text)
    run(i,r1.xpath('/html/body/div[5]/a/img/@src')[0],path_title)

def download():
    threads = []
    title, img = title_img()
    path(title)
    print('开始下载')
    for i,url in enumerate(img):
        t=threading.Thread(target=imguls,args=(i+1,url,title))
        threads.append(t)
    for t in threads:
        t.start()
    for t in tqdm(threads):
        t.join()
    print('下载完成')

if __name__ == '__main__':
    url='https://www.2meinv.com/article-5573.html'
    download()
    print('总共耗时{:.2f}秒'.format(time.perf_counter() - start))

