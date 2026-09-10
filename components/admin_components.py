from fasthtml import common as c


class Pages:

    @staticmethod
    def create_company_page(message=None, message_type=None, name = ''):
        return c.Titled('Create Company',
                                   c.Div(
                                       c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
                                       c.Form (
                                             c.Label('Name: ', c.Input(type='text', name='name', value=name)),
                                              c.Br(),
                                              c.Br(),
                                         c.Button('Create Company', type='submit'),
                                         method='POST', action='/create-company'
                                     )))

   
    @staticmethod
    def admin_dashboard_page(message=None, message_type=None):
        return c.Titled('Dashboard',
                     c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P()),
                        c.P('Welcome to your dashboard!'),
                        c.Div(c.Form(c.Button('INVITE TO COMPANY', type = "submit"), method='GET', action='/invite-to-company')),
                        c.Div(c.Form(c.Button('CREATE TEAM', type='submit'), method='GET', action='/create-team')),
                        c.Div(c.Form(c.Button('DELETE TEAM', type = "submit"), method='GET', action='/delete-team')),
                        c.Div(c.Form(c.Button('ADD TO TEAM', type = "submit"), method='GET', action='/add-to-team')),
                        c.Div(c.Form(c.Button('REMOVE FROM TEAM', type = "submit"), method='GET', action='/remove-from-team')),
                        c.Div(c.Form(c.Button('ASSIGN TEAM LEADER', type = "submit"), method='GET', action='/assign-team-leader')),
                        c.Div(c.Form(c.Button('REMOVE TEAM LEADER', type = "submit"), method='GET', action='/remove-team-leader')),
                        c.Div(c.Form(c.Button('VIEW TEAMS', type = "submit"), method='GET', action='/view-teams'))
                        )

    