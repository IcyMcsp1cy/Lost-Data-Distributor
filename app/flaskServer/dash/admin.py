from flask import render_template, abort, request, redirect, url_for, session, g
from dash import Dash, callback_context
from flask_login import current_user
import dash_core_components as dcc
import dash_html_components as html
from dash_bootstrap_components import Alert, Card, CardBody, Button
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
from flask_wtf.recaptcha.widgets import JSONEncoder
from pandas.core.frame import DataFrame
import pandas as pd
import dash_table
from julian import to_jd
from datetime import date, datetime
from bson.objectid import ObjectId
from .graphing import rv_plot
from ..extensions import JSONEncoder, collection, sendMail, mongo
from ..config import csv_label
from pymongo import DESCENDING 


url_base = "/admin/"

empty_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-wrapper')
])


file_manager = html.Div([
    html.H1('File Management', className='mb-2'),

    dcc.Loading([
        html.P([

            'Set public/private access date:\n',
        ]),
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
        ),
        html.Button('Submit', id='date-submit', className='btn mx-2'),
        html.Br(),
        html.Div(className='', id='file-alert'),
    ], id='date-loader'),
    html.Br(),
])


glos_manager = html.Div([
    html.H1('Glossary Management', className='mb-2'),
    html.Br(),
    dcc.Input(
        id="glos-term",
        type='text',
        placeholder="Glossary Term (Naming a term after another will replace that term)",
        className='w-75 form-control mb-2'
    ),
    dcc.Textarea(
        id='glos-text',
        placeholder='Definition',
        style={'height': 50},
        className='input-group w-75 form-control pb-2'
    ),
    html.Button('Submit', id='glos-submit', className='btn my-2'),
    html.Button('Delete', id='glos-delete', className='btn my-2 mx-2 d-none'),
    html.Div(className='', id='glos-alert'),
    html.Div(className='', id='glos-alert-2'),
    html.Br()
], className='mb-4')



user_manager = html.Div([
    html.H1('User Management', className='mb-2'),
    html.Br(),
    html.Div([
        html.P('', className="d-none", id='user-email'),
    ], id='user-display'),
    Button('Verify', id='user-verify', className='btn my-2 mx-2 d-none', color='success'),
    Button('Reject', id='user-reject', className='btn my-2 mx-2 d-none', color='danger'),
    html.Br(),
    html.Div([
        Button('Purge Unverified Users', id='user-purge', className='btn my-2 mx-2', color='warning'),
    ],className='text-right', id='user-control'),
    html.Div(className='', id='user-alert'),
    
], className='mb-4')



news_manager = html.Div([
    html.H1('News Management', className='mb-2'),
    html.Br(),
    dcc.Input(
        id="news-title",
        type='text',
        placeholder="Post Title (Naming a post after another will replace that post)",
        className='w-75 form-control mb-2'
    ),
    dcc.Input(
        id="news-subtitle",
        type='text',
        placeholder="Subtitle",
        className='w-75 form-control mb-2'
    ),
    dcc.Input(
        id="news-author",
        type='text',
        placeholder="Author",
        className='w-50 form-control mb-2'
    ),
    dcc.Textarea(
        id='news-text',
        placeholder='Lorem Ipsum Dolor',
        style={'height': 100},
        className='input-group w-100 form-control pb-2'
    ),
    Button('Submit', id='news-submit', className='btn my-2', n_clicks=0, color='success'),
    Button('Delete', id='news-delete', className='btn my-2 mx-2 d-none', n_clicks=0, color='danger'),
    Button('Set on Homepage', id='news-home', className='btn my-2 mx-2 d-none', n_clicks=0, color='secondary'),
    html.Div(className='', id='news-alert'),
    html.Div(className='', id='news-alert-2'),
    html.Br()
], className='mb-4')



def getFiles():
    one = list(collection('one').files.find({}))
    for i in one:
        i['filetype'] = '1d'
    two= list(collection('one').files.find({}))
    for i in two:
        i['filetype'] = '2d'
    sort = sorted(one+two, key=lambda k: k['uploadDate'], reverse=True)
    df = pd.DataFrame(eval(JSONEncoder().encode(sort)))
    
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {'id': 'filename', 'name': 'File Name'},
            {'id': 'filetype', 'name': 'Type'},
            {'id': 'uploadDate', 'name': 'Date'},
        ],
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Date', 'Region']
        ],
        style_as_list_view=True,
        id='file-table'
    )
    return [file_manager, table]


