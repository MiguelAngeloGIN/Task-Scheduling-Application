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