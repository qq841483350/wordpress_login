#coding:utf8
#使用些软件前请先安装插件python-wordpress-xmlrpc，安装方法pip install python-wordpress-xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
def wordpress_public(domain="如：www.domain.com ",username="后台登陆用户名",password='后台登陆密码',title='文章标题',content="文章内容" ,tags='标签,多个标签用逗号隔开如’标签1,标签2',category='分类名称'):
    import urllib,urllib2,cookielib,requests
    headers={
    "Host":"%s"%domain,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",}
    cookieJar=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    urllib2.install_opener(opener)
    login_data={
        "log":"%s"%username,
        "pwd":"%s"%password,
    }
    login_data=urllib.urlencode(login_data)
    login_url='http://%s/wp-login.php'%domain
    req=urllib2.Request(url=login_url,data=login_data,headers=headers)
    html=urllib2.urlopen(req).read()
    url='http://%s/wp-admin/edit.php?s=%s'%(domain,title)
    html=opener.open(url).read()
    if 'post-title page-title column-title' in html:
        print '标题已经已经存在,跳过不发布'.decode('utf8')
    else:
        tag=[]
        categorys=[]
        tag.append(tags)
        categorys.append(category)
        wp = Client('http://%s/xmlrpc.php'%domain, '%s'%username, '%s'%password) #登陆后台

        wp.call(GetPosts())
        wp.call(GetUserInfo())
        post = WordPressPost()
        post.title = """%s"""%title         #文章标题
        post.content = """%s"""%content  #文章内容
        post.terms_names = {
            'post_tag': tag,     #标签    如果有多个标签的话需要以列表形式，如： 'post_tag': ['eo ', 'discuz'],
            'category': categorys,   #分类    如果是有多个分类的话需要以列表形式，如：'category': ['Introductions', 'Tests']
        }
        post.post_status = 'publish'
        wp.call(NewPost(post))
        print '发布成功,标题是：'.decode('utf8'),title.decode('utf8')

if __name__=="__main__":
    domain="liyatao.com"  #域名如： liyatao.com
    username=""  #用户名
    password=""  #密码
    title="李亚涛SEO伪原创工具1"  #文章标题
    content="这是一个测试内容"   #文章内容
    tags='seo'   #文章关键词
    category="原创文章"  #文章分类
    wordpress_public(domain,username,password,title,content,tags,category)
