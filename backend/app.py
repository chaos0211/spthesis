from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes.auth import auth_bp
from routes.product import product_bp
from routes.order import order_bp
from routes.analytics import analytics_bp

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(product_bp, url_prefix='/api/product')
app.register_blueprint(order_bp, url_prefix='/api/order')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)