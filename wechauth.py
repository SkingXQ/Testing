# coding=utf-8
#!/usr/bin/python
"""script for redis with url interface
"""

from flask import Flask, request, json, abort, jsonify
from flask import Blueprint
from flask import render_template
import json
import urllib
import ssl

wechauth_blueprint = Blueprint("wechauth_blueprint", __name__)

# Static keys for auth
appid = "wxd12c0796d3ce9987"
appsecret = "eee9a01958979af6a339990d3b083c67"
token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
info_url = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN"

@wechauth_blueprint.route('/', methods=["GET", "POST"])
def index_page():
    """
    index page for auth
    """
    try:
        code = request.args.get('code')
        if code != "":
            context = ssl._create_unverified_context()
            token_info = urllib.urlopen(token_url.format(appid, appsecret, code), context=context).read()
            token_info = json.loads(token_info)
            user_info = urllib.urlopen(info_url.format(token_info['access_token'], \
                                                       token_info['openid']), context=context).read()
            user_info = json.loads(user_info) 
            print user_info
    except:
        return 'Authority fail'
    return render_template("index.html", user_info = user_info)

if __name__ == '__main__':
    app=Flask(__name__)
    app.debug = True
    app.register_blueprint(wechauth_blueprint)
    app.run(host = "45.78.62.125", port = 80)
