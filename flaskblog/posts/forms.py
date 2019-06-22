from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskblog.models import Cat
from wtforms.validators import DataRequired


def category_select():
    return Cat.query.order_by(Cat.title)


class PostForm(FlaskForm):
    category = QuerySelectField(get_label='title',
                                query_factory=category_select,
                                allow_blank=True,
                                validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', id="summernote", validators=[DataRequired()])
    picture = FileField('Header/Thumbnail Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')
