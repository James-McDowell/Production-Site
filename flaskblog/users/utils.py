import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message
from threading import Thread
from flaskblog.config import Config

REC_EMAIL = os.environ.get('REC_EMAIL')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following link
    {url_for('users.reset_token', token=token, _external=True)}
    
    If you did not make this request, ignore this email.
    '''
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_contact_email(email, subject, message):
    msg = Message(subject, sender=email, recipients=[REC_EMAIL])
    msg.body = f''' {email}
    {message}
    '''
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
