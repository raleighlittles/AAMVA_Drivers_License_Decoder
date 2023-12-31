import flask_wtf
import flask_wtf.file
import wtforms

class SubmitDriversLicenseTextForm(flask_wtf.FlaskForm):

    # Must use TextArea instead of standard StringField, for it to be accepted as multi-line
    drivers_license_text_encoded = wtforms.TextAreaField("Encoded driver's license text")
    submit_btn = wtforms.SubmitField("Submit")