def getGlos():
    glos = list(collection('glossary').find({}))
    df = pd.DataFrame(eval(JSONEncoder().encode(glos)))
    
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {'id': 'entry', 'name': 'Entry'},
            {'id': 'definition', 'name': 'Definition'},
            {'id': 'datetime', 'name': 'Date'},
        ],
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['entry', 'definition']
        ],
        style_as_list_view=True,
        id='glos-table',
    )
    return [glos_manager, table,]



def getUser():
    users = list(collection('user').find({}).sort('_id', DESCENDING))
    df = pd.DataFrame(eval(JSONEncoder().encode(users)))
    
    table = dash_table.DataTable(
        data=df[['firstName', 'lastName', 'email', 'institution', 'type']].to_dict('records'),
        columns=[
            {'id': 'firstName', 'name': 'First'},
            {'id': 'lastName', 'name': 'Last'},
            {'id': 'email', 'name': 'Email'},
            {'id': 'institution', 'name': 'Institution'},
            {'id': 'type', 'name': 'Type'},
        ],
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[  
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['lastName', 'institution']
        ]+[
            {   
                'if': {
                    'filter_query': '{type} = "unverified"',
                },
                'color': '#ffc107',
                'fontWeight': 'bold'
            },  
            {   
                'if': {
                    'row_index': -1,
                    'column_id': 'type'
                },
                'backgroundColor': 'black'
            },  
        ],
        style_as_list_view=True,
        id='user-table',
    )
    return [user_manager, table,]


def getNews():
    news = list(collection('news').find({}))
    df = pd.DataFrame(eval(JSONEncoder().encode(news)))

    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {'id': 'title', 'name': 'Post Title'},
            {'id': 'author', 'name': 'Author'},
            {'id': 'datetime', 'name': 'Date'},
        ],
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['title', 'author']
        ],
        style_as_list_view=True,
        id='news-table',
    )
    return [news_manager, table,]



