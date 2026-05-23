from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    
    CORS(app)
    
    from app.routes.auth import auth_bp
    from app.routes.gradients import gradients_bp
    from app.routes.plaza import plaza_bp
    from app.routes.favorites import favorites_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(gradients_bp)
    app.register_blueprint(plaza_bp)
    app.register_blueprint(favorites_bp)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '接口不存在'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': '服务器内部错误'}), 500
    
    return app
