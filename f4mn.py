import os,time,requests,threading
from lxml import etree
from tqdm  import  tqdm
start = time.perf_counter()

# 网站https://www.f4mn.com/
headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',}

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

def title_img(url):
    r=requests.get(url=url,headers=headers)
    r.endcoding = r.apparent_encoding
    r = etree.HTML(r.text)
    title = r.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/h1/text()')[0]
    imgurl=r.xpath('/html/body/div[1]/div[2]/div[1]/div[4]/div[*]/img/@data-src')
    return  title,imgurl


def download(url):
    threads = []
    title, img = title_img(url)
    path(title)
    print('开始下载')
    for i, url in enumerate(img):
        t = threading.Thread(target=run, args=(i + 1, url, title))
        threads.append(t)
    for t in threads:
        t.start()
    for t in tqdm(threads):
        t.join()
    print('下载完成')


if __name__ == '__main__':
    download('https://www.f4mn.com/beauty/20220907/26919.html')
    print('总共耗时{:.2f}秒'.format(time.perf_counter() - start))