def init_admin( server ):

    app = Dash(
    '__main__',
    server=server,
    url_base_pathname=url_base,
    assets_folder='static',
    )

    @server.before_request
    def adminDash():
        if str(request.endpoint).startswith(url_base):
            app.index_string = render_template('admin.html')
            if current_user.is_authenticated:
                if current_user.accountType == 'admin':
                    return
                abort(403)
            return redirect('/login')

    app.layout = empty_layout


    @app.callback(
        Output('page-wrapper', 'children'),
        Input('url', 'pathname'))
    def display_page(pathname):
        if pathname == url_base + 'news':
            return getNews()
        elif pathname == url_base + 'glossary':
            return getGlos()
        elif pathname == url_base + 'files':
            return getFiles()
        else:
            return getUser()


    @app.callback(
        Output('glos-term', 'value'),
        Output('glos-text', 'value'),
        Output('glos-delete', 'className'),
        Input('glos-table', 'data'),
        Input('glos-table', 'active_cell'),
    )
    def selectGlos(data, cell):
        if cell and data and len(data) > cell['row']:
            record = data[cell['row']]
            return record['entry'], record['definition'], 'btn my-2 mx-2'
        raise PreventUpdate


    @app.callback(
        Output('glos-alert', 'children'),
        Output('glos-table', 'data'),
        Input('glos-submit', 'n_clicks'),
        Input('glos-delete', 'n_clicks'),
        State('glos-term', 'value'),
        State('glos-text', 'value'),
        State('glos-table', 'data'))
    def editGlos(submit, delete, term, definition, table):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'glos-submit' in changed_id:
            for val in [term, definition]:
                if val is None or val == '':
                    return Alert(
                        "Please fill out all fields",
                        id="alert-auto",
                        is_open=True,
                        duration=10000,
                        color='danger'
                    ), table.to_dict('records')
            entry = collection('glossary').find_one({'entry': term}) 
            if(entry):
                collection('glossary').replace_one(
                    {'_id': entry['_id']},
                    {
                        '_id': entry['_id'],
                        'entry': term,
                        'definition': definition,
                        'datetime': datetime.now()
                    }
                )
            else:
                entry = {
                    '_id': ObjectId(),
                    'entry': term,
                    'definition': definition,
                    'datetime': datetime.now()
                }

                collection('glossary').insert_one(
                    {
                        '_id': entry['_id'],
                        'entry': term,
                        'definition': definition,
                        'datetime': datetime.now()
                    })
            
            glos = list(collection('glossary').find({}))
            df = pd.DataFrame(eval(JSONEncoder().encode(glos)))

            return Alert(
                ["Glossary Updated"],
                id="alert-auto",
                is_open=True,
                duration=10000,
            ), df.to_dict('records')
        elif 'glos-delete' in changed_id:
            result = collection('glossary').find_one({'entry': term})
            if(result):
                collection('glossary').delete_one(
                    {'_id': result['_id']}
                )
                alert = Alert([
                    "Post Deleted"
                    ],
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                )
            else:
                alert = Alert(
                    "Post does not exist",
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                    color='danger'
                )
            news = list(collection('glossary').find())
            df = pd.DataFrame(eval(JSONEncoder().encode(news)))
            return alert, df.to_dict('records')
        else:
            raise PreventUpdate

            
    @app.callback(
        Output('news-title', 'value'),
        Output('news-subtitle', 'value'),
        Output('news-author', 'value'),
        Output('news-text', 'value'),
        Output('news-delete', 'className'),
        Output('news-home', 'className'),
        Input('news-table', 'data'),
        Input('news-table', 'active_cell'))
    def selectNews(data, cell):
        if cell and data and len(data) > cell['row']:
            record = data[cell['row']]
            return record['title'], record['subtitle'], record['author'], record['content'], 'btn my-2 mx-2', 'btn my-2 mx-2'
        raise PreventUpdate


    @app.callback(
        Output('news-alert', 'children'),
        Output('news-table', 'data'),
        Input('news-submit', 'n_clicks'),
        Input('news-delete', 'n_clicks'),
        Input('news-home', 'n_clicks'),
        State('news-title', 'value'),
        State('news-subtitle', 'value'),
        State('news-author', 'value'),
        State('news-text', 'value'),
        State('news-table', 'data'))
    def editNews(submit, delete, home, title, subtitle, author, text, table):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'news-submit' in changed_id:
            for val in [title, subtitle, author, text]:
                if val is None or val == '':
                    return Alert(
                        "Please fill out all fields",
                        id="alert-auto",
                        is_open=True,
                        duration=10000,
                        color='danger'
                    ), table.to_dict('records')

            post = collection('news').find_one({'title': title})

            if(post):
                collection('news').replace_one(
                    {'_id': post['_id']},
                    {
                        '_id': post['_id'],
                        'title': title,
                        'subtitle': subtitle,
                        'author': author,
                        'content': text,
                        'datetime': datetime.now().strftime('%B %d, %Y')
                    }
                )
            else:
                post = {
                    '_id': ObjectId(),
                    'title': title,
                    'subtitle': subtitle,
                    'author': author,
                    'content': text,
                    'datetime': datetime.now().strftime('%B %d, %Y')
                }

                collection('news').insert_one(post)

            url = url_for('post', post_id=str(post['_id']))
            
            news = list(collection('news').find({}))
            df = pd.DataFrame(eval(JSONEncoder().encode(news)))

            return Alert([
                "Article posted to ",
                html.A("this link", href=url, className="alert-link")
                ],
                id="alert-auto",
                is_open=True,
                duration=10000,
            ), df.to_dict('records')

        elif 'news-delete' in changed_id:
            post = collection('news').find_one({'title': title})
            if(post):
                collection('news').delete_one(
                    {'_id': post['_id']}
                )
                alert = Alert([
                    "Post Deleted"
                    ],
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                )
            else:
                alert = Alert(
                    "Post does not exist",
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                    color='danger'
                )
            news = list(collection('news').find().sort('datetime', DESCENDING))
            df = pd.DataFrame(eval(JSONEncoder().encode(news)))
            return alert, df.to_dict('records')
        elif 'news-home' in changed_id:
            post = collection('news').find_one({'title': title})
            if(post):
                home = collection('news').find_one({'location': 'home'})
                if(home): collection('news').update_one({'location': 'home'}, {'$set': {'location': 'default'}}, True)
                collection('news').update_one({'_id': post['_id']}, {'$set': {'location': 'home'}}, True)
                alert = Alert([
                    "Post set as home"
                    ],
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                )
            else:
                alert = Alert(
                    "Post does not exist",
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                    color='danger'
                )
            news = list(collection('news').find().sort('datetime', DESCENDING))
            df = pd.DataFrame(eval(JSONEncoder().encode(news)))
            return alert, df.to_dict('records')
        else:
            raise PreventUpdate



    @app.callback(
        Output('user-display', 'children'),
        Output('user-verify', 'className'),
        Output('user-reject', 'className'),
        Input('user-table', 'data'),
        Input('user-table', 'active_cell'),
    )
    def selectUser(data, cell):
        if cell and data and len(data) > cell['row']:
            record = data[cell['row']]
            type = record['type']
            color = 'secondary'
            dNone = ' d-none'
            if type == 'unverified':
                color = 'warning'
                dNone = ''
            elif type == 'researcher':
                color='primary'
            elif type == 'admin':
                color='danger'
            #'btn my-2 mx-2'
            return Card([
                    CardBody(
                        [
                            
                            html.H4(record['firstName']+" "+record['lastName'],
                                className="card-title text-"+color),
                            html.H6(record['institution'], className="card-subtitle"),
                            html.P(
                                record['email'],
                                className="card-text",
                                id='user-email'
                            ),
                            html.B(
                                "Unverified" if record['type'] == 'unverified' else record['type'],
                                className="card-text",
                            ),
                        ]
                    )],
                    style={"width": "18rem"},
                    className='border border-5 border-' + color
                ), 'btn my-2 mx-2'+dNone, 'btn my-2 mx-2'+dNone
        raise PreventUpdate


    @app.callback(
        Output('user-alert', 'children'),
        Output('user-table', 'data'),
        Output('user-display', 'className'),
        Input('user-verify', 'n_clicks'),
        Input('user-reject', 'n_clicks'),
        Input('user-purge', 'n_clicks'),
        Input('user-table', 'active_cell'),
        State('user-email', 'children'),
        State('user-table', 'data'))
    def editUser(verify, reject, purge, active, email, table):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        df_table = DataFrame(table)
        if 'user-verify' in changed_id:
            if email is None or email == '':
                return Alert(
                    "Please select user",
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                    color='danger'
                ), df_table.to_dict('records'), ''
                    

            entry = collection('user').find_one({'email': email})
            
            if(entry):
                collection('user').update_one(
                    {'_id': entry['_id']},
                    {"$set": 
                        {'type': 'researcher'}
                    }
                )
            else:
                return Alert(
                    "Please select user",
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                    color='danger'
                ), df_table.to_dict('records'), ''

            fullname = entry['firstName'] + ' ' + entry['lastName']
            messageBody = "Hello, " + fullname + " has been granted researcher access for the LOST telescope.\n" + (
                "Email: " + entry['email']+ "\nInstitution: " + entry['institution'] + "\n\nThis is your generated password:\n\n"
                + entry['password'])

                
            sendMail(entry['email'], "Database Access Granted to " + fullname,
            messageBody)

            result = list(collection('user').find({}).sort('_id', DESCENDING))
            df = pd.DataFrame(eval(JSONEncoder().encode(result)))

            return Alert(
                ["User Verified"],
                id="alert-auto",
                is_open=True,
                duration=10000,
            ), df.to_dict('records'), ''
        elif 'user-reject' in changed_id:
            result = collection('user').find_one({'email': email})
            if(result):
                collection('user').delete_one(
                    {'_id': result['_id']}
                )
                alert = Alert([
                    "User Rejected"
                    ],
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                )
            else:
                alert = Alert(
                    "User does not exist",
                    id="alert-auto",
                    is_open=True,
                    duration=10000,
                    color='danger'
                )
            news = list(collection('user').find().sort('_id', DESCENDING))
            df = pd.DataFrame(eval(JSONEncoder().encode(news)))
            return alert, df.to_dict('records'), 'd-none'

        elif 'user-purge' in changed_id:
            removed = collection('user').remove({'type': 'unverified'})
            news = list(collection('user').find().sort('_id', DESCENDING))
            df = pd.DataFrame(eval(JSONEncoder().encode(news)))
            return Alert(
                "Applicants Deleted",
                id="alert-auto",
                is_open=True,
                duration=10000,
                color='danger'
            ), df.to_dict('records'), ''
        elif 'user-table' in changed_id:
            return '', df_table.to_dict('records'), ''
        else:
            raise PreventUpdate

            

    @app.callback(
        Output('file-alert', 'children'),
        Input('date-submit', 'n_clicks'),
        State('date-picker', 'date'))
    def update_output(submit, date_value):
        string_prefix = 'You have selected: '
        if date_value is not None:
            date_object = datetime.fromisoformat(date_value)
            setDate = to_jd(date_object, fmt='mjd')
            date_string = date_object.strftime('%B %d, %Y')

            entries = list(collection('radialvelocity').find())
            for entry in entries:
                collection('radialvelocity').update_one(
                    {'_id': entry['_id']},
                    {
                        '$set': {
                            'PUBLIC': (float(entry['MJD']) < setDate)
                        }
                    })

            rv_plot(server)
            return Alert(
                ["Permissions set to "+ date_string],
                id="alert-auto",
                is_open=True,
                duration=10000,
            )

    return app
