import requests,json,os,pickle,time # type: ignore


class MefrpClient:
    def __init__(self,token=""):
        #����һ����Ϊconfig���ļ��У�
        #���ڴ�������
        try:
            os.mkdir("config")
        except Exception:
            pass
        if not os.path.exists(os.path.join(os.getcwd()+"\\config","global.json")):
            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"w") as file:
                print("{}",file=file)
                file.close()
        if token:
            self.token=token



    def login(self,username:str,password:str,headers:dict=False):
        #ȷ���û���¼��Ϣ��
        #������ȷ������û�token
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
        #��pickle,bug��
        #���ڴ������ݣ�
        #data��ʽΪdict��
        #method��������ģʽ��
        #��chenge���͡�rewrite����
        #�ֱ��ʾ�¼�����߸����������ã�
        #Ȼ����д


        if method=="chenge":
            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"r") as file:
                old_data=json.loads(file.read(7500))
                print(old_data)

            for key,val in data:
                old_data[key]=val

            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"w") as file:
                file.write(str(old_data))

        elif method=="rewrite":
            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"w") as file:
                file.write(str(data))

        else:
            return("\'method\'must be \'chenge\' or\'rewrite\'")


    def save_data_pickle(self,data:dict):
        if method=="chenge":
            old_data=pickle.trt()

            for key,val in data.items():
                old_data[key]=val

            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"w") as file:
                file.write(str(old_data))
                file.close()

        elif method=="rewrite":
            with (open(os.path.join(os.getcwd()+"\\config","global.json")),"w") as file:
                file.write(str(data))
                file.close()

        else:
            return("\'method\'must be \'chenge\' or\'rewrite\'")
        




    def read_data(self):
        #���ڶ�ȡ�Ѿ�д�õ������ļ���
        #json����
        with (open(os.path.join(os.getcwd()+"\\config","global.json")),"r") as file:
                data=json.loads(file.read(7500))
                file.close()
        return data

    
    def get_info(self,token:str=""):
        #��ȡmefrp�û���Ϣ
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/user/info",headers=header)
        return json.loads(response.text)


    def get_ad(self,token:str=""):
        #��ȡ�ٷ����
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/ads/query?placement=home",headers=header)
        return json.loads(response.text)


    def get_notice(self,token:str=""):
        #��ȡ����
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/notice",headers=header)
        return json.loads(response.text)


    def sign(self,token:str=""):
        #�û�ǩ��
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/user/sign",headers=header)
        return json.loads(response.text)


    def node_list(self,token:str=""):
        #��ȡ�ڵ��б�
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.get("https://api.mefrp.com/api/auth/node/list",headers=header)
        return json.loads(response.text)


    def add_proxy(self,data:dict,token:str=""):
        #������
        #data����Ϊdict������accesskey(��ѡ)��domain(��ѡ)��headerXFromWhere(��ѡ)��hostHeaderRewrite(��ѡ)��proxyProtocolVersion(��ѡ��
        #�����localIp(����ip)��localPort(���ض˿�)��nodeId(�ڵ�id),proxyName(�������),proxyType(���Э�飬��udp��tcp��http��https)��remotePort(�����˿�)��useCompression(ʹ��ѹ��)��useEncryption(ʹ�ü���)

        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.post("https://api.mefrp.com/api/auth/proxy/create",headers=header,json=data)
        return json.loads(response.text)
    

    def get_free_port(self,NodeId,protocol,token:str=""):
        #��ȡ�ڵ���ж˿ڣ�NodeId�ǽڵ��ţ�protocol��Э��(��tcp��udp)

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
        #�ֶ����Ķ����д����token
        self.token=token



    def add_domain(self,domain:str,token:str=""):
        #�������
        #�β�domainΪ�׼�����
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
        #ɾ������
        #�β�domainΪ�׼�����
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
        #��ѯ�����б�
        #�β�domainΪ�׼�����
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/user/icpDomain/list",headers=header)
        return json.loads(response.text)

    def is_realname(self,token:str=""):
        #��ѯ�û��Ƿ�ʵ����֤
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/user/info/realname",headers=header)
        return json.loads(response.text)

    def token_reset(self,token:str=""):
        #�����û�token(����)
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
        #��ȡ�����д����token
        return self.token

    def chenge_password(self,orginal:str,new:str,token:str=""):
        #�����û����룬orginalΪԭ���룬newΪ������
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
        #ǿ���������
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
        #�г��û����µ����
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
        }
        response=requests.get("https://api.mefrp.com/api/auth/proxy/list",headers=header)
        return json.loads(response.text)


    def update_proxy(self,data:dict,token:str=""):
        #���������Ϣ��data����ο��뿴add_proxy����,��Ҫ�������proxyId�β�(�ֵ���)
        if not token:
            token=self.token
        header={
            "Authorization":"Bearer "+token
            }
        response=requests.post("https://api.mefrp.com/api/auth/proxy/update",headers=header,json=data)
        return json.loads(response.text)


    def toggle_proxy(self,proxyId:int,is_enable:bool,token:str=""):
        #���������״̬(���û��߽���)
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

        
        
r=MefrpClient(token="69991d99163647d686d79f7b6aab3fa9")
#print(r.toggle_proxy(64887,is_enable=True))
#print(r.update_proxy({"proxyId":64887,"loacalIp":"127.0.0.1","localPort":53244,"nodeId":73,"proxyName":"sbb","proxyType":"tcp","remotePort":23314,"useCompression":False,"useEncryption":False}))
print(r.list_domain())
'''
print(r.login(username="Archers",password="zqa#20120623"))
print("================================================")
print(r.update_proxy({"proxyId":64887,"loacalIp":"127.0.0.1","localPort":53244,"nodeId":73,"proxyName":"sbb","proxyType":"tcp","remotePort":23314,"useCompression":False,"useEncryption":False}))

r.add_proxy({"loacalIp":"127.0.0.1","localPort":25565,"nodeId":73,"proxyName":"test","proxyType":"tcp","remotePort":23314,"useCompression":False,"useEncryption":False})
time.sleep(1)
print(r.get_info())
print("================================================")
time.sleep(1)
print(r.get_ad())
print("================================================")
time.sleep(1)
print(r.get_notice())
print("================================================")
time.sleep(1)
print(r.sign())
print("================================================")
time.sleep(1)
print(r.proxy_list())
print("================================================")
time.sleep(1)
print(r.add_domain("mcfriends666.com"))

#print(r.get_free_port(NodeId=67,protocol="tcp")) 
#r.save_data({"token":"7403cad4f502861277744a2d5215a98f"},"chenge")
'''
           
