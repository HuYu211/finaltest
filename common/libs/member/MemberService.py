import hashlib,requests,random,string,json
from flask import Flask


app=Flask(__name__)

class MemberService():

    @staticmethod
    def geneAuthCode( member_info = None ):
        m = hashlib.md5()
        str = "%s-%s-%s" % ( member_info.id, member_info.salt,member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt( length = 16 ):
        keylist = [ random.choice( ( string.ascii_letters + string.digits ) ) for i in range( length ) ]
        return ( "".join( keylist ) )

    @staticmethod
    def getWeChatOpenId(code):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format('wx77d7fc3ff2569cb6','1e7e661c85191405ab9674634c0efd5c', code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid