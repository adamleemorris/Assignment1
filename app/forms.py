from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, FileField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileRequired

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()], render_kw={"class": "form-control"})
    bedrooms = IntegerField('No. of Rooms', validators=[DataRequired(), NumberRange(min=1)], render_kw={"class": "form-control"})
    bathrooms = IntegerField('No. of Bathrooms', validators=[DataRequired(), NumberRange(min=1)], render_kw={"class": "form-control"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"class": "form-control"})
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"class": "form-control"})
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[DataRequired()], render_kw={"class": "form-control"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"class": "form-control"})
    photo = FileField('Property Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png','jpeg'], 'Images only!')
    ], render_kw={"class": "form-control"})
