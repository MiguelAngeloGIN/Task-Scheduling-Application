from core.app import app, rt

import routes.auth_routes
import routes.task_routes
import routes.search_routes
import routes.admin.team_routes
import routes.dashboard_routes
import routes.admin.company_routes
import routes.admin.objective_routes

from fasthtml import common as c

@rt('/')
def root():
    return c.RedirectResponse('/auth/signup', status_code = 302)


c.serve()
