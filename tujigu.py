from lxml import etree
import requests,os,re,webbrowser,time
proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
def download():
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    print('2秒后为您打开主页:https://www.tujigu.com 挑选喜欢的妹子点进去 再把url链接复制粘贴到下面, 再按回车即可!')
    time.sleep(2)
    webbrowser.open('https://www.tujigu.com')
    url=input('\n快速下载:')
    r=requests.get(url=url,headers=headers,timeout=7)
    r.encoding = r.apparent_encoding
    r_bt=etree.HTML(r.text)
    title=r_bt.xpath('//title/text()')
    path(title[0])
    picnum=int(re.findall("<p>图片数量： (.*?)P</p>",r.text)[0])
    ID=url.split("/")[4]
    print('共有%s张照片' % picnum)
    for i in range(1, picnum + 1):
        picurl = "https://tjg.gzhuibei.com/a/1/" + ID + '/' + str(i) + '.jpg'  # 单个图片URL地址的拼接
        print('正在下载：' + picurl)
        pic = requests.get(picurl,headers=headers)
        with open('%s\%s.jpg' % (title[0], i), 'wb') as f:
            f.write(pic.content)
        time.sleep(1)
    print( '\n下载完成！\n\n')

def  path(title):
    path = title  # 设置输出文件夹
    if not os.path.exists(path):  # 判断文件夹不存在
        os.makedirs(path)  # 不存在则建立文件夹
        print('目录创建完成')
    else:
        exit('已经下载过了哦!')


if __name__ == '__main__':
    download()
