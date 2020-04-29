from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from apis import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wdbjcwvtwqrepa' \
                                        ':cee8af49d68c54942189e2d9688e7fa5f2d2b6d00f9dd0e8d4bd90febacf4b24@ec2-54-228' \
                                        '-250-82.eu-west-1.compute.amazonaws.com:5432/d5d3577l6fd3ac '
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/api_example/todo.db'
db = SQLAlchemy(app)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, port=33507)
