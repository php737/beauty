import  requests,os,threading,time
from lxml import etree
from tqdm  import  tqdm
start = time.perf_counter()
headers={'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1'}

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

def download(url):
    r=requests.get(url=url,headers=headers,timeout=7)
    r.endcoding=r.apparent_encoding
    r=etree.HTML(r.text)
    title=r.xpath('/html/body/div[3]/div/div/div[1]/h1/text()')[0]
    img_url=r.xpath('/html/body/div[3]/div/div[1]/div[4]/div/img/@data-original')
    print('共有{}张图片'.format(len(img_url)))
    path(title)
    threads = []
    for i,url in enumerate(img_url):
        t=threading.Thread(target=run,args=(i,url,title))
        threads.append(t)
    for t in threads:
        t.start()
    for t in tqdm(threads):
        t.join()
    print('下载OK!')

if __name__ == '__main__':
    download('http://www.502x.com/yuhuajie/207-all.html')#必须是全图模式  网站http://www.502x.com/ 选需要的地址
    end = time.perf_counter()
    print('耗时{:.2f}秒'.format(end-start))
