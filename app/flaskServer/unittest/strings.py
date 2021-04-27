click_1d = {
    "output":"..spec-data.children...spec-download-container.className...spec-range.className...resolution.className...slide-label.children..",
    "outputs":[
        {"id":"spec-data","property":"children"},
        {"id":"spec-download-container","property":"className"},
        {"id":"spec-range","property":"className"},
        {"id":"resolution","property":"className"},
        {"id":"slide-label","property":"children"}
    ],
    "inputs":[
        {"id":"click-data","property":"children","value":"98765.4321"},
        {"id":"dim-switch","property":"value"}
    ],
    "changedPropIds":["click-data.children"]
}

click_1d_res = {"response": {"spec-data": {"children": "{\"Unnamed: 0\":{\"0\":0},\"# WAVE\":{\"0\":3814.49471651},\"FLUX\":{\"0\":1.00343363}}"}, "spec-download-container": {"className": "row justify-content-end"}, "spec-range": {"className": "col d-none"}, "resolution": {"className": "col"}, "slide-label": {"children": "Resolution\n"}}, "multi": True}


click_2d = {
    "output":"..spec-data.children...spec-download-container.className...spec-range.className...resolution.className...slide-label.children..",
    "outputs":[
        {"id":"spec-data","property":"children"},
        {"id":"spec-download-container","property":"className"},
        {"id":"spec-range","property":"className"},
        {"id":"resolution","property":"className"},
        {"id":"slide-label","property":"children"}
    ],
    "inputs":[
        {"id":"click-data","property":"children","value":"98765.4321"},
        {"id":"dim-switch","property":"value","value":True}
    ],
    "changedPropIds":["dim-switch.value"]
}

click_2d_res = {"response": {"spec-data": {"children": "{\"Unnamed: 0\":{\"0\":0},\"# WAVE\":{\"0\":381.45022},\"FLUX\":{\"0\":0.0406},\"CONTINUUM\":{\"0\":0.04047},\"NORMALIZED\":{\"0\":1.00323},\"ORDER\":{\"0\":0}}"}, "spec-download-container": {"className": "row justify-content-end"}, "spec-range": {"className": "col"}, "resolution": {"className": "col d-none"}, "slide-label": {"children": "Order Range\n"}}, "multi": True}


down_rv = {
    "output":"rv-download-data.data",
    "outputs":{"id":"rv-download-data","property":"data"},
    "inputs":[
        {"id":"rv-download","property":"n_clicks","value":1}
    ],
    "changedPropIds":["rv-download.n_clicks"]
}

down_rv_res = {'response': {'rv-download-data': {'data': {'content': 'LEZJTEVOQU1FLE9CTk0sTUpELFYKMSw5ODc2NS40MzIxLDMwMDAwMC4xMDY3LDIwMjMtMDItMjUgMTc6NDQ6MjYuODgwLDIwMDAuMjMK', 'filename': 'radial_velocities.csv', 'mime_type': None, 'base64': True}}}, 'multi': True}
down_1d = {
    "output":"1d-spec-download-data.data",
    "outputs":{
        "id":"1d-spec-download-data","property":"data"
    },
    "inputs":[
        {"id":"1d-spec-download","property":"n_clicks","value":1}
    ],
    "changedPropIds":["1d-spec-download.n_clicks"],
    "state":[{"id":"click-data","property":"children","value":"98765.4321"}]
}

down_1d_res = {"response": {"1d-spec-download-data": {"data": {"content": "LFVubmFtZWQ6IDAsIyBXQVZFLEZMVVgKMCwwLDM4MTQuNDk0NzE2NTEsMS4wMDM0MzM2Mwo=", "filename": "98765.4321.1d_spectrum.csv", "mime_type": None, "base64": True}}}, "multi": True}


down_2d = {
    "output":"2d-spec-download-data.data",
    "outputs":{"id":"2d-spec-download-data","property":"data"},
    "inputs":[{"id":"2d-spec-download","property":"n_clicks","value":1}],
    "changedPropIds":["2d-spec-download.n_clicks"],
    "state":[{"id":"click-data","property":"children","value":"98765.4321"}]}

