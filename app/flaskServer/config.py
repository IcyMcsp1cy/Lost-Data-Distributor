
FLASK_ENV = 'production'
DEBUG = True
SECRET_KEY = 'AlrightThenKeepYourSecrets'

MONGO_URI = 'mongodb+srv://Dev:dev@cluster0.odagz.mongodb.net/lost?retryWrites=true&w=majority'
TESTING = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'LOSTEXPRS1@gmail.com'
MAIL_PASSWORD = 'LostExpres2021'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

ADMIN_EMAIL = 'LOSTEXPRES2@gmail.com'

csv_label = {
    # Dict of csv formatting options.
    # 'type': 'DEFINE LABEL HERE'
    'accept': 'ACCEPT',
    'filename': 'FILENAME',
    'datetime': 'MJD',
    'velocity': 'V',

}
graph_label = {
    'rv_x': 'Recorded Date',
    'rv_y': 'Radial Velocity',
    'spec_x': 'Wavelength(Angstrom)',
    'spec_y': 'Flux',
}
rv_label = [
    csv_label['filename'], 
    csv_label['datetime'], 
    csv_label['velocity']
]
