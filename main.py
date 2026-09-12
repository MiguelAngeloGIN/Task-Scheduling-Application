from core.app import app, rt

import routes.auth_routes
import routes.task_routes
import routes.admin_routes
import routes.search_routes


@rt('/')
def root():
    return c.RedirectResponse('/signup', status_code = 302)


from fasthtml import common as c
c.serve()
