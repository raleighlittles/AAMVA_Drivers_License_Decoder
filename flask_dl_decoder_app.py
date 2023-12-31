import flask
import flask_helper
import my_app_form
import inspect
import json

# locals
import aamva_drivers_license_decoder


flask_app = flask.Flask(
    flask_helper.generate_instance_id(), static_folder="static", template_folder="templates")

# needed for CSRF
flask_app.config['SECRET_KEY'] = flask_helper.generate_secret_key(16)


@flask_app.route("/decode", methods=["GET", "POST"])
def decode_dl_text():

    curr_function_name = inspect.stack()[0][3]

    flask_app.logger.info("'%s()' called", curr_function_name)

    form = my_app_form.SubmitDriversLicenseTextForm()

    http_request_method = flask.request.method

    if http_request_method == "GET":
        return flask.render_template("submit.html", form=form)

    elif http_request_method == "POST":

        if not form.validate():
            # Reload the page to the user and let them try again
            flask.flash(
                "Error: Must either provide DL text or a photo of ID's reverse")
            return flask.render_template("submit.html", form=form)

        else:  # form validates

            flask_app.logger.info("User submitted: '%s'",
                                  form.drivers_license_text_encoded.data)
            users_dl_text = form.drivers_license_text_encoded.data.split("\n")

            if len(users_dl_text) < 2:
                return flask.render_template("submission_failed.html", err_msg="Submitted text was too short!")

            else:
                parsed_dl_data_results = aamva_drivers_license_decoder.decode_aamva_fields(
                    users_dl_text)
                return flask.render_template("submission_successful.html", parsed_json_dl_data=json.dumps(parsed_dl_data_results, sort_keys=True, indent=2))

    else:
        raise ValueError(f"Invalid HTTP request type '{http_request_method}'")
