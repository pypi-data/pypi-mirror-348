from kcweb.common import *
from kcwebplus import config
kcwebpluspath=(os.path.split(os.path.realpath(__file__))[0]).replace('\\','/')[:-7] #框架目录
class kcwebplusdomain:
    def getbanddomain():
        """获取绑定域名
        """
        addtype='kcwebplus'
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            else:
                if len(lists):
                    webitem=lists[0]
                else:
                    webitem={}
                return True,webitem
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def banddomainall(domain,proxy_pass=[]):
        """绑定域名/修改多个代理
        
        domain 域名 必填 该方法生次使用时必填

        proxy_pass 代理信息 格式：[{'notes':'备注','types':'http','rule':'规则','url':'地址'}]
        """
        for k in proxy_pass:
            if not is_index(k,'notes') or not k['notes']:
                return False,'proxy_pass参数缺少notes'
            if not is_index(k,'types') or not k['types']:
                return False,'proxy_pass参数缺少types'
            if not is_index(k,'rule') or not k['rule']:
                return False,'proxy_pass参数缺少rule'
            if not is_index(k,'url') or not k['url']:
                return False,'proxy_pass参数缺少url'
        addtype='kcwebplus'
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            webitem={
                'id':'','log_switch':0,'domain':domain,'port':'80','title':'kcwebplus域名映射',
                'describes':'','path':'','webtpl':'balancing','client_max_body_size':20,
                'balancing':[{'ip':'127.0.0.1','port':'39001','type':'weight','val':1}],
                'proxy_set_header':[],'header':[],'aliaslists':[],'ssl':'','key':'','pem':'',
                'rewrite':'','ssl_certificate':'','ssl_certificate_key':'','other':{'phppath':'','proxy_pass':proxy_pass},'cusconfdata':'','denylist':[]
            }
            if len(lists):
                webitem=lists[0]
                if domain:
                    webitem['domain']=domain
                    webitem['other']={'phppath':'','proxy_pass':proxy_pass}
            status,msg=nginx.funadd_web(data=webitem,addtype=addtype)
            return status,msg
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def banddomain(proxyitem,domain=''):
        """绑定域名/增加代理
        
        proxyitem 代理信息 必填 格式：{'notes':'备注','types':'http','rule':'规则','url':'地址'} 

        domain 域名 非必填 该方法首次使用时该参数必填
        """
        if not is_index(proxyitem,'notes') or not proxyitem['notes']:
            return False,'proxyitem参数缺少notes'
        if not is_index(proxyitem,'types') or not proxyitem['types']:
            return False,'proxyitem参数缺少types'
        if not is_index(proxyitem,'rule') or not proxyitem['rule']:
            return False,'proxyitem参数缺少rule'
        if not is_index(proxyitem,'url') or not proxyitem['url']:
            return False,'proxyitem参数缺少url'
        addtype='kcwebplus'
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            if not len(lists):
                if not domain:
                    return False,'请绑定域名'
            webitem={
                'id':'','log_switch':0,'domain':domain,'port':'80','title':'kcwebplus域名映射',
                'describes':'','path':'','webtpl':'balancing','client_max_body_size':20,
                'balancing':[{'ip':'127.0.0.1','port':'39001','type':'weight','val':1}],
                'proxy_set_header':[],'header':[],'aliaslists':[],'ssl':'','key':'','pem':'',
                'rewrite':'','ssl_certificate':'','ssl_certificate_key':'','other':{'phppath':'','proxy_pass':[proxyitem]},'cusconfdata':'','denylist':[]
            }
            zx =False
            if len(lists):
                webitem=lists[0]
                if domain:
                    webitem['domain']=domain
                    zx=True
                add=True
                for k in webitem['other']['proxy_pass']:
                    if k['url']==proxyitem['url'] and k['rule']==proxyitem['rule']:
                        add=False
                if add:
                    webitem['other']['proxy_pass'].append(proxyitem)
                    zx=True
                # if proxyitem not in webitem['other']['proxy_pass']:
                #     webitem['other']['proxy_pass'].append(proxyitem)
                #     zx=True
            else:
                zx=True
            if zx:
                status,msg=nginx.funadd_web(data=webitem,addtype=addtype)
                return status,msg
            else:
                return True,'没有任何变化'
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def delproxy(proxyitem):
        """删除指定代理
        
        proxyitem 代理信息 必填 格式：{'rule':'规则','url':'地址'}
        """
        if not is_index(proxyitem,'rule') or not proxyitem['rule']:
            return False,'proxyitem参数缺少rule'
        if not is_index(proxyitem,'url') or not proxyitem['url']:
            return False,'proxyitem参数缺少url'
        addtype='kcwebplus'
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            if len(lists):
                webitem=lists[0]
                proxy_pass=webitem['other']['proxy_pass']
                proxy_passarr=[]
                for k in proxy_pass:
                    if k['url']!=proxy_pass['url'] and k['rule']!=proxy_pass['rule']:
                        proxy_passarr.append(k)
                webitem['other']['proxy_pass']=proxy_passarr
                status,msg=nginx.funadd_web(data=webitem,addtype=addtype)
                return status,msg
            else:
                return False,'未绑定域名'
        else:
            return False,'需要先在插件管理中安装“软件管理”'
    def delbnddomain():
        addtype='kcwebplus'
        if os.path.isfile('app/intapp/controller/soft/nginx.py'):
            nginx=getfunction('app.intapp.controller.soft.nginx')
            status,lists,count=nginx.weblist(pagenow=1,pagesize=1,kw='kcwebplus域名映射',addtype=addtype)
            if not status:
                return False,lists
            if len(lists):
                id=lists[0]['id']
                status,msg=nginx.del_nginx_web(id=id)
                return status,msg
            else:
                return True,'相关网站不存在'
        else:
            return False,'需要先在插件管理中安装“软件管理”'