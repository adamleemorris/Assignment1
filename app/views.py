"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app,db
from flask import render_template, request, redirect, send_from_directory, url_for, current_app
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from sys import platform
from flask import send_from_directory


from app.model import PropertyModel
from app.forms import PropertyForm

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods=["GET", "POST"])
def create():
    form = PropertyForm()

    if request.method == 'POST' and form.validate_on_submit():
        property_title = form.title.data
        description = form.description.data
        bedrooms = form.bedrooms.data  # Adjusted to match the correct form field name
        bathrooms = form.bathrooms.data
        price = form.price.data
        location = form.location.data
        property_type = form.property_type.data
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        # Ensure the uploads folder exists
        uploads_path = app.config['UPLOAD_FOLDER']
        os.makedirs(uploads_path, exist_ok=True)  # Create the folder if it does not exist
        print("Uploading to:", uploads_path)
        print(os.path.join(os.path.join(uploads_path, filename)))

        if photo:
            print("File received:", photo.filename)
        else:
            print("No file received")


        photo.save(os.path.join(uploads_path, filename))



        property = PropertyModel(
            title=property_title,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            location=location,
            price=price,
            property_type=property_type,
            description=description,
            photo_filename=filename  
        )

        db.session.add(property)
        db.session.commit()

        flash('Your property data has been successfully uploaded', 'success')
        return redirect(url_for('properties'))  # Make sure 'properties' route exists

    return render_template('create.html', form=form)

@app.route('/uploads/<filename>')
def get_image(filename): 
    filepath = os.path.join(current_app.root_path, 'uploads')  # Assuming 'uploads' is directly in your app root
    return send_from_directory(filepath,filename)
    # return 'hi'

def get_uploaded_images():
    image_list = []
    rootdir = os.getcwd()
    upload_path = os.path.join(rootdir, 'uploads')  # More reliable path handling

    for subdir, dirs, files in os.walk(upload_path):
        for file in files:
            image_list.append(file)
    return image_list  # 


@app.route('/properties')
def properties():
    properties = PropertyModel.query.all()
    return render_template('properties.html', properties= properties)

@app.route('/properties/<propertyid>')
def show_property(propertyid): 
    property = PropertyModel.query.filter_by(id=propertyid).first()
    if property:
        return render_template('property.html', property=property)
    else:
        return "Property not found", 404


# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
