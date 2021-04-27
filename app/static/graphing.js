
csv_label = {
    'accept': 'ACCEPT',
    'filename': 'FILENAME',
    'datetime': 'MJD',
    'velocity': 'V',
    'flux': 'FLUX',
    'wavelength': '# WAVE',
    'order': 'ORDER'
}
graph_label = {
    'rv_x': 'Recorded Date',
    'rv_y': 'Radial Velocity',
    'spec_x': 'Wavelength(Angstrom)',
    'spec_y': 'Flux',
}




window.dash_clientside = Object.assign({}, window.dash_clientside, {
    graphing: {
        clickData: function(clickData, table) {
            if(clickData === undefined) return;
            data = JSON.parse(table)
            return data[csv_label['filename']][clickData.points[0].pointIndex]
        },
        
        datefunc: function(start, end, table) {
            var xrange
            if(table === undefined) {
                throw "input undefined"
            }
            if(start === undefined) {
                xrange = {
                    
                    'autoscale': true}
            } else {
                xrange = {
                    
                    'range': [start, end]
                }
            }

            data = JSON.parse(table)
            console.log(start)
            return {
                'data':[{
                    'x': Object.values(data[csv_label['datetime']]),
                    'y': Object.values(data[csv_label['velocity']]),
                    'xaxis': 'x',
                    'yaxis': 'y',
                    'type': 'scattergl',
                    'mode': 'markers'
                }],
                'layout':{
                    'xaxis': {
                        'title': {
                            'text': graph_label['rv_x'],
                            'font': {
                                'size': 18,
                                'color': '#7f7f7f'
                            }
                        },
                        xrange,
                    },
                    'yaxis': {
                        'title': {
                            'text': graph_label['rv_y'],
                            'font': {
                                'size': 18,
                                'color': '#7f7f7f'
                            }
                        },
                        'autoscale': true
                    },
                    'type': 'scattergl',
                    "hovermode": "closest"
                }
            }

        },

        specfunc: function(res, range, log, table) {
            if(table === undefined) {
                throw "input undefined"
            }
            
            data = JSON.parse(table)

            let linlog = "linear"
            if(log) {
                linlog = "log"
            }
            let index = 0, x_order = [], y_order = [], data_structure = []

            if( data.hasOwnProperty(csv_label['order'])) {
                for(let order = range[0]; order < range[1]; order++) {
                    while(data[csv_label['order']][index] <= order) {
                        if(data[csv_label['order']][index] === order) {
                            x_order.push(data[csv_label['wavelength']][index])
                            y_order.push(data[csv_label['flux']][index])
                        }
                        index++
                    }

                    data_structure.push({
                        "line": { "color": ["#EE3124", "#F8971D", "#FFDD00", "#3DAE2B", "#00AEEF", "#002F87", "#A25EB5"][order%7], "dash": "solid" },
                        "mode": "lines",
                        "name": "<b>" + order + "</b>",
                        "showlegend": true,
                        "type": "scattergl",
                        "x": x_order,
                        "xaxis": "x",
                        "y": y_order,
                        "yaxis": "y"
                    })
                    x_order = []
                    y_order = []
                }
            } else {

                less = {
                    'wave':[],
                    'flux':[]
                }
                len =Object.keys(data[csv_label['wavelength']]).length
                for (i = 0; i < len; i=i+res) {
                    f=0
                    for (r=0; r < res; r+=1) {
                        f += data[csv_label['wavelength']][i+r]
                    }

                    less['wave'].push(f/res);
                    less['flux'].push(data[csv_label['wavelength']][i]);
                }
                data_structure = [{
                    'x': Object.values(less['wave']),
                    'y': Object.values(less['flux']),
                    'xaxis': 'x',
                    'yaxis': 'y',
                    'type': 'linegl',
                }]
            }
            
            
            return {
                'data': data_structure,
                'layout':{
                    'yaxis': {
                        'title': {
                            'text': graph_label['spec_y'],
                            'font': {
                                'size': 18,
                                'color': '#7f7f7f'
                            }
                        },
                        'type': linlog,
                        'autoscale': true},
                    'xaxis': {
                        'title': {
                            'text': graph_label['spec_x'],
                            'font': {
                                'size': 18,
                                'color': '#7f7f7f'
                            }
                        },
                        'autoscale': true
                    },
                    'type': 'linegl',
                    "hovermode": "closest",
                    
                }
            }
        },
    }
});
