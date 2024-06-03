from flask import Flask, render_template, Response, jsonify, request, session, Blueprint
#FlaskForm--> it is required to receive input from the user
# Whether uploading a video file  to our object app model
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os
# Required to run the YOLOv8 model
import cv2
from yolov8_detect_video import video_detection

webserver_route = Blueprint('routes', __name__)

class UploadFileForm(FlaskForm):
    #We store the uploaded video file path in the FileField in the variable file
    #We have added validators to make sure the user inputs the video in the valid format  and user does upload the
    #video when prompted to do so
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Run")


def generate_frames(path_x=''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @webserver_route.route('/', methods=['GET', 'POST'])
# def frontStart():
#     # Upload File Form: Create an instance for the Upload File Form
#     form = UploadFileForm()
#     if form.validate_on_submit():
#         # Our uploaded video file path is saved here
#         file = form.file.data
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), webserver_route.config['UPLOAD_FOLDER'],
#                                secure_filename(file.filename)))  # Then save the file
#         # Use session storage to save video file path
#         session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), webserver_route.config['UPLOAD_FOLDER'],
#                                              secure_filename(file.filename))
#     return render_template('videoprojectnew.html', form=form)

@webserver_route.route('/', methods=['GET'])
def frontStart():
    return 'Home Page Route'

@webserver_route.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('indexproject.html')


# Rendering the Webcam Rage
#Now lets make a Webcam page for the application
#Use 'app.route()' method, to render the Webcam page at "/webcam"
@webserver_route.route("/webcam", methods=['GET', 'POST'])
def webcam():
    session.clear()
    return render_template('ui.html')


@webserver_route.route('/FrontPage', methods=['GET', 'POST'])
def front():
    # Upload File Form: Create an instance for the Upload File Form
    form = UploadFileForm()
    if form.validate_on_submit():
        # Our uploaded video file path is saved here
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), webserver_route.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # Then save the file
        # Use session storage to save video file path
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), webserver_route.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('videoprojectnew.html', form=form)


@webserver_route.route('/video')
def video():
    #return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(path_x=session.get('video_path', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# To display the Output Video on Webcam page
@webserver_route.route('/webapp')
def webapp():
    #return Response(generate_frames(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

