#all the imports
import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,\
abort,render_template,flash
from contextlib import closing

# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
"""


#create our little application
app=Flask(__name__)

#configuration
app.config.update(dict(DATABASE='/tmp/flaskr.db',
DEBUG=True,
SECRET_KEY='development key',
USERNAME='admin',
PASSWORD='default'))


app.config.from_envvar('FLASK_SETINGS',silent=True)

def connect_db():
	"""connect to the specific database"""
	rv=sqlite3.connect(app.config['DATABASE'])
	rv.row_factory=sqlite3.Row
	return rv

def init_db():
	"""Creates the database table"""
	with app.app_context():
		db=get_db()
		with app.open_resource('schema.sql',mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


def get_db():
	"""opens a new database connection
	   current application context.
	"""
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db=connect_db()
	return g.sqlite_db

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username']!=app.config['USERNAME']:
			error='Invalid username'
		elif request.form['password']!=app.config['PASSWORD']:
			error='Invaild password'
		else:
			session['logged_in']=True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error='error')


@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))


@app.route('/')
def show_entries():
	cur=g.db.execute('select title,text from entries order by id desc')
	entries=[dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html',entries=entries)


@app.route('/add',method=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db=get_db()
	db.execute('insert into entries (title,text) values(?,?)',
			   [request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))




if __name__=='__main__':
	init_db()
	app.run()
