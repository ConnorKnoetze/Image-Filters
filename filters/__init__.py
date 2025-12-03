def create_app():
    from flask import Flask
    import os

    app = Flask(__name__)

    # Auto-reload templates and avoid static file caching in dev
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    from filters.blueprints.index.index import index_bp
    app.register_blueprint(index_bp)
    from filters.blueprints.filter_types.pixelate.pixelate import pixelate_bp
    app.register_blueprint(pixelate_bp)
    from filters.blueprints.upload.upload import upload_bp
    app.register_blueprint(upload_bp)

    return app