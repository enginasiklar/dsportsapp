from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)


@app.route("/",methods=['GET', 'POST'])
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM branches")
    session['branch_data'] = cursor.fetchall()
    return render_template('index.html',data=session['branch_data'])


@app.route("/main")
def main():
    name = session['Name']
    session['UserID']=session['UserID2']
    return render_template('main.html', name=name,role=session['RoleID'])


@app.route("/feat", methods=['GET', 'POST'])
def feat():
    session['SessionID'] = request.form['SessionID']
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM feats WHERE sessionid = %s", (session['SessionID'],))
        data = cursor.fetchall()
        return render_template('feat.html', data=data,role=session['RoleID'],user1=session['UserID'],user2=session['UserID2'])


@app.route("/create_team")
def create_team():
    if session['TeamID']:
        msg = "You're already in a team"
        return render_template('error.html',msg=msg ,role=session['RoleID'])
    return render_template('create_team.html',role=session['RoleID'])


@app.route("/create_team_send", methods=['GET', 'POST'])
def create_team_send():
    branch_id = session['BranchID']
    user_id = session['UserID']
    tname = request.form['tname']
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO teams VALUES(NULL,%s,%s)''',
                   (tname, branch_id))
    mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM teams WHERE teamname = %s", (tname,))
    data = cursor.fetchone()
    session['TeamID'] = data['TeamID']
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE account SET teamid = %s WHERE userid = %s", (data['TeamID'], user_id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('add_team'))


@app.route("/add_team")
def add_team():
    branch_id = session['BranchID']
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM account WHERE teamid is NULL AND branchid = %s and roleid = 1", (branch_id,))
        data = cursor.fetchall()
        return render_template('add_team.html', data=data,role=session['RoleID'])


@app.route("/view_team", methods=['GET', 'POST'])
def view_team():
    branch_id = session['BranchID']
    team_id = session['TeamID']
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM account WHERE teamid = %s AND branchid = %s", (team_id, branch_id,))
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM subteams WHERE teamid = %s", (team_id,))
        data2 = cursor.fetchall()
        return render_template('view_team.html', data=data, data2=data2,role=session['RoleID'])


@app.route("/add_session")
def add_session():
    return render_template('add_session.html',role=session['RoleID'])


@app.route("/create_steam", methods=['POST'])
def create_steam():
    if request.method == 'POST':
        sname = request.form['sname']
        team_id = session['TeamID']
        cursor = mysql.connection.cursor()
        cursor.execute(
            ''' INSERT INTO subteams VALUES(NULL,%s,%s)''', (sname, team_id))
        mysql.connection.commit()
        return redirect(url_for('view_team'))

@app.route("/add_to_steam", methods=['POST'])
def add_to_steam():
    userid = request.form.getlist("userid")
    subid = request.form['subteamid']
    cursor = mysql.connection.cursor()
    
    for x in userid:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM subteammembers WHERE userid = %s", (x,))
        account = cursor.fetchone()
        if account:
            msg = "One or more members are in a subteam"
            return render_template('error.html',msg=msg ,role=session['RoleID'])

    for x in userid:
        cursor.execute(''' INSERT INTO subteammembers VALUES(%s,%s)''', (subid,x))
        mysql.connection.commit()
    return redirect(url_for('view_team'))


@app.route("/view_stat")
def view_stat():
    if request.method == 'GET':
        user_id = session['UserID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM physicalstats WHERE userid = %s", (user_id,))
        data = cursor.fetchall()
        return render_template('view_stat.html', data=data,role=session['RoleID'],user1=session['UserID'],user2=session['UserID2'])

@app.route("/comment_stat", methods=['GET', 'POST'])
def comment_stat():
    date = request.form['StatDate']
    comment = request.form['scomment']
    cursor = mysql.connection.cursor()
    cursor.execute(
            "UPDATE physicalstats SET comment = %s WHERE userid = %s AND statdate = %s", (comment, session['UserID'], date))
    mysql.connection.commit()
    return redirect(url_for('view_stat'))

@app.route("/delete_stat", methods=['GET', 'POST'])
def delete_stat():
    date = request.form['StatDate']
    cursor = mysql.connection.cursor()
    cursor.execute(
            "DELETE FROM physicalstats WHERE userid = %s AND statdate = %s", ( session['UserID'], date))
    mysql.connection.commit()
    return redirect(url_for('view_stat'))

@app.route("/delete_user", methods=['GET', 'POST'])
def delete_user():
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM physicalstats WHERE userid = %s", ( session['UserID']))
    mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM sessions WHERE userid = %s", ( session['UserID'],))
    data = cursor.fetchall()
    cursor = mysql.connection.cursor()
    for x in data:
        cursor.execute("DELETE FROM feats WHERE sessionid = %s", ( x['SessionID']))
        mysql.connection.commit()
        cursor.execute("DELETE FROM sessions WHERE sessionid = %s", ( x['SessionID']))
        mysql.connection.commit()
    cursor.execute("DELETE FROM subteammembers WHERE userid = %s", ( session['UserID']))
    mysql.connection.commit()
    cursor.execute("DELETE FROM account WHERE userid = %s", ( session['UserID']))

    return redirect(url_for('login'))

@app.route("/add_stat")
def add_stat():
    return render_template('add_stat.html',role=session['RoleID'])

@app.route("/subteam")
def subteam():
    team_id = session['TeamID']
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM subteams WHERE teamid = %s", (team_id,))
        data = cursor.fetchall()
        return render_template('subteam.html', data=data,role=session['RoleID'])

@app.route("/view_subteam", methods=['GET', 'POST'])
def view_subteam():
    print(session['TeamID'])

    if session['RoleID']==2:
        subteamid = request.form['subteamid']
    else:
        if session['SubteamID']!=0:
            subteamid= session['SubteamID']
        else:
            msg = "You're not in a subteam"
            return render_template('error.html',msg=msg ,role=session['RoleID'])

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM account WHERE userid IN (SELECT userid FROM subteammembers WHERE subteamid = %s)", (subteamid,))
    data = cursor.fetchall()
    
    return render_template('subteam_view.html', data=data,role=session['RoleID'])

    
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM account WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            if account['TeamID']!= 'NULL':
                cursor.execute('SELECT * FROM subteammembers WHERE userid = %s', (account['UserID'],))
                subteam=cursor.fetchone()
                if subteam:
                    session['SubteamID'] = subteam['SubteamID']
                else:
                    session['SubteamID'] = 0

            session['UserID'] = account['UserID']
            session['UserID2'] = account['UserID']
            session['RoleID'] = account['RoleID']
            session['BranchID'] = account['BranchID']
            session['Name'] = account['Name']
            session['TeamID'] = account['TeamID']
            session['logged_in'] = True
            return redirect(url_for('main'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('SessionID', None)
    session.pop('loggedin', None)
    session.pop('UserID', None)
    session.pop('RoleID', None)
    session.pop('BranchID', None)
    session.pop('TeamID',None)
    session.pop('SubteamID',None)
    session.pop('Name', None)
    return render_template('index.html',data=session['branch_data'])

@app.route('/account')
def account():
    return render_template('account.html',role=session['RoleID'])

@app.route('/change_username', methods=['GET', 'POST'])
def change_username():
    username = request.form['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM account WHERE username = %s", (username,))
    account = cursor.fetchone()
    if account:
        msg = "Username already taken"
        return render_template('error.html',msg=msg ,role=session['RoleID'])
    cursor = mysql.connection.cursor()
    cursor.execute(
            "UPDATE account SET username = %s WHERE userid = %s", (username, session['UserID']))
    mysql.connection.commit()
    return redirect(url_for('main'))


@app.route('/session_send', methods=['GET', 'POST'])
def session_send():
    user_id = session['UserID']
    if request.method == 'POST':
        session_date = request.form['sdate']
        session_length = request.form['slen']
        photo = request.form['sphoto']
        comment = request.form['scomment']
        
        cursor = mysql.connection.cursor()

        cursor.execute(''' INSERT INTO sessions VALUES(NULL,%s,%s,%s,%s,%s)''',
                       (session_date, session_length, photo, comment, user_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('add_session'))


@app.route('/stat_send', methods=['GET', 'POST'])
def stat_send():
    user_id = session['UserID']
    if request.method == 'POST':
        stat_date = request.form['sdate']
        height = request.form['height']
        weight = request.form['weight']
        fpercent = request.form['fpercent']
        calintake = request.form['calintake']
        comment = request.form['scomment']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM physicalstats WHERE userid = %s and statdate = %s ", (session['UserID'],stat_date))
        account = cursor.fetchone()
        if account:
            msg = "These stats are already added"
            return render_template('error.html',msg=msg ,role=session['RoleID'])

        cursor = mysql.connection.cursor()

        cursor.execute(''' INSERT INTO physicalstats VALUES(%s,%s,%s,%s,%s,%s,%s)''',
                       (user_id, stat_date, height, weight, fpercent, calintake, comment))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('add_stat'))


@app.route('/feat_send', methods=['GET', 'POST'])
def feat_send():
    if request.method == 'POST':
        fname = request.form['fname']
        value = request.form['value']
        rep = request.form['rep']

        cursor = mysql.connection.cursor()

        cursor.execute(''' INSERT INTO feats VALUES(NULL,%s,%s,%s,%s)''',
                       (fname, value, rep, session['SessionID']))
        mysql.connection.commit()
        cursor.close()
        return render_template('feat.html',role=session['RoleID'])


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        branchID = request.form['branchID']
        roleID = request.form['roleID']
        cursor = mysql.connection.cursor()

        cursor.execute(''' INSERT INTO account VALUES(NULL,%s,%s,%s,%s,%s,%s,NULL)''',
                       (username, password, name, surname, roleID, branchID))
        mysql.connection.commit()
        cursor.close()
        return render_template('index.html',data=session['branch_data'])


@app.route("/view_session", methods=['GET', 'POST'])
def view_session():

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM sessions WHERE userid = %s", (session['UserID'],))
        data = cursor.fetchall()

        return render_template('view_session.html', data=data,role=session['RoleID'],user1=session['UserID'],user2=session['UserID2'])

@app.route("/change_user_temp", methods=['GET', 'POST'])
def change_user_temp():
    user=request.form['selected_user']
    session['UserID'] = user
    return render_template('main_other.html')




@app.route("/delete_session", methods=['GET', 'POST'])
def delete_session():
    if session['UserID']==session['UserID2']:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM feats WHERE sessionid = %s", ( session['SessionID'],))
        mysql.connection.commit()
        cursor.execute("DELETE FROM sessions WHERE sessionid = %s", ( session['SessionID'],))
        mysql.connection.commit()
    else:
        print("this is not your account")
    return redirect(url_for('view_session'))


@app.route("/comment_session", methods=['GET', 'POST'])
def comment_session():
    comment = request.form['comment']
    cursor = mysql.connection.cursor()
    cursor.execute(
            "UPDATE sessions SET comment = %s WHERE sessionid = %s", (comment, session['SessionID']))
    mysql.connection.commit()
    return redirect(url_for('view_session'))

@app.route("/add_member", methods=['GET', 'POST'])
def add_member():

    cursor = mysql.connection.cursor()
    userid = request.form.getlist("userid")
    for x in userid:
        cursor.execute(
            "UPDATE account SET teamid = %s WHERE userid = %s", (session['TeamID'], x))
        mysql.connection.commit()
    cursor.close()
    return redirect(url_for('add_team'))


if __name__ == "__main__":
    app.run()
