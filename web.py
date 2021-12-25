from bottle import *
# from bottle import app.route, run, template, request, view, static_file
from utils.pyrogram import PyrogramClient


client = PyrogramClient()

app = Bottle()


@app.route('/static/<filepath:path>')
def load_static(filepath):
    return static_file(filepath, root='./static')


@app.route('/', method='GET')
@app.route('/', method='POST')
def index():
    if request.method == 'POST':
        api_id = request.forms.get('api_id')
        api_hash = request.forms.get('api_hash')
        result = client.connect_tg(api_id=api_id, api_hash=api_hash)
        return result
    return template('home.html')



@app.route('/phone_number', method='GET')
@app.route('/phone_number', method='POST')
def get_phone_number():
    if request.method == 'POST':
        phone_number = request.forms.get('ph_number')
        result = client.tg_send_code(phone_number=phone_number)
        return result
    return template('phone_number.html')

@app.route('/verify', method='GET')
@app.route('/verify', method='POST')
def otp_verify():
    if request.method == 'POST':
        code = request.forms.get('tg_otp')
        result = client.tg_sing_in(tg_otp=code)
        return result
    return template('code_verification.html')


@app.route('/password', method='GET')
@app.route('/password', method='POST')
def two_step():
    if request.method == 'POST':
        two_ = request.forms.get('tg_password')
        result = client.tg_password(password=two_)
        return result
    return template('password.html')

@app.route('/success')
def success():
    me = client.tg_get_me()
    print(me)
    return template('success', user_name='Hello')



# @app.route('/error', method='GET')
# @app.route('/error', method='POST')
# @view('error')
# def error_html():
#     return dict(name='Hello')

# @app.error(404)
# @view('error')
# def error_handler_404(error):
#     return 'error_handler_404'

app.run(host='localhost', port=8080)