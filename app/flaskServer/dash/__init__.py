from flask import request, render_template
from .admin import init_admin
from .graphing import init_graphing
from datetime import date

def init_dash( app ):
    

    init_admin(app)
    init_graphing( app )


    