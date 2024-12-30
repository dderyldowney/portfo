"""
This is the server file that will run the Flask app.
"""

from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<string:page_name>")
def render_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open("database.csv", mode="a", newline="") as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(
            database, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
        )
        csv_writer.writerow([email, subject, message])


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()  # Extract form data
            write_to_csv(data)  # Write data to CSV
            return redirect("thankyou.html")  # Redirect to thank you page
        except KeyError as e:  # Handle missing keys in form data
            return f"KeyError: {str(e)}. Did not save to the database."
        except IOError as e:  # Handle file-related errors
            return f"IOError: {str(e)}. Could not write to the database."
        except Exception as e:  # General catch-all for unexpected exceptions
            return f"An unexpected error occurred: {str(e)}. Did not save to the database."
    else:
        return "Something went wrong. Try again!"
