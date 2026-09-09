from fasthtml import common as c
from routes import auth_routes, task_routes
from core.app import app, rt


@rt('/')
def get():
    return c.RedirectResponse('/signup', status_code=302)


c.serve()




