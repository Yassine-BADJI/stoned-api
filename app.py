from flask import Flask
from apis import api

app = Flask(__name__)
api.init_app(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/api_example/todo.db'

if __name__ == '__main__':
    app.run(debug=True, port=33507)