down_2d_res = {"response": {"2d-spec-download-data": {"data": {"content": "LFVubmFtZWQ6IDAsIyBXQVZFLEZMVVgsQ09OVElOVVVNLE5PUk1BTElaRUQsT1JERVIKMCwwLDM4MS40NTAyMiwwLjA0MDYsMC4wNDA0NywxLjAwMzIzLDAK", "filename": "98765.43212d_spectrum.csv", "mime_type": None, "base64": True}}}, "multi": True}


news_submit = {
    "output":"..news-alert.children...news-table.data..",
    "outputs":[
        {"id":"news-alert","property":"children"},
        {"id":"news-table","property":"data"}
    ],
    "inputs":[
        {"id":"news-submit","property":"n_clicks","value":1},
        {"id":"news-delete","property":"n_clicks","value":0},
        {"id":"news-home","property":"n_clicks","value":0}
    ],
    "changedPropIds":["news-submit.n_clicks"],
    "state":[
        {"id":"news-title","property":"value","value":"title"},
        {"id":"news-subtitle","property":"value","value":"subtitle"},
        {"id":"news-author","property":"value","value":"author"},
        {"id":"news-text","property":"value","value":"body text"},
        {"id":"news-table","property":"data","value":[]}
    ]
}

news_submit_res = {"response": {"news-alert": {"children": {"props": {"children": ["Article posted to ", {"props": {"children": "this link", "href": "/post/6084a61657eacebd93c8c6a3", "className": "alert-link"}, "type": "A", "namespace": "dash_html_components"}], "id": "alert-auto", "is_open": True, "duration": 10000}, "type": "Alert", "namespace": "dash_bootstrap_components"}}, "news-table": {"data": [{"_id": "6084a61657eacebd93c8c6a3", "title": "title", "subtitle": "subtitle", "author": "author", "content": "body text", "datetime": "April 24, 2021"}]}}, "multi": True}


def news_select(post):
    return {
        "output":"..news-title.value...news-subtitle.value...news-author.value...news-text.value...news-delete.className...news-home.className..",
        "outputs":[
            {"id":"news-title","property":"value"},
            {"id":"news-subtitle","property":"value"},
            {"id":"news-author","property":"value"},
            {"id":"news-text","property":"value"},
            {"id":"news-delete","property":"className"},
            {"id":"news-home","property":"className"}
        ],
        "inputs":[
            {
                "id":"news-table",
                "property":"data",
                "value":[
                    {"_id":str(post['_id']),
                    "title":post['title'],
                    "subtitle":post['subtitle'],
                    "author":post['author'],
                    "content":post['content'],
                    "datetime":post['datetime']
                    }
                ]
            },
            {"id":"news-table",
            "property":"active_cell",
            "value":{
                "row":0,
                "column":1,
                "column_id":"author"
            }
        }
    ],
    "changedPropIds":["news-table.active_cell"]
}

news_select_res = {"response": {"news-title": {"value": "title"}, "news-subtitle": {"value": "subtitle"}, "news-author": {"value": "author"}, "news-text": {"value": "body text"}, "news-delete": {"className": "btn my-2 mx-2"}, "news-home": {"className": "btn my-2 mx-2"}}, "multi": True}


def news_home(post):
    return {
    "output":"..news-alert.children...news-table.data..",
    "outputs":[
        {"id":"news-alert","property":"children"},
        {"id":"news-table","property":"data"}
    ],
    "inputs":[
        {"id":"news-submit","property":"n_clicks","value":1},
        {"id":"news-delete","property":"n_clicks","value":0},
        {"id":"news-home","property":"n_clicks","value":1}
    ],
    "changedPropIds":["news-home.n_clicks"],
    "state":[
        {"id":"news-title","property":"value","value":"title"},
        {"id":"news-subtitle","property":"value","value":"subtitle"},
        {"id":"news-author","property":"value","value":"author"},
        {"id":"news-text","property":"value","value":"body text"},
        {"id":"news-table","property":"data","value":[
            {"_id":str(post['_id']),
                "title":post['title'],
                "subtitle":post['subtitle'],
                "author":post['author'],
                "content":post['content'],
                "datetime":post['datetime']
            }
        ]}
    ]
}

