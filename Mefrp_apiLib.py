import requests,json,os,pickle,time # type: ignore


class MefrpClient:
    def __init__(self,token=""):
        #创建一个名为config的文件夹，
        #用于储存配置
        try:
            os.mkdir("config")
        except Exception as e:
            pass
        #if not os.path.exists(os.path.join(os.getcwd()+"\\config","global.json")):
            #with (open(os.path.join(os.getcwd()+"\\config","global.json")),"w+") as file:
                #print("{}",file=file)
                #file.close()
        if token:
            self.token=token



    def login(self,username:str,password:str,headers:dict=False):
        #确认用户登录信息，
        #并返回确认码和用户token
        data={
            "username":username,
            "password":password,
            }
        if headers:
            response=requests.post("https://api.mefrp.com/api/public/login",json=data,headers=headers)
        else:
            response=requests.post("https://api.mefrp.com/api/public/login",json=data)
        if json.loads(response.text).get("code")==200:
            self.token=json.loads(response.text).get("data").get("token")
        return json.loads(response.text)



    def save_data(self,data:dict,method:str="chenge"):
        #用pickle,bug少
        #用于储存数据，
        #data格式为dict，
        #method共有两种模式，
        #“chenge”和“rewrite”，
        #分别表示新加入或者覆盖所有配置，
        #然后重写


        if method=="chenge":
            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"rb") as file:
                old_data=json.loads(file.read(7500))
                print(old_data)

            for key,val in data:
                old_data[key]=val

            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"wb+") as file:
                file.write(str(old_data))

        elif method=="rewrite":
            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"wb+") as file:
                file.write(str(data))

        else:
            return "\'method\'must be \'chenge\' or\'rewrite\'"

    # noinspection PyTypeChecker
    def save_data_pickle(self,data:dict,method:str="chenge"):
        if method=="chenge":
            old_data=pickle.load(open(os.path.join(os.getcwd()+"\\config","global.json"),"rb+"))

            for key,val in data.items():
                old_data[key]=val
            with open(os.path.join(os.getcwd()+"\\config","global.json"),"wb+") as file:
                pickle.dump(data, file)

        elif method=="rewrite":
            with open(os.path.join(os.getcwd()+"\\config","global.json"),"wb+") as file:
                pickle.dump(data, file)
        else:
            return "\'method\'must be \'chenge\' or\'rewrite\'"
        




    def read_data(self):
        #用于读取已经写好的配置文件，
        #json返回
        return pickle.load(open(os.path.join(os.getcwd()+"\\config","global.json"),"rb+"))

    
    def get_info(self,token:str=""):
        #获取mefrp用户信息
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/user/info",headers=header)
        return json.loads(response.text)


    def get_ad(self,token:str=""):
        #获取官方广告
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/ads/query?placement=home",headers=header)
        return json.loads(response.text)


    def get_notice(self,token:str=""):
        #获取公告
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/notice",headers=header)
        return json.loads(response.text)


    def sign(self,token:str=""):
        #用户签到
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/user/sign",headers=header)
        return json.loads(response.text)


    def node_list(self,token:str=""):
        #获取节点列表
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/node/list",headers=header)
        return json.loads(response.text)


    def add_proxy(self,data:dict,token:str=""):
        #添加隧道
        #data类型为dict，包含accesskey(可选)，domain(可选)，headerXFromWhere(可选)，hostHeaderRewrite(可选)，proxyProtocolVersion(可选）
        #必填项：localIp(本地ip)，localPort(本地端口)，nodeId(节点id),proxyName(隧道名称),proxyType(隧道协议，如udp，tcp，http，https)，remotePort(外网端口)，useCompression(使用压缩)，useEncryption(使用加密)

        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.post("https://api.mefrp.com/api/auth/proxy/create",headers=header,json=data)
        return json.loads(response.text)
    

    def get_free_port(self,NodeId,protocol,token:str=""):
        #获取节点空闲端口，NodeId是节点编号，protocol是协议(如tcp，udp)

        if not token:
            token=self.token
        data={
            "nodeId":NodeId,
            "protocol":protocol
        }
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.post("https://api.mefrp.com/api/auth/node/freePort",headers=header,json=data) 
        return json.loads(response.text)

    def set_token(self,token:str):
        #手动更改对象中储存的token
        self.token=token



    def add_domain(self,domain:str,token:str=""):
        #添加域名
        #形参domain为首级域名
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        data={
            "domain":domain,
            }
        response=requests.post("https://api.mefrp.com/api/auth/user/icpDomain/add",headers=header,json=data)
        return json.loads(response.text)


    def del_domain(self,domain:str,token:str=""):
        #删除域名
        #形参domain为首级域名
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        data={
            "domain":domain,
            }
        response=requests.post("https://api.mefrp.com/api/auth/user/icpDomain/delete",headers=header,json=data)
        return json.loads(response.text)

    def list_domain(self,token:str=""):
        #查询域名列表
        #形参domain为首级域名
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/user/icpDomain/list",headers=header)
        return json.loads(response.text)

    def is_realname(self,token:str=""):
        #查询用户是否实名认证
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/user/info/realname",headers=header)
        return json.loads(response.text)

    def token_reset(self,token:str=""):
        #重置用户token(慎用)
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/user/tokenReset",headers=header)
        if json.loads(response.text).get("code")==200:
            self.token=json.loads(response.text).get("data").get("newToken")
        return json.loads(response.text)

    def get_token(self):
        #获取对象中储存的token
        return self.token

    def chenge_password(self,orginal:str,new:str,token:str=""):
        #重置用户密码，orginal为原密码，new为新密码
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        data={
            "newPassword":new,
            "oldPassword":orginal
            }
        response=requests.post("https://api.mefrp.com/api/auth/user/passwordReset",headers=header,json=data)
        return json.loads(response.text)


    def kick(self,proxyId,token:str=""):
        #强制下线隧道
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        data={
            "proxyId":proxyId,
            }
        response=requests.post("https://api.mefrp.com/api/auth/proxy/kick",headers=header,json=data)
        return json.loads(response.text)


    def proxy_list(self,token:str=""):
        #列出用户名下的隧道
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/proxy/list",headers=header)
        return json.loads(response.text)


    def update_proxy(self,data:dict,token:str=""):
        #更新隧道信息，data输入参考请看add_proxy函数,还要另外加入proxyId形参(字典内)
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.post("https://api.mefrp.com/api/auth/proxy/update",headers=header,json=data)
        return json.loads(response.text)


    def toggle_proxy(self,proxyId:int,is_enable:bool,token:str=""):
        #设置隧道的状态(启用或者禁用)
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        data={
            "isDisabled":not is_enable,
            "proxyId":proxyId
            }
        
        response=requests.post("https://api.mefrp.com/api/auth/proxy/toggle",headers=header,json=data)
        return json.loads(response.text)
