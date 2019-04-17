from flask import request,jsonify,Flask,Blueprint,Flask,g
from config.DB import db
import requests,json
from common.models.Member import Member
from common.models.Oauth_member_bind import OauthMemberBind
from common.libs.helper import getCurrentDate
from common.libs.member.MemberService import MemberService
from common.models.Card import Card
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager

import re


route_api =Blueprint("api_page",__name__)

app=Flask(__name__)
@route_api.route("/")
def index():
    return "test"

@route_api.route("/member/login",methods = ["GET","POST"])
def login( ):
    resp = {'code':200,'msg':'操作成功~','data':{}}
    req = request.values
    # app.logger.info( req )
    code = req['code'] if 'code' in req else ''
    if not code or len(code)<1:
        resp['code'] = -1
        resp['msg'] ="需要code"
        return jsonify(resp)

    openid= MemberService.getWeChatOpenId( code )
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickname'] if 'nickname' in req else ''
    sex = req['gender'] if 'gender' in req else ''
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    # app.logger.info( req )

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}

    return jsonify(resp)

@route_api.route("/member/check-reg",methods = ["GET","POST"])
def checkReg( ):
    resp = {'code':200,'msg':'操作成功~','data':{}}
    req = request.values

    code = req['code'] if 'code' in req else ''
    if not code or len(code)<1:
        resp['code'] = -1
        resp['msg'] ="需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)
    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    token = "%s#%s"%( MemberService.geneAuthCode( member_info ), member_info.id )
    resp['data'] = { 'token':token }
    return jsonify(resp)

@route_api.route("/card/index",methods = ["GET","POST"])
def noteIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    # app.logger.info(req)
    id = req['uid'] if 'uid'in req else ''
    if not id or len(id)<1:
        resp['code'] = -1
        resp['msg'] ="需要id"
        return jsonify(resp)

    card_list = Card.query.filter_by(status=0,member_id=id).order_by(Card.created_time.asc()).all()
    data_card_list = []
    # data_card_list.append({
    #     'id': 0,
    #     'card_name': "first_card",
    #     'member_id': 3,
    #     'card_comment':"记忆曲线4/14次复习",
    #     'peview_time':"应在1小时后复习",
    #     'current_date':"2019/4/13",
    # })
    if card_list:
        for item in card_list:
            tmp_data = {
                'id': item.id,

                'card_name': item.card_name,
                'card_comment':item.study_status,
                'peview_time':"应在1小时后复习",
                'current_date':item.created_time
            }
            data_card_list.append(tmp_data)
    resp['data']['card_list'] = data_card_list
    resp['data']['count'] = Card.query.filter_by(status=0).order_by(Card.id.desc()).count()
    return jsonify(resp)

@route_api.route("/card/show",methods = ["GET","POST"])
def cardshow():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    app.logger.info(req)
    card_id = req['card_id'] if 'card_id' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "需要card_id"
        return jsonify(resp)

    card_list1 = Card.query.filter_by(id=card_id).order_by(Card.created_time.asc()).all()

    if card_list1:
        for item in card_list1:
            resp['data'] = {
                'card_name':item.card_name,
                'card_content': item.card_content
             }

            print(item.card_content)
    return jsonify(resp)


@route_api.route("/upload",methods = [ "GET","POST" ])
def uploadImage():
	resp = { 'state':'SUCCESS','url':'','title':'','original':'' ,'data':{} }
	req = request.values
	id = req['id'] if 'id' in req else ''

	if id is None:
		resp['state'] = "id获取失败"
		return jsonify(resp)

	file_target = request.files
	upfile = file_target['file'] if 'file' in file_target else None
	if upfile is None:
		resp['state'] = "上传失败"
		return jsonify(resp)


	ret = UploadService.uploadByFile( upfile,id )



	if ret['code'] != 200:
		resp['state'] = "上传失败：" + ret['msg']
		return jsonify(resp)

	resp['url'] = UrlManager.buildImageUrl( ret['data']['file_key'] )
	resp['data']['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
	return jsonify( resp )

@route_api.route("/card/inset",methods = ["GET","POST"])
def cardinset():
    resp = {'code':200,'msg':'操作成功~','data':{}}
    req = request.values
    app.logger.info(req)
    member_id = req['uid'] if 'uid' in req else ''
    card_name = req['name'] if 'name' in req else ''
    card_content = req['content'] if 'content' in req else ''
    fromid = req['fromid'] if 'fromid' in req else ''

    # model_card = Card()
    # model_card.member_id = member_id
    # model_card.card_name = card_name
    # model_card.card_content = "<view class='weui-article__p'>" + card_content + "</view></view><view> <image  src="
    # model_card.fromid = fromid
    # db.session.add(model_card)
    # db.session.commit()
    # a= uploadImage.imagepath


    return jsonify(resp)
