from wtforms import Form, TextField, TextAreaField, PasswordField, validators
from wtforms import HiddenField

strip_filter = lambda x: x.strip() if x else None


class BlogCreateForm(Form):
    title = TextField('Entry title', [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    body = TextAreaField('Entry body', [validators.Length(min=1)],
                         filters=[strip_filter])
    owner = HiddenField()


class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()


class CreateUser(Form):
    name = TextField('Username', [validators.Length(min=1, max=255)],
                     filters=[strip_filter])
    email = TextField('Email Address', [validators.Email()],
                      filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=4, max=255)],
                             filters=[strip_filter])
