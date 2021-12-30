from  lxml import etree
import  requests,re,os,threading
proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
def  path(title):
    path = title  # 设置输出文件夹
    if not os.path.exists(path):  # 判断文件夹不存在
        os.makedirs(path)  # 不存在则建立文件夹
        print('目录创建完成')
    else:
        exit('已经下载过了哦!')

def run(i,url,path_title):#数量,链接,名称路径
    print('正在下载{}: {}'.format(i,url))
    pic = requests.get(url,headers=headers)
    with open('{}\{}.jpg'.format(path_title, i), 'wb') as f:#二进制下载
        f.write(pic.content)
def download(url):
    r=requests.get(url=url,headers=headers,timeout=7)
    r.encoding=r.apparent_encoding
    r_bt = etree.HTML(r.text)
    title = r_bt.xpath('//h1/text()')[0]
    path(title)#创建文件夹
    picnum=int(re.findall('展开全图\(1/(.*?)\)</i></span>' ,r.text)[0])#正则匹配标题括号可以用反斜杠 \
    purl=re.findall('<div class="content" id="content"><img src="(.*?)1.jpg" alt=',r.text)[0]#匹配图片url
    print('共有{}张图片'.format(picnum))
    threads = [] #创建数组多线程下载
    for i in range(1,picnum+1):
        picurl=purl+str(i)+'.jpg'#拼接图片的url
        threads.append(
            threading.Thread(target=run, args=(i, picurl, title))
        )

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('\n{}下载完成!'.format(title))

if __name__ == '__main__':
    print('图片下载器v1.1')
    print('打开主页:https://www.tuiimg.com/meinv/ 挑选喜欢的妹子点进去 再把url链接复制粘贴到下面, 再按回车即可!')
    url = input('\n快速下载:')
    download(url)##获取链接下载 
