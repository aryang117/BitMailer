from celery import Celery
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import psycopg2

from coolStuff import password

app = Flask(__name__)
api = Api(app)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

conn = psycopg2.connect(database="postgres", user="postgres",
                        password=password, host="127.0.0.1", port="5432")
cur = conn.cursor()
tableName = "User"

@app.route('/create', methods=['POST'])
def create():
    parser = reqparse.RequestParser()  # initialize

    parser.add_argument('email', required=True)
    parser.add_argument('upperlimit', required=True)
    parser.add_argument('lowerlimit', required=True)

    args = parser.parse_args()
    print(args)
    email1 = "'" + args["email"] + "'"
    ul = args["upperlimit"]
    ll = args["lowerlimit"]

    cur.execute('INSERT INTO public."' + tableName +
                '" (email, upperlimit, lowerlimit) VALUES ( ' + email1 + ',' + ul + ',' + ll + ')')
    conn.commit()

    res = args['email'] + ' ' + args['upperlimit'] + ' ' + args['lowerlimit']

    return 'Added!' + res


@app.route('/delete', methods=['POST'])
def deleteEntry():
    parser = reqparse.RequestParser()

    parser.add_argument('email', required=True)

    args = parser.parse_args()
    print(parser.args)

    deleteEmail = "'" + args['email'] + "'"

    cur.execute('DELETE FROM public."' + tableName +
                '" WHERE email LIKE ' + deleteEmail)
    conn.commit()

    return 'Deleted ' + args['email']


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@celery.task()
def add_together(a, b):
    return a + b

#result = add_together.delay(1, 1)
#result.wait()  # 65

if __name__ == '__main__':
    app.run()
