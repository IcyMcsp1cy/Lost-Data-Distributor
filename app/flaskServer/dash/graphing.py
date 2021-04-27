from dash_html_components import Div, Span
from flask import render_template, request, g
from flask_login import current_user
from dash import Dash
from dash_core_components import (
    Graph, Slider, RangeSlider,
    DatePickerRange, Loading)
from dash_html_components import Div, Pre, Br, Button, Span, I
from dash_bootstrap_components import Tooltip
from dash.dependencies import (Input,
                               Output, State, ClientsideFunction)
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from dash.exceptions import PreventUpdate
from pandas import read_csv, DataFrame
from ..extensions import collection, mongo, get_fs
from ..config import csv_label, rv_label, graph_label
import julian
from datetime import date
import dash_daq as daq
from json import dumps
import plotly

url_base = '/data/'

rv_plot = None


def from_mjd(num):
    return str(julian.from_jd(float(num), fmt='mjd'))[0:23]


def to_mjd(num):
    return julian.to_jd(date(num), fmt='mjd')

def rv_plot(server):
    with server.app_context():

        entries = list(collection('radialvelocity').find())
        if entries == []:
            df_none = DataFrame(columns=[
                csv_label['datetime'], csv_label['filename'], csv_label['velocity']
            ])
            rv_plot.result = {}
            rv_plot.data = df_none
            rv_plot.public = df_none
            return df_none
        data = DataFrame(entries)
        data[csv_label['datetime']] = data[csv_label['datetime']].apply(from_mjd)
        
        rv_plot.data = data
        rv = data[data['PUBLIC'] == True]

        fig = plotly.graph_objs.Scatter(
            x= rv[csv_label['datetime']],
            y= rv[csv_label['velocity']],
            mode="markers",
            marker=plotly.graph_objs.scatter.Marker(
                opacity=0.6,
                colorscale="Viridis"
            )
        )
        x_axis = {
            'title': {
                'text': graph_label['rv_x'],
                'font': {
                    'size': 18,
                    'color': '#7f7f7f'
                }
            },
        }

        y_axis = {
            'title': {
                'text': graph_label['rv_y'],
                'font': {
                    'size': 18,
                    'color': '#7f7f7f'
                }
            },
        }

        rv_plot.result = dumps({'data': [fig], 'layout':{'xaxis':x_axis, 'yaxis':y_axis}, 'config': {'responsive': True}}, cls=plotly.utils.PlotlyJSONEncoder)
        rv_plot.public = rv
        return rv

tool = Span(
    "floccinaucinihilipilification",
    id="tooltip-target",
    style={"textDecoration": "underline", "cursor": "pointer"},
)

