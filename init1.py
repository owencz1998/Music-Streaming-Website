#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import hashlib
import datetime
from datetime import date
import time
from decimal import Decimal

today = date.today()
now = time.strftime('%Y-%m-%d %H:%M:%S')
salt = "sm9752"

#Initialize the app from Flask
app = Flask(__name__)
app.secret_key = "secret key"

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='root',
                       db='fatear',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Define route for search
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/songsearch', methods=['GET', 'POST'])
def songsearch():
    cursor = conn.cursor();
    genre = '%' + request.form['genre'] + '%'
    fname = '%' + request.form['fname'] + '%'
    lname = '%' + request.form['lname'] + '%'
    rating = request.form['rating']
    ops1 = request.form['ops1']
    ops2 = request.form['ops2']
    if (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'and' and ops2 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND s.songID = r.songID AND (g.genre LIKE %s AND (a.fname LIKE %s AND a.lname LIKE %s)) GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'and' and ops2 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s AND (a.fname LIKE %s AND a.lname LIKE %s)) UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'or' and ops2 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND s.songID = r.songID AND (g.genre LIKE %s OR (a.fname LIKE %s AND a.lname LIKE %s)) GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'or' and ops2 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s OR (a.fname LIKE %s AND a.lname LIKE %s)) UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating == '' and ops1 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s AND (a.fname LIKE %s AND a.lname LIKE %s))'
        cursor.execute(query, (genre, fname, lname))
    elif (genre == '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops2 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID AND (a.fname LIKE %s AND a.lname LIKE %s) GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (fname, lname, rating))
    elif (genre != '%%' and (fname == '%%' and lname == '%%') and rating != '' and ops1 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND s.songID = r.songID AND g.genre LIKE %s GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating == '' and ops1 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s OR (a.fname LIKE %s AND a.lname LIKE %s))'
        cursor.execute(query, (genre, fname, lname))
    elif (genre == '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops2 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID AND (a.fname LIKE %s AND a.lname LIKE %s) UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (fname, lname, rating))
    elif (genre != '%%' and (fname == '%%' and lname == '%%') and rating != '' and ops1 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND g.genre LIKE %s UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, rating))
    elif (genre != '%%' and (fname == '%%' and lname == '%%') and rating == ''):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND g.genre LIKE %s'
        cursor.execute(query, (genre))
    elif (genre == '%%' and (fname != '%%' and lname != '%%') and rating == ''):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND (a.fname LIKE %s AND a.lname LIKE %s)'
        cursor.execute(query, (fname, lname))
    elif (genre == '%%' and (fname == '%%' and lname == '%%') and rating != ''):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (rating))
    else:
        return redirect('search')
    data = cursor.fetchall()
    cursor.close()
    return render_template('results.html', songs=data)

@app.route('/song', methods=['GET', 'POST'])
def song():
    cursor = conn.cursor()
    songid = request.form['songid']
    query = 'SELECT s.title, CONCAT(a.fname, " ", a.lname) AS singer, s.releaseDate, g.genre, AVG(r.stars) AS stars, s.songURL FROM song s, artist a, artistperformssong p, songgenre g, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = g.songID AND s.songID = r.songID AND s.songID = %s GROUP BY s.title, singer, s.releaseDate, g.genre'
    cursor.execute(query, (songid))
    data = cursor.fetchone()
    cursor.close()
    return render_template('song_page.html', songinfo=data)

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    db_password = password + salt
    h = hashlib.md5(db_password.encode())
    pwd = h.hexdigest()
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s and pwd = %s'
    cursor.execute(query, (username, pwd))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)


