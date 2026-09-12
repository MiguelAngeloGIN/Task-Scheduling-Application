from fasthtml import common as c
from components.search_component import AutoSearch


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

    @staticmethod
    def single_field_form(message=None, message_type=None, title ='', action = '', value='', button = '', label = '', input_type='text'):
            return c.Titled(title,
                            c.Div(
                                c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
                                c.Form(
                                    c.Label(f'{label}: ', c.Input(type=input_type, name=label.lower().replace(' ', '_'), value=value)),
                                    c.Br(),
                                    c.Br(),
                                    c.Button(button, type='submit'),
                                    c.Br(),
                                    c.Br(),
                                    c.A('Back to dashboard', href='/admin-dashboard'),
                                    method='POST', action=action
                                )
                            )
                        )

    @staticmethod
    def invite_user_page(message=None, message_type=None, email=''):
        return Pages.single_field_form(
            message=message,
            message_type=message_type,
            title='Invite User to Company',
            action='/invite-to-company',
            value=email,
            button='Send Invitation',
            label = 'Email',
            input_type='email'
        )

    @staticmethod
    def create_team_page(message=None, message_type=None, team_name=''):
        return Pages.single_field_form(
            message=message,
            message_type=message_type,
            title='Create Team',
            action='/create-team',
            value=team_name,
            button='Create Team',
            label='Team Name'
        )

    @staticmethod
    def delete_team_page(message=None, message_type=None, team_name=''):
        return Pages.single_field_form(
            message=message,
            message_type=message_type,
            title='Delete Team',
            action='/delete-team',
            value=team_name,
            button='Delete Team',
            label='Team Name'
        )

    @staticmethod
    def accept_invite_page(message=None, message_type=None):
        return c.Div(
                    c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
                    c.A("Dashboard", href="/dashboard")
               )


    @staticmethod
    def user_team_page(message=None, message_type=None, warning = None, title='', action='', user_mode = 'select', team_mode = 'select_one'):
        return  c.Titled(title,
            c.Div(
                c.P(
                message,
                cls=message_type
        ) if message else "",

        c.P(warning, 
            cls= 'warning') if warning else '',

        c.Form(
            AutoSearch.render(
                form_id="add-team-form",
                hidden_input_id="user_id",
                entity="user",
                search_id="user-search",
                label='User email:',
                mode = user_mode,
            ),

            AutoSearch.render(
                 form_id="add-team-form",
                 hidden_input_id="team_id",
                 entity="team",
                 search_id="team-search",
                 label='Team:',
                 mode = team_mode
                   ),

            c.Button("Add to Team", type="submit"),
            c.A("Cancel", href="/admin-dashboard"),
            id="add-team-form",
            method="POST",
            action=action
        )
        )
        )

    
    
    