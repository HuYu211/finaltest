from flask import Flask
from controllers.api import route_api
from controllers.api.getToken import route_getToken


app = Flask(__name__)

app.register_blueprint(route_api,url_prefix='/api')
app.register_blueprint(route_getToken,url_prefix='/getToken')


@app.route('/')
def hello_world():
    return 'Chen Xi is zhuzhu'


if __name__ == '__main__':
    app.run( host="0.0.0.0",debug=True)
