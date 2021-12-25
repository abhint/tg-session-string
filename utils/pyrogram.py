from re import S, template
from bottle import request, redirect
from pyrogram import Client
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    CodeInvalid
)
from pyrogram.methods import password


class PyrogramClient:
    def __init__(self):
        pass
        # self.client = Client(":memory:", api_id=api_id, api_hash=api_hash)

    def connect_tg(self, api_id: str, api_hash):
        self.api_id=api_id
        self.api_hash=api_hash
        self.client = Client(":memory:", api_id=api_id, api_hash=api_hash)
        try:
            self.client.connect()
            return redirect('/phone_number')
        except ConnectionError as e:
            self.client.disconnect()
            return "404"

    def tg_send_code(self, phone_number: str):
        try:
            self.phone_number = phone_number
            self.code = self.client.send_code(phone_number=phone_number)
            return redirect('/verify')
        except ApiIdInvalid:
            return redirect('/')
        except PhoneNumberInvalid:
            return redirect('/phone_number')

    def tg_password(self, password):
        try:
            self.client.check_password(password=password)
            session_string = self.client.export_session_string()
            self.client.send_message('me', f'`{session_string}`')
            return redirect('/success')
        except:
            pass

    def tg_sing_in(self, tg_otp):
        try:
            self.client.sign_in(
                phone_number=self.phone_number,
                phone_code_hash=self.code.phone_code_hash,
                phone_code=tg_otp,
            )
            session_string = self.client.export_session_string()
            self.client.send_message('me', f'`{session_string}`')
            return redirect('/success')
        except PhoneCodeInvalid:
            return redirect('/phone_number')
        except PhoneCodeExpired:
            return redirect('/phone_number')
        except SessionPasswordNeeded:
            return redirect('/password')
        except CodeInvalid:
            return redirect('/verify')

    def tg_get_me(self):
        return self.client.get_me()

# def pyrogram_sing_in(api_id: str, api_hash: str):
#     try:
#         client = Client(
#             ":memory:",
#             api_id=api_id,
#             api_hash=api_hash
#         )
#     except Exception:
#         return 'error'
#     try:
#         client.connect()
#         return client, render_template('phone_number.html')
#     except ConnectionError as e:
#         return '404'