def news_home_res(post):
    return {
    "response": {
        "news-alert": {
            "children": {
                "props": {
                    "children": ["Post set as home"], 
                    "id": "alert-auto", 
                    "is_open": True, 
                    "duration": 10000
                }, 
                "type": "Alert", 
                "namespace": "dash_bootstrap_components"}
            }, 
            "news-table": {
                "data": [
                    {
                        "_id":str(post['_id']),
                        "title":post['title'],
                        "subtitle":post['subtitle'],
                        "author":post['author'],
                        "content":post['content'],
                        "datetime":post['datetime'],
                        "location": 'home',
                    }
                ]
            }
        }, 
        "multi": True
    }


user_select = {
    "output":"..user-alert.children...user-table.data...user-display.className..",
    "outputs":[
        {"id":"user-alert","property":"children"},
        {"id":"user-table","property":"data"},
        {"id":"user-display","property":"className"}
    ],
    "inputs":[
        {"id":"user-verify","property":"n_clicks"},
        {"id":"user-reject","property":"n_clicks"},
        {"id":"user-purge","property":"n_clicks"},
        {"id":"user-table","property":"active_cell","value":{"row":1,"column":2,"column_id":"email"}}
    ],
    "changedPropIds":["user-table.active_cell"],
    "state":[
        {"id":"user-email","property":"children","value":""},
        {"id":"user-table","property":"data","value":[
            {"firstName":"taken","lastName":"taken","email":"taken@email.com","institution":"taken","type":"unverified"},
            {"firstName":"register","lastName":"account","email":"reg@email.com","institution":"reg","type":"researcher"},
            {"firstName":"admin","lastName":"admin","email":"admin@email.com","institution":"lowell","type":"admin"}
        ]}
    ]
}

user_select_res = {"response": {"user-alert": {"children": ""}, "user-table": {"data": [{"firstName": "taken", "lastName": "taken", "email": "taken@email.com", "institution": "taken", "type": "unverified"}, {"firstName": "register", "lastName": "account", "email": "reg@email.com", "institution": "reg", "type": "researcher"}, {"firstName": "admin", "lastName": "admin", "email": "admin@email.com", "institution": "lowell", "type": "admin"}]}, "user-display": {"className": ""}}, "multi": True}

user_display = {
    "output":"..user-display.children...user-verify.className...user-reject.className..",
    "outputs":[
        {"id":"user-display","property":"children"},
        {"id":"user-verify","property":"className"},
        {"id":"user-reject","property":"className"}
    ],
    "inputs":[
        {"id":"user-table","property":"data","value":[
            {"firstName":"taken","lastName":"taken","email":"taken@email.com","institution":"taken","type":"unverified"},
            {"firstName":"register","lastName":"account","email":"reg@email.com","institution":"reg","type":"researcher"},
            {"firstName":"admin","lastName":"admin","email":"admin@email.com","institution":"lowell","type":"admin"}
        ]},
        {"id":"user-table","property":"active_cell","value":{"row":1,"column":2,"column_id":"email"}}
    ],
    "changedPropIds":["user-table.active_cell","user-table.data"]
}

user_display_res = {"response": {"user-display": {"children": {"props": {"children": [{"props": {"children": [{"props": {"children": "register account", "className": "card-title text-primary"}, "type": "H4", "namespace": "dash_html_components"}, {"props": {"children": "reg", "className": "card-subtitle"}, "type": "H6", "namespace": "dash_html_components"}, {"props": {"children": "reg@email.com", "id": "user-email", "className": "card-text"}, "type": "P", "namespace": "dash_html_components"}, {"props": {"children": "researcher", "className": "card-text"}, "type": "B", "namespace": "dash_html_components"}]}, "type": "CardBody", "namespace": "dash_bootstrap_components"}], "style": {"width": "18rem"}, "className": "border border-5 border-primary"}, "type": "Card", "namespace": "dash_bootstrap_components"}}, "user-verify": {"className": "btn my-2 mx-2 d-none"}, "user-reject": {"className": "btn my-2 mx-2 d-none"}}, "multi": True}


user_reject = {"output":"..user-alert.children...user-table.data...user-display.className..","outputs":[{"id":"user-alert","property":"children"},{"id":"user-table","property":"data"},{"id":"user-display","property":"className"}],"inputs":[{"id":"user-verify","property":"n_clicks"},{"id":"user-reject","property":"n_clicks","value":1},{"id":"user-purge","property":"n_clicks"},{"id":"user-table","property":"active_cell","value":{"row":0,"column":3,"column_id":"institution"}}],"changedPropIds":["user-reject.n_clicks"],"state":[{"id":"user-email","property":"children","value":"reg@email.com"},{"id":"user-table","property":"data","value":[{"firstName":"register","lastName":"account","email":"reg@email.com","institution":"reg","type":"unverified"},{"firstName":"admin","lastName":"admin","email":"admin@email.com","institution":"lowell","type":"admin"},{"firstName":"taken","lastName":"taken","email":"taken@email.com","institution":"taken","type":"unverified"}]}]}


