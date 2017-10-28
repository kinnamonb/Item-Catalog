from app import app


def application(environ, start_response):
    app.run()
