from flask import Flask
app = Flask(__name__)
app.secret_key ='&AC9xXMjyEhBMh'


if __name__=="main":
    app.run(debug=True)

DATABASE_SCHEMA='sasquatch_websightings'