#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    nickname = request.form['nickname']
    db_password = password + salt
    h = hashlib.md5(db_password.encode())
    pwd = h.hexdigest()
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, pwd, firstname, lastname, today, nickname))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    user = session['username']
    cursor = conn.cursor();
    query1 = 'SELECT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, userfanofartist f, user u, songinalbum i, album b WHERE s.songID = p.songID AND p.artistID = a.artistID AND a.artistID = f.artistID AND f.username = u.username AND s.songID = i.songID AND i.albumID = b.albumID AND s.releaseDate > u.lastlogin AND u.username = %s'
    cursor.execute(query1, (user))
    data1 = cursor.fetchall()
    query2 = 'SELECT f.follows, s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName, r.reviewText FROM reviewsong r, follows f, user u, song s, artistperformssong p, artist a, songinalbum i, album b WHERE s.songID = p.songID AND p.artistID = a.artistID AND r.username = f.follows AND f.follower = u.username AND r.reviewDate > u.lastlogin AND r.songID = s.songID AND s.songID = i.songID AND i.albumID = b.albumID AND u.username = %s UNION SELECT f.user1, s.songID,  s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName, r.reviewText FROM reviewsong r, friend f, user u, song s, artistperformssong p, artist a, songinalbum i, album b WHERE s.songID = p.songID AND p.artistID = a.artistID AND (r.username = f.user1 AND f.user2 = u.username) AND f.acceptStatus = "Accepted" AND r.reviewDate > u.lastlogin AND r.songID = s.songID AND s.songID = i.songID AND i.albumID = b.albumID AND u.username = %s UNION SELECT f.user2, s.songID,  s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName, r.reviewText from reviewsong r, friend f, user u, song s, artistperformssong p, artist a, songinalbum i, album b WHERE s.songID = p.songID AND p.artistID = a.artistID AND (r.username = f.user2 AND f.user1 = u.username) AND f.acceptStatus = "Accepted" AND r.reviewDate > u.lastlogin AND r.songID = s.songID AND s.songID = i.songID AND i.albumID = b.albumID AND u.username = %s'
    cursor.execute(query2, (user, user, user))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=user, songs1=data1, songs2=data2)

@app.route('/profile')
def profile():
    user = session['username']
    cursor = conn.cursor();
    query1 = 'SELECT fname, lname, username, nickname, lastlogin FROM user WHERE username = %s'
    cursor.execute(query1, (user))
    data1 = cursor.fetchone()
    query2 = 'SELECT s.title, r.stars, r.ratingDate, c.reviewtext, c.reviewDate FROM user u, song s, ratesong r, reviewsong c WHERE u.username = r.username AND u.username = c.username AND s.songID = r.songID and s.songID = c.songID AND u.username = %s ORDER BY r.ratingDate DESC, c.reviewDate DESC'
    cursor.execute(query2, (user))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('profile.html', username=user, user=data1, activity=data2)



@app.route('/registered_search')
def registered_search():
    user = session['username']
    return render_template('registered_search.html', username=user)


@app.route('/registered_songsearch', methods=['GET', 'POST'])
def registered_songsearch():
    user = session['username']
    cursor = conn.cursor();
    genre = '%' + request.form['genre'] + '%'
    fname = '%' + request.form['fname'] + '%'
    lname = '%' + request.form['lname'] + '%'
    rating = request.form['rating']
    ops1 = request.form['ops1']
    ops2 = request.form['ops2']
    if (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'and' and ops2 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND s.songID = r.songID AND (g.genre LIKE %s AND (a.fname LIKE %s AND a.lname LIKE %s)) GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'and' and ops2 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s AND (a.fname LIKE %s AND a.lname LIKE %s)) UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'or' and ops2 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND s.songID = r.songID AND (g.genre LIKE %s OR (a.fname LIKE %s AND a.lname LIKE %s)) GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops1 == 'or' and ops2 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s OR (a.fname LIKE %s AND a.lname LIKE %s)) UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, fname, lname, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating == '' and ops1 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s AND (a.fname LIKE %s AND a.lname LIKE %s))'
        cursor.execute(query, (genre, fname, lname))
    elif (genre == '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops2 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID AND (a.fname LIKE %s AND a.lname LIKE %s) GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (fname, lname, rating))
    elif (genre != '%%' and (fname == '%%' and lname == '%%') and rating != '' and ops1 == 'and'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND s.songID = r.songID AND g.genre LIKE %s GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, rating))
    elif (genre != '%%' and (fname != '%%' and lname != '%%') and rating == '' and ops1 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND (g.genre LIKE %s OR (a.fname LIKE %s AND a.lname LIKE %s))'
        cursor.execute(query, (genre, fname, lname))
    elif (genre == '%%' and (fname != '%%' and lname != '%%') and rating != '' and ops2 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID AND (a.fname LIKE %s AND a.lname LIKE %s) UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (fname, lname, rating))
    elif (genre != '%%' and (fname == '%%' and lname == '%%') and rating != '' and ops1 == 'or'):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND g.genre LIKE %s UNION SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (genre, rating))
    elif (genre != '%%' and (fname == '%%' and lname == '%%') and rating == ''):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, songgenre g WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = g.songID AND g.genre LIKE %s'
        cursor.execute(query, (genre))
    elif (genre == '%%' and (fname != '%%' and lname != '%%') and rating == ''):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND (a.fname LIKE %s AND a.lname LIKE %s)'
        cursor.execute(query, (fname, lname))
    elif (genre == '%%' and (fname == '%%' and lname == '%%') and rating != ''):
        query = 'SELECT DISTINCT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, b.albumName FROM song s, artistperformssong p, artist a, songinalbum i, album b, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = i.songID AND i.albumID = b.albumID AND s.songID = r.songID GROUP BY s.songID, s.title, singer, b.albumName HAVING AVG(r.stars) >= %s'
        cursor.execute(query, (rating))
    else:
        return redirect('registered_search')
    data = cursor.fetchall()
    cursor.close()
    return render_template('registered_results.html', username=user, songs=data)

