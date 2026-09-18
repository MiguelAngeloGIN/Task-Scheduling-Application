from fasthtml import common as c

app, rt = c.fast_app(live=True,
                     static_path=".",
                     hdrs=(
                         c.Link(rel="stylesheet", href="/css/main.css"),

                     )
                 )

print("Application created")