import requests,threading,time,os,base64
from tqdm import tqdm
headers={'User-Agent': 'iPhone14,2(iOS/16.4.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1125x2436'}
ip= '' #代理
proxies={'http':'http://' + ip, 'https':'http://' + ip}
ssa_url=base64.b64decode('d3d3LnNzYWxlZ3Muc3RvcmU=').decode("utf-8")
def run(i,url,path_title):#数量,链接,名称路径
    print(f'正在下载{i}: {url}')
    pic = requests.get(url,headers=headers,proxies=proxies)
    with open(f'{path_title}\{i}.jpg', 'wb') as f:
        f.write(pic.content)
def  get_url(id):
    url=f'https://{ssa_url}/cms/appapi/shows/catid/39/id/{id}/imgclarity/720'
    r=requests.get(url,headers=headers,proxies=proxies,timeout=7)
    r.encoding=r.apparent_encoding
    return r.json()
def  ssa_id():
    url=f'https://{ssa_url}/cms/appapi/index/catid/46/page/1/pagenum/100/keywords/'
    r=requests.get(url,headers=headers,proxies=proxies,timeout=7)
    r.encoding = r.apparent_encoding
    r=r.json()
    for i in r:
        print(i['title'],i['id'])

def  path(title):
    path = title  # 设置输出文件夹
    if not os.path.exists(path):  # 判断文件夹不存在
        os.makedirs(path)  # 不存在则建立文件夹
        print('目录创建完成')
    else:
        exit('已经下载过了哦!')
def download(id):
    img_data = get_url(id)
    img_num=len(img_data['playimages'])
    title=img_data['title']
    path(title)
    threads=[] #多线程
    num=1
    print(f'共有{img_num}张图片')
    for url in img_data['playimages']:
        threads.append(
            threading.Thread(target=run,args=(num,url,title))
        )
        num+=1
    for thread in threads:
        thread.start()
    for thread in tqdm(threads):
        thread.join()
    print(f'\n{title}下载已完成!')

if __name__ == '__main__':
   #print(get_url(1564))
   download(1563)
   #ssa_id()#id查询