@app.route('/registered_song', methods=['GET', 'POST'])
def registered_song():
    user = session['username']
    cursor = conn.cursor()
    songid = request.form['songid']
    query1 = 'SELECT s.songID, s.title, CONCAT(a.fname, " ", a.lname) AS singer, s.releaseDate, g.genre, AVG(r.stars) AS stars, s.songURL FROM song s, artist a, artistperformssong p, songgenre g, ratesong r WHERE s.songID = p.songID AND p.artistID = a.artistID AND s.songID = g.songID AND s.songID = r.songID AND s.songID = %s GROUP BY s.title, singer, s.releaseDate, g.genre'
    cursor.execute(query1, (songid))
    data1 = cursor.fetchone()
    query2 = 'SELECT CONCAT(u.fname, " ", u.lname) AS name, r.reviewText FROM reviewsong r, user u WHERE r.username = u.username and r.songID = %s'
    cursor.execute(query2, (songid))
    data2 = cursor.fetchall()
    cursor.close()
    return render_template('registered_song_page.html', username=user, songinfo=data1, reviews=data2)


@app.route('/review', methods=['GET', 'POST'])
def review():
    user = session['username']
    review = request.form['review']
    songid = request.form['songid']
    sif = eval(request.form['songinfo'])
    cursor = conn.cursor();
    query1 = 'SELECT * FROM reviewsong WHERE username = %s AND songID = %s'
    cursor.execute(query1, (user, songid))
    data = cursor.fetchone()
    if (data):
        query2 = 'UPDATE reviewsong SET reviewText = %s, reviewDate = %s WHERE username = %s AND songID = %s'
        cursor.execute(query2, (review, today, user, songid))
    else:
        query3 = 'INSERT INTO reviewsong VALUES (%s, %s, %s, %s)'
        cursor.execute(query3, (user, songid, review, today))
    conn.commit()
    cursor.close()
    return render_template('registered_song_page.html', username=user, songinfo=sif)


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    user = session['username']
    rate = request.form['rate']
    songid = request.form['songid']
    sif = eval(request.form['songinfo'])
    cursor = conn.cursor();
    query1 = 'SELECT * FROM ratesong WHERE username = %s AND songID = %s'
    cursor.execute(query1, (user, songid))
    data = cursor.fetchone()
    if (data):
        query2 = 'UPDATE ratesong SET stars = %s, ratingDate = %s WHERE username = %s AND songID = %s'
        cursor.execute(query2, (rate, today, user, songid))
    else:
        query3 = 'INSERT INTO ratesong VALUES (%s, %s, %s, %s)'
        cursor.execute(query3, (user, songid, rate, today))
    conn.commit()
    cursor.close()
    return render_template('registered_song_page.html', username=user, songinfo=sif)


