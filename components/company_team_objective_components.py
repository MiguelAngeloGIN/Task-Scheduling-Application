from fasthtml import common as c

from components.search_component import AutoSearch


class Pages:

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
    def double_field_form(message=None, message_type=None, title ='', action = '', value1='', value2='',name1='', name2='', 
                          button = '', label1 = '', label2 = '', input_type='text', ):
        return c.Titled(title,
                        c.Div(
                            c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
                            c.Form(
                                c.Label(f'{label1}: ', c.Input(type=input_type, name=name1, value=value1)),
                                c.Br(),
                                c.Br(),
                                c.Label(f'{label2}: ', c.Input(type=input_type, name=name2, value=value2)),
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
    def admin_objective_toggle(active = "admin"):
          return c.Div(
                 c.A(
                        'Admin dashboard', href="/admin-dashboard",
                          cls="toggle-option active" if active == "admin" else "toggle-option"
                 ),
                 c.A(
                        'Objectives Dashboard', href="/objective-dashboard",
                          cls="toggle-option active" if active == "objectives" else "toggle-option"
                 ),
                 cls = "admin_dashboard-toggle"
                 )


    @staticmethod
    def create_company_page(message=None, message_type=None, name=''):
          return Pages.single_field_form(
               message=message,
               message_type=message_type,
               title='Create Company',
               action='/admin/company/create',
               value=name,
               button='Create Company',
               label='Company Name'
            )


    @staticmethod
    def create_objective_page(message=None, message_type=None, name='', description=''):
          return Pages.double_field_form(
               message=message,
               message_type=message_type,
               title='Create Objective',
               action='/admin/objective/create',
               value1=name,
               value2=description,
               button='Create Objective',
               name1='objective_name',
               name2='description',
               label1='Objective Name',
               label2='Description'
            )


    @staticmethod
    def create_team_page(message=None, message_type=None, team_name=''):
            return Pages.single_field_form(
                message=message,
                message_type=message_type,
                title='Create Team',
                action='/admin/team/create',
                value=team_name,
                button='Create Team',
                label='Team Name'
            )


    @staticmethod
    def deactivate_team_page(message=None, message_type=None, team_name=''):
            return Pages.single_field_form(
                message=message,
                message_type=message_type,
                title='Deactivate Team',
                action='/admin/team/deactivate',
                value=team_name,
                button='Deactivate Team',
                label='Team Name'
            )


    @staticmethod
    def archive_objective_page(message=None, message_type = None, name=''):
          return Pages.single_field_form(
                        message=message,
                        message_type=message_type,
                        title=' Objective',
                        action='/admin/objective/archive',
                        value=name,
                        button='Archive Objective',
                        label='Objective Name'
                     )


    @staticmethod
    def objective_dashboard_page(message=None, message_type = None):
         return c.Titled('Objective dashboard',
                         c.Div(Pages.admin_objective_toggle(active = 'objective')),
                         c.Div(c.P(f'{message}', cls = f"message {message_type}") if message else ""),
                         c.Div(c.Form(c.Button('CREATE OBJECTIVE', type='submit'), method = 'GET', action='/admin/objective/create')),
                         c.Div(c.Form(c.Button('ARCHIVE OBJECTIVE', type='submit'), method = 'GET', action='/admin/objective/archive')),
                         c.Div(c.Form(c.Button('VIEW OBJECTIVES SCHEDULE', type='submit'), method = 'GET', action='/admin/objective/view')))
                         
   
    @staticmethod
    def admin_dashboard_page(message=None, message_type=None):
        return c.Titled('Dashboard',
                        c.Div(Pages.admin_objective_toggle(active = 'admin')),
                        c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else ""),
                        c.P('Welcome to your dashboard!'),
                        c.Div(c.Form(c.Button('Logout', type='submit'), method='POST', action='/auth/logout')),
                        c.Div(c.Form(c.Button('INVITE TO COMPANY', type = "submit"), method='GET', action='/admin/company/invite')),
                        c.Div(c.Form(c.Button('CREATE TEAM', type='submit'), method='GET', action='/admin/team/create')),
                        c.Div(c.Form(c.Button('ADD TO TEAM', type = "submit"), method='GET', action='/admin/team/add')),
                        c.Div(c.Form(c.Button('REMOVE FROM TEAM', type = "submit"), method='GET', action='/admin/team/remove')),
                        c.Div(c.Form(c.Button('ASSIGN TEAM LEADER', type = "submit"), method='GET', action='/admin/team/assign-leader')),
                        c.Div(c.Form(c.Button('REMOVE TEAM LEADER', type = "submit"), method='GET', action='/admin/team/remove-leader')),
                        c.Div(c.Form(c.Button('VIEW TEAMS', type = "submit"), method='GET', action='/admin/team/view'))
                        )

    
    @staticmethod
    def invite_user_page(message=None, message_type=None):

         return c.Titled(
        "Invite User to Company",

        c.Div(
            c.P(f'{message}', cls=f"message {message_type}") if message else ""
        ),

        c.Form(
            AutoSearch.render(
                form_id="invite-form",
                hidden_input_id="user_id",
                entity="all-users",
                search_id="user-search",
                label="User email:",
                mode="select_one"
            ),

            c.Button("Send Invitation", type="submit"),

            c.A("Back to dashboard", href="/admin-dashboard"),

            id="invite-form",
            method="POST",
            action="/admin/company/invite"
        )
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

    @staticmethod
    def manage_objectives_page(message=None, message_type=None):
        return c.Titled("Manage Objectives",
            c.Div(
                    c.P(f'{message}', cls=f"message {message_type}") if message else "",

                    c.Form(
                          AutoSearch.render(
                              form_id="manage-objectives-form",
                              hidden_input_id="objective_id",
                              entity="company-objectives",
                              search_id="objective-search",
                              label="Objective:",
                              mode="select_one"
                          )
                    ),
                    c.A("Dashboard", href="/objective-dashboard")
               )
        )



    @staticmethod
    def view_teams_page(teams, message=None, message_type=None):

         team_cards = []

         for team in teams:

               members = [
                     c.Li(
                           f"{member.user.first_name} {member.user.last_name}"
                           )

               for member in team.team_members ]

               if not members:
                    members = [c.Li("No members")]

               team_cards.append(
                     c.Div(
                     c.H3(team.name),
                     c.P("Members:"),
                     c.Ul(*members),
                    cls="team-card",
                    data_team_name=team.name.lower()
            )
        )

         return c.Titled("View Teams", c.A("Dashboard", href="/admin-dashboard"),
                         c.Div(c.P(message, cls=f"message {message_type}") if message else ""),
                              c.Div(
                              c.Input(
                                     id="team-filter",
                                     placeholder="Search teams by name..."
                                     ),
                                     id="team-search-container" ),

                         c.Div(*team_cards, id="team-list"),

                         AutoSearch.filter_script())


    @staticmethod
    def view_objectives_page(objectives, progress, message=None, message_type=None):

         objective_cards = []

         for objective in objectives:
               objective_progress = progress[objective.objective_id]

               objective_cards.append(
                  c.A(
                      c.H3(objective.name),

                    #  c.Div(
                    #  c.P(f"{objective_progress}%"),cls="progress-circle"
                    # ),

                    c.P(f"Progress: {objective_progress}%"),

                    href=f"/task/view-schedule/{objective.objective_id}",
                    cls="objective-card",
                    data_objective_name=objective.name.lower()
                     )
            )
        

         return c.Titled("View Objectives", c.A("Dashboard", href="/admin-dashboard"),
                         c.Div(c.P(message, cls=f"message {message_type}") if message else ""),
                              c.Div(
                              c.Input(
                                     id="objective-filter",
                                     placeholder="Search objectives by name..."
                                     ),
                                     id="objective-search-container" ),

                         c.Div(*objective_cards, id="objective-list"),

                         AutoSearch.filter_script())


    
    
    