user_verify = {"output":"..user-alert.children...user-table.data...user-display.className..","outputs":[{"id":"user-alert","property":"children"},{"id":"user-table","property":"data"},{"id":"user-display","property":"className"}],"inputs":[{"id":"user-verify","property":"n_clicks"},{"id":"user-reject","property":"n_clicks","value":2},{"id":"user-purge","property":"n_clicks"},{"id":"user-table","property":"active_cell","value":{"row":1,"column":3,"column_id":"institution"}}],"changedPropIds":["user-reject.n_clicks"],"state":[{"id":"user-email","property":"children","value":"taken@email.com"},{"id":"user-table","property":"data","value":[{"_id":"6084d83d77ee148efefb9825","email":"admin@email.com","firstName":"admin","lastName":"admin","institution":"lowell","password":"adminpass","type":"admin"},{"_id":"6084d83d77ee148efefb9824","email":"taken@email.com","firstName":"taken","lastName":"taken","institution":"taken","password":"taken","type":"unverified"}]}]}



glos_submit = {
    "output":"..glos-alert.children...glos-table.data..",
    "outputs":[
        {"id":"glos-alert","property":"children"},
        {"id":"glos-table","property":"data"}
    ],
    "inputs":[
        {"id":"glos-submit","property":"n_clicks","value":1},
        {"id":"glos-delete","property":"n_clicks"}
    ],
    "changedPropIds":["glos-submit.n_clicks"],
    "state":[
        {"id":"glos-term","property":"value","value":"term"},
        {"id":"glos-text","property":"value","value":"definition"},
        {"id":"glos-table","property":"data","value":[]}
    ]
}

def glos_submit_res(post):
    return {
    "response": {
        "glos-alert": {
            "children": {
                "props": {
                    "children": ["Glossary Updated"], 
                    "id": "alert-auto", "is_open": True, 
                    "duration": 10000
                },
                "type": "Alert", 
                "namespace": "dash_bootstrap_components"
            }
        }, 
        "glos-table": {
            "data": [
                {
                    "_id": str(post['_id']), 
                    "entry": post['entry'], 
                    "definition": post['definition'], 
                    "datetime": str(post['datetime']), 
                }
            ]
        }
    },
    "multi": True}


def glos_delete(post):
    return {
    "output":"..glos-alert.children...glos-table.data..",
    "outputs":[
        {"id":"glos-alert","property":"children"},
        {"id":"glos-table","property":"data"}
    ],
    "inputs":[
        {"id":"glos-submit","property":"n_clicks","value":1},
        {"id":"glos-delete","property":"n_clicks","value":1}
    ],
    "changedPropIds":["glos-delete.n_clicks"],
    "state":[
        {"id":"glos-term","property":"value","value":"term"},
        {"id":"glos-text","property":"value","value":"definition"},
        {"id":"glos-table","property":"data","value":[
            {
                "_id": str(post['_id']), 
                "entry": post['entry'], 
                "definition": post['definition'], 
                "datetime": str(post['datetime']), 
            }
        ]}
    ]
}

glos_delete_res = {"response": {"glos-alert": {"children": {"props": {"children": ["Post Deleted"], "id": "alert-auto", "is_open": True, "duration": 10000}, "type": "Alert", "namespace": "dash_bootstrap_components"}}, "glos-table": {"data": []}}, "multi": True}


def date_submit(date):
    return {"output":"file-alert.children","outputs":{"id":"file-alert","property":"children"},"inputs":[{"id":"date-submit","property":"n_clicks","value":1}],"changedPropIds":["date-submit.n_clicks"],"state":[{"id":"date-picker","property":"date","value":"2020-11-01"}]}

date_submit_res = {"response": {"file-alert": {"children": {"props": {"children": ["Permissions set to November 01, 2020"], "id": "alert-auto", "is_open": True, "duration": 10000}, "type": "Alert", "namespace": "dash_bootstrap_components"}}}, "multi": True}