@app.route('/friends', methods=['GET', 'POST'])
def friends():
    user = session['username']
    cursor = conn.cursor();
    query3 = 'SELECT CONCAT(u.fname, " ", u.lname) AS name, f.user1 AS username FROM friend f, user u WHERE f.user1 = u.username AND f.user2 = %s AND acceptStatus = "Accepted" UNION SELECT CONCAT(u.fname, " ", u.lname) AS name, user2 as username FROM friend f, user u WHERE f.user2 = u.username AND f.user1 = %s AND acceptStatus = "Accepted"'
    cursor.execute(query3, (user, user))
    data3 = cursor.fetchall()
    query1 = 'SELECT * FROM friend WHERE (user1 = %s OR user2 = %s) AND acceptStatus = %s AND requestSentBy != %s'
    cursor.execute(query1, (user, user, 'Pending', user))
    data1 = cursor.fetchall()
    data2 = []
    for i in data1:
        if i['user1'] == user:
            i['user'] = i['user2']
        else:
            i['user'] = i['user1']
        query2 = 'SELECT CONCAT(fname, " ", lname) AS name FROM user WHERE username = %s'
        cursor.execute(query2, (i['user']))
        data2.append(cursor.fetchone())
    data = [dict(x, **y) for x, y in zip(data1, data2)]
    cursor.close()
    return render_template('friends.html', username=user, flist=data3, friends=data)

@app.route('/accept', methods=['GET', 'POST'])
def accept():
    user = session['username']
    friend = request.form['friend']
    at = request.form['at']
    cursor = conn.cursor();
    query = 'UPDATE friend SET acceptStatus = "Accepted", updatedAt = %s WHERE ((user1 = %s AND user2 = %s) OR (user2 = %s AND user1 = %s)) AND acceptStatus = "Pending" AND requestSentBy = %s AND createdAt = %s'
    cursor.execute(query, (now, user, friend, user, friend, friend, at))
    conn.commit()
    return redirect('/friends')

@app.route('/reject', methods=['GET', 'POST'])
def reject():
    user = session['username']
    friend = request.form['friend']
    at = request.form['at']
    cursor = conn.cursor();
    query = 'UPDATE friend SET acceptStatus = "Not accepted", updatedAt = %s WHERE ((user1 = %s AND user2 = %s) OR (user2 = %s AND user1 = %s)) AND acceptStatus = "Pending" AND requestSentBy = %s AND createdAt = %s'
    cursor.execute(query, (now, user, friend, user, friend, friend, at))
    conn.commit()
    return redirect('/friends')

@app.route('/search_friends', methods=['GET', 'POST'])
def search_friends():
    user = session['username']
    fname = "%" + request.form['fname'] + "%"
    lname = "%" + request.form['lname'] + "%"
    uname = "%" + request.form['uname'] + "%"
    cursor = conn.cursor();
    query = 'SELECT DISTINCT u.username, u.fname, u.lname, u.nickname from user u, friend f WHERE u.username != %s AND u.username LIKE %s AND u.fname LIKE %s AND u.lname LIKE %s  AND u.username NOT IN(SELECT user2 FROM friend WHERE user1 = %s AND acceptStatus IN ("Accepted", "Pending", "Not Accepted") UNION SELECT user1 FROM friend WHERE user2 = %s AND acceptStatus IN ("Accepted", "Pending"))'
    cursor.execute(query, (user, uname, fname, lname, user, user))
    data = cursor.fetchall()
    return render_template('search_friends.html', username=user, people=data)

@app.route('/send_request', methods=['GET', 'POST'])
def send_request():
    user = session['username']
    uname = request.form['uname']
    cursor = conn.cursor();
    query = 'INSERT INTO friend (user1, user2, acceptStatus, requestSentBy, createdAt) VALUES (%s, %s, "Pending", %s, %s)'
    cursor.execute(query, (user, uname, user, now))
    conn.commit()
    return redirect('/friends')

@app.route('/logout')
def logout():
    user = session['username']
    cursor = conn.cursor()
    query = 'UPDATE user SET lastlogin = %s WHERE username = %s'
    cursor.execute(query, (today, user))
    conn.commit()
    session.pop('username')
    return redirect('/')


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)