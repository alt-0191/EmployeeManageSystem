from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import SQLAlchemyError

from backend.routes.getData import getdata
from backend.routes.modEmployees import modEmployees
from backend.routes.modUsers import modUsers

from config import Config
from backend.routes.auth import auth
from backend.models import db
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(getdata)
app.register_blueprint(modEmployees)
app.register_blueprint(modUsers)

jwt = JWTManager(app)
app.config.from_object(Config)

db.init_app(app)

# 跨域资源共享
CORS(app)


@app.route('/helloworld')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
            print("数据库连接成功并创建模型")
    except SQLAlchemyError as e:
        print("发生了SQLAlchemy错误:", e)
        raise SystemExit(1)

    finally:
        app.run(debug=True)
