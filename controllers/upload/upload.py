from flask import Blueprint,request,jsonify,Flask,g
import re,json
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager
from common.models.Images import Image
route_upload = Blueprint('upload_page', __name__)

app=Flask(__name__)


@route_upload.route("/",methods = [ "GET","POST" ])
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
	g.imagepath = ret


	if ret['code'] != 200:
		resp['state'] = "上传失败：" + ret['msg']
		return jsonify(resp)

	resp['url'] = UrlManager.buildImageUrl( ret['data']['file_key'] )
	resp['data']['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
	return jsonify( resp )