def init_graphing(server):
    #fs = gridfs.GridFS(mongo.db)
    with server.app_context():
        one = get_fs('one')
        two = get_fs('two')
    
    rv = rv_plot(server)
    

    app = Dash(
        '__main__',
        server=server,
        url_base_pathname=url_base,
        assets_folder='static',
    )

    @server.before_request
    def update():
        
        if request.endpoint == url_base:
            app.index_string = render_template(
                'data_page.html'
            )
            rv = rv_plot.public
            curr_user = g.user['atype']
            if curr_user == 'admin' or curr_user == 'researcher':
                rv = rv_plot.data
            app.layout = Div([
                Tooltip(
                    "Set the Y axis to a linear or logarithmic scale.",
                    target="log-switch",
                ),
                Tooltip(
                    "Enables data to be separated by order on the spectrograph",
                    target="dim-switch",
                ),
                Tooltip(
                    "The name of the file being displayed",
                    target="click-data",
                    placement="bottom"
                ),
                Tooltip(
                    "Selects which orders of the spectrum to render",
                    target="order-tool",
                ),
                Tooltip(
                    "Reduces the amount of points rendered to the screen",
                    target="res-tool",
                ),
                Tooltip(
                    "Each graph has a tool bar in the upper-right hand corner that appears when you mouse over a graph."
                    "Use the buttons in the tool bar to zoom in, zoom out, reset the axis, save a screen shot, "
                    "and more. Click on a point in the Radial Velocity graph to display the Spectrum graph below."  
                    "Hover over the slider and toggle bottoms below the lower graph to further interact with the"
                    "spectrum data.",
                    target="graph-tool"
                ),
                Loading([
                    Div([
                        Button([
                                I(
                                    className="fas fa-info-circle",
                                ),
                                Span(
                                    ' Info',
                                )
                            ],
                            id='graph-tool',
                            className='btn btn-warning btn-sm',
                        ),
                    ]),
                    Div(
                        id='rv-download-container'
                    ),
                    Button([
                            I(
                                className="fas fa-download",
                            ),
                            Span(
                                " Download Radial Velocities",
                            )
                        ],
                        id='rv-download',
                        className='btn btn-primary btn-sm float-right',
                    ),
                    Download(
                        id='rv-download-data'
                    ),
                    DatePickerRange(
                        id='date-range',
                        className='pt-1 d-flex justify-content-end w-100',
                    ),
                    Graph(
                        id='rv-plot',
                        className="",
                        config={
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'autoscale']
                        }
                    ),
                    
                ], type="default", className='d-flex justify-content-end w-100'),
                Div(
                    id='rv-data',
                    children=rv[rv_label].to_json(),
                    className='d-none'
                ),
                Div([
                    Pre(id='click-data', className=' d-inline'),
                ]),
                
                
                Br(),
                Br(),
                Div([
                    Loading([
                        Div([
                            Div([
                                Button([
                                        I(
                                            className="fas fa-download",
                                        ),
                                        Span(
                                            " Download 1D",
                                        )
                                    ],
                                    id='1d-spec-download',
                                    className='btn btn-primary btn-sm',
                                ),

                                Download(
                                    id='1d-spec-download-data'
                                ),
                            ], className='pr-2'),
                            Div([
                                Button([
                                    I(
                                        className="fas fa-download",
                                    ),
                                    Span(
                                        " Download 2D",
                                    )],
                                    id='2d-spec-download',
                                    className='btn btn-primary btn-sm',
                                ),

                                Download(
                                    id='2d-spec-download-data'
                                ),
                            ], className=""),
                        ], className="row justify-content-end d-none", id="spec-download-container"),
                        Div(
                            id='spec-data',
                            children=[],
                            className='d-none'
                        ),
                        Graph(
                            id='spec-plot',
                            className="pt-0",
                            config={
                                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'autoscale']
                            }
                        ),
                    ], type="default", ),


                    Div([
                        Span([
                            'Order Range\n'
                        ], id='order-tool', className='d-none'),
                        Span([
                            'Resolution\n'
                        ], id='res-tool', className='d-none')
                    ],
                    id='slide-label',
                    className='w-100 text-center'),


                    Div([
                        
                        Slider(
                            min=1,
                            max=200,
                            value=100,
                            marks={
                                1: {'label': '1:1', 'style': {'color': '#77b0b1'}},
                                20: {'label': '20:1'},
                                50: {'label': '50:1'},
                                100: {'label': '100:1'},
                                200: {'label': '200:1', 'style': {'color': '#f50'}}
                            },
                            id='resolution',
                            className='col d-none',
                        ),
                        RangeSlider(
                            id='spec-range',
                            className='col d-none',
                            min=0,
                            max=85,
                            step=1,
                            value=[40, 45],
                            marks={
                                0: {'label': '0'},
                                40: {'label': '40'},
                                45: {'label': '45'},
                                85: {'label': '85'}
                            }
                        ),
                    ], className='row'),
                ], id='spec-container'),
                Br(),
                Div([
                    Div([
                        daq.ToggleSwitch(
                            label='lin/log',
                            id='log-switch',
                            className='d-inline-block',
                            labelPosition='bottom'
                        ),
                    ], className='col text-center'),
                    Div([
                        daq.ToggleSwitch(
                            label='1D / 2D',
                            id='dim-switch',
                            className='d-inline-block',
                            labelPosition='bottom'
                        )
                    ], className='col text-center'),
                ], className="row")
            ])

    

    app.layout = Div([])

    app.clientside_callback(
        output=Output('click-data', 'children'),
        inputs=[Input('rv-plot', 'clickData'),
                State('rv-data', 'children')],
        clientside_function=ClientsideFunction(
            namespace='graphing',
            function_name='clickData'
        )
    )

    app.clientside_callback(
        output=Output('rv-plot', 'figure'),
        inputs=[Input('date-range', 'start_date'),
                Input('date-range', 'end_date'),
                State('rv-data', 'children')],
        clientside_function=ClientsideFunction(
            namespace='graphing',
            function_name='datefunc'
        )
    )

    app.clientside_callback(
        output=Output('spec-plot', 'figure'),
        inputs=[Input('resolution', 'value'),
                Input('spec-range', 'value'),
                Input('log-switch', 'value'),
                Input('spec-data', 'children')],
        clientside_function=ClientsideFunction(
            namespace='graphing',
            function_name='specfunc'
        )
    )


    @app.callback(Output('rv-download-data', 'data'),
                  Input('rv-download', 'n_clicks'))
    def rvDownload(n_clicks):
        if (n_clicks is not None) and (n_clicks > 0):
            return send_data_frame(rv.drop(['_id', 'PUBLIC'], axis=1).to_csv, filename="radial_velocities.csv")

    @app.callback(Output('1d-spec-download-data', 'data'),
                  Input('1d-spec-download', 'n_clicks'),
                  State('click-data', 'children'))
    def oneDownload(n_clicks, children):
        if (n_clicks is not None) and (n_clicks > 0) and (children is not None):
            searchDate = children.strip('Sun_')
            searchDate = searchDate.strip('.fits')
            try:
                specData = read_csv(one.find_one({'filename': {'$regex': '.*' + searchDate + '.*'}}))
                return send_data_frame(specData.to_csv, filename=searchDate+'.1d_spectrum.csv')
            except:
                entry = one.find_one({})
                specData = read_csv(entry)
                return send_data_frame(specData.to_csv, filename=entry['filename']+".1d_spectrum.csv")

    @app.callback(Output('2d-spec-download-data', 'data'),
                  Input('2d-spec-download', 'n_clicks'),
                  State('click-data', 'children'))
    def twoDownload(n_clicks, children):
        if (n_clicks is not None) and (n_clicks > 0) and (children is not None):
            searchDate = children.strip('Sun_')
            searchDate = searchDate.strip('.fits')
            try:
                specData = read_csv(two.find_one({'filename': {'$regex': '.*' + searchDate + '.*'}}))
                return send_data_frame(specData.to_csv, filename=searchDate + ".2d_spectrum.csv")
            except:
                entry = one.find_one({})
                specData = read_csv(entry)
                return send_data_frame(specData.to_csv, filename=entry['filename']+".2d_spectrum.csv")


    @app.callback(
        Output('spec-data', 'children'),
        Output('spec-download-container', 'className'),
        Output('spec-range', 'className'),
        Output('resolution', 'className'),
        Output('slide-label', 'children'),
        Input('click-data', 'children'),
        Input('dim-switch', 'value')
    )
    def getGraph(children, dim):

        if (children == None):
            raise PreventUpdate
        
        searchDate = children.strip('Sun_')
        searchDate = searchDate.strip('.fits')

        if (dim):
            slide = [
            Span([
                'Order Range\n'
            ], id='order-tool', className=''),
            Span([
                'Resolution\n'
            ], id='res-tool', className='d-none')
        ]
            regex = two.find_one({'filename': {'$regex': '.*' + searchDate + '.*'}})
            if regex:
                res = read_csv(regex).to_json()
                return res, 'row justify-content-end', 'col', 'col d-none', slide
            res = read_csv(two.find_one({})).to_json()
            return res, 'row justify-content-end', 'col', 'col d-none', slide

        slide = [
            Span([
                'Order Range\n'
            ], id='order-tool', className='d-none'),
            Span([
                'Resolution\n'
            ], id='res-tool', className='')
        ]
        regex = one.find_one({'filename': {'$regex': '.*' + searchDate + '.*'}})
        if regex:
            res = read_csv(regex).to_json()
            return res, 'row justify-content-end', 'col d-none', 'col', slide
        res = read_csv(one.find_one({})).to_json()
        return res, 'row justify-content-end', 'col d-none', 'col', slide

    return app
