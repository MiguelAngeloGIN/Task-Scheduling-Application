from fasthtml import common as c
class Pages:
    @staticmethod
    def signup_page(message=None, message_type=None, first_name='', last_name='', email='', action = '/signup'):

        company_signup = action == '/company-signup'

        return c.Titled('Sign Up',
                                   c.Div(
                                       c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),

                                       c.A('Sign up as an employee' if company_signup else 'Sign up as a company',
                                            href='/signup' if company_signup else '/admin-signup'),

                                       c.P('Please fill out the form below to sign up.'),
                                       
                                       c.Form (
                                             c.Label('First Name: ', c.Input(type='text', name='first_name', value=first_name)),
                                             c.Br(),
                                             c.Label('Last Name: ', c.Input(type='text', name='last_name', value=last_name)),
                                             c.Br(),
                                              c.Br(),
                                         c.Label('Email: ', c.Input(type='email', name='email', value=email)),
                                         c.Br(),
                                         c.Label('Password: ', c.Input(type='password', name='password')),
                                         c.Br(),
                                         c.Button('Sign Up', type='submit'),
                                         c.P('Already have an account? ', c.A('Log in here', href='/login')),
                                         method='POST', action=action
                                     )))

    @staticmethod
    def login_page(message=None, message_type=None, email=''):
        return c.Titled('Log In',
                           c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
                           c.P('Please enter your credentials to log in.'),
                                 c.Form(
                                     c.Label('Email: ', c.Input(type='email', name='email', value=email)),
                                     c.Br(),
                                     c.Label('Password: ', c.Input(type='password', name='password')),
                                     c.Br(),
                                     c.Button('Log In', type='submit'),
                                     c.P("Don't have an account? ", c.A('Sign up here', href='/signup')),
                                     c.P('Forgot your password?', c.A ('Reset your password', href = '/reset-password')),
                                        method='POST', action='/login'
                                 )
                           )
                           )
                        

    @staticmethod
    def reset_password_page(message=None, message_type=None):
        return c.Titled('Reset Password',
                                   c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P() ,
                                   c.P('Please enter your email.'),
                                         c.Form(
                                             c.Label('Email: ', c.Input(type='email', name='email')),
                                             c.Br(),
                                             c.Br(),
                                             c.Button('Reset Password', type='submit'),
                                             c.P(c.A('Login', href='/login')),
                                                method='POST', action='/reset-password'))
                                   )
        
    @staticmethod
    def paste_token_page(message=None, message_type=None, email=''):
        return c.Titled('Paste Token',
                                   c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P() ,
                                   c.P('Please paste the token you received in your email.'),
                                         c.Form(
                                             c.Label('Token: ', c.Input(type='text', name='token')),
                                             c.Input(type="hidden", name="email", value=email),
                                             c.Br(),
                                             c.Br(),
                                             c.Button('Submit Token', type='submit'),
                                                method='POST', action='/paste-token'))
                                   )

    @staticmethod
    def new_password_page(message=None, message_type=None, email='', token=''):
        return c.Titled('New Password',
                                   c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P() ,
                                   c.P('Please enter your new password.'),
                                         c.Form(
                                             c.Label('New Password: ', c.Input(type='password', name='new_password')),
                                             c.Input(type="hidden", name="email", value=email),
                                             c.Input(type="hidden", name="token", value=token),
                                             c.Br(),
                                             c.Br(),
                                             c.Button('Submit New Password', type='submit'),
                                                method='POST', action='/new-password'))
                                   )



    