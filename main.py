from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = "mykey"
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

# my_dict = {'Tuples in Python are immutable (True/False)': ('True', 'False'),
#             'The elements of a List in Python are written inside': ('{} brackets', '[] brackets', '() brackets', 'None of the Above'),
#             'Which of the following computer languages is not object oriented': ('C++', 'C', 'Python', 'Java'),
#             'What exception is raised when there is datatype mismatch in python': ('DivideByZero', 'FormatException', 'IndexOutOfRangeException', 'MemoryOutOfBoundsException'),
#             'What class is used to obtain input from user in Java': ('Scanner class', 'SqlDataAdapter', 'Input/Output class', 'Exception class')}

# answer_dict = {
#   "The elements of a List in Python are written inside": [
#     "[] brackets"
#   ],
#   "Tuples in Python are immutable (True/False)": [
#     "True"
#   ],
#   "What class is used to obtain input from user in Java": [
#     "Scanner class"
#   ],
#   "What exception is raised when there is datatype mismatch in python": [
#     "FormatException"
#   ],
#   "Which of the following computer languages is not object oriented": [
#     "C"
#   ]
# }


class ScoresModel(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Scores(email = {self.email}, score = {self.score}"


class RegisterModel(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Register(name = {self.name}, email = {self.email}, password = {self.password})"


class QuestionModel(db.Model):
    question = db.Column(db.String(500), primary_key=True)
    option1 = db.Column(db.String(500), nullable=False)
    option2 = db.Column(db.String(500), nullable=False)
    option3 = db.Column(db.String(500), nullable=False)
    option4 = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Question(question = {self.question}, option1 = {self.option1}, option2 = {self.option2}, option3 = {self.option3}, option4 = {self.option4}, answer = {self.answer}"


resource_fields = {
    # 'id': fields.Integer,   # was using id as primary key , changed it to email (unique email id)
    'name': fields.String,
    'email': fields.String,
    'password': fields.String
}

resource_fields1 = {
    'email': fields.String,
    'score': fields.Integer
}

resource_fields2 = {
    'question': fields.String,
    'option1': fields.String,
    'option2': fields.String,
    'option3': fields.String,
    'option4': fields.String,
    'answer' : fields.String

}


@marshal_with(resource_fields)
@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@marshal_with(resource_fields)
@marshal_with(resource_fields1)
@app.route('/evaluate', methods=["GET", "POST"])
def evaluate():
    if request.method == "POST":
        email = request.form["email"]
        passwd = request.form["password"]  # use db.create_all() first time for database has to be created
        if email == "" and passwd == "":
            flash('Please fill missing fields', 'missing')
            return redirect(url_for('login'))
        if email == "admin@admin.com" and passwd == "admin":
            session['email'] = "admin@admin.com"
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            new_tup = ()
            for row in cur.execute("SELECT question, option1, option2, option3, option4 FROM question_model;"):
                new_tup += (row,)
            my_dict = {}
            new_tup2 = ()
            k = 0
            for i in range(len(new_tup)):
                for j in range(1, 5):
                    new_tup2 += (new_tup[i][j],)

                my_dict[new_tup[i][k]] = new_tup2
                new_tup2 = ()
            return render_template("admin.html", content=email, data=my_dict)
        else:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            my_list = []
            i = 0
            for row in cur.execute('SELECT email,password FROM register_model;'):
                my_list.append(row)

            j = 0
            p = 1
            flag = 0
            for i in range(len(my_list)):
                if my_list[i][j] == email and my_list[i][p] == passwd:
                    flag = 1
                    break

            if flag == 1:
                session['email'] = email
                for row in cur.execute("SELECT * FROM scores_model;"):
                    if email in row:
                        flag = 2
                        # return render_template("scores.html")
                # check if user has already taken quiz and restrict
                #     else:
                #         return render_template("home.html", content=email, data=my_dict)
                # return 'Logged in as ' + email + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
                if flag == 2:
                    tup = ()
                    for row in cur.execute("SELECT * FROM scores_model;"):
                        tup = tup + (row,)
                    return render_template("scores.html", content=tup)
                else:
                    new_tup = ()
                    for row in cur.execute("SELECT question, option1, option2, option3, option4 FROM question_model;"):
                        new_tup+=(row,)
                    my_dict = {}
                    new_tup2 = ()
                    k = 0
                    for i in range(len(new_tup)):
                        for j in range(1, 5):
                            new_tup2+=(new_tup[i][j],)

                        my_dict[new_tup[i][k]] = new_tup2
                        new_tup2 = ()
                        # check(my_dict)
                    return render_template("home.html", content=email, data=my_dict)

            else:
                flash('Unregistered User!', 'error')
                return redirect(url_for('login'))


@app.route('/check', methods=["GET", "POST"])
def check():
    new_dict = {}
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    new_tup = ()
    for row in cur.execute("SELECT question, option1, option2, option3, option4 FROM question_model;"):
        new_tup += (row,)
    my_dict = {}
    new_tup2 = ()
    k = 0
    for i in range(len(new_tup)):
        for j in range(1, 5):
            new_tup2 += (new_tup[i][j],)

        my_dict[new_tup[i][k]] = new_tup2
        new_tup2 = ()
    score = 0
    new_tup = ()

    for row in cur.execute("SELECT question, answer FROM question_model;"):
        new_tup += (row,)
    answer_dict = {}
    new_tup2 = ()
    k = 0
    for i in range(len(new_tup)):
        for j in range(1, 2):
            new_tup2 += (new_tup[i][j],)

        answer_dict[new_tup[i][k]] = new_tup2
        new_tup2 = ()
    if request.method == "POST":
        for i, j in my_dict.items():
            new_dict[i] = request.form.get(i,)  # building a dictionary with user submitted answers
    #     my_list.append((request.form.getlist('The elements of a List in Python are written inside')))
    for i, j in answer_dict.items():
        for p, q in new_dict.items():
            if i == p:
                if j[0] == q:
                    score+=1

    print(answer_dict)
    print("")
    print(new_dict)

    score_str = "Your score: "
    score = str(score)
    email = session['email']
    new_result = ScoresModel(email=email, score=int(score))
    db.session.add(new_result)
    db.session.commit()
    db.create_all()
    return score_str+score+" <b><a href = '/logout'>click here to log out</a></b>"


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


@marshal_with(resource_fields)
@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template("register.html")


@marshal_with(resource_fields)
@app.route('/insertrecord', methods=["POST"])
def put():
    if request.method == "POST":
        # unique_id = request.form["id"]
        name = request.form["name"]
        email = request.form["email"]
        passwd = request.form["passwd"]
        db.create_all()  # used only for one time (initially)

        result = RegisterModel.query.filter_by(email=email).first()
        if result:
            flash('Email already exists! try logging in!', 'taken')
            return redirect(url_for('register'))
        else:
            registerquery = RegisterModel(name=name, email=email, password=passwd)
            db.session.add(registerquery)
            db.session.commit()
            str = "Successfully registered as "+email
            flash(str, 'success')
            return redirect(url_for('login'))


@app.route('/scores')
def scores():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    tup = ()
    for row in cur.execute("SELECT * FROM scores_model;"):
        tup = tup + (row,)
    return render_template("scores.html", content=tup)


@marshal_with(resource_fields2)
@app.route('/createq', methods=["GET", "POST"])
def createq():
    if request.method == "POST":
        question = request.form["question"]
        opt1 = request.form["opt1"]
        opt2 = request.form["opt2"]
        opt3 = request.form["opt3"]
        opt4 = request.form["opt4"]
        ans = request.form["ans"]
        db.create_all()
        result = QuestionModel.query.filter_by(question=question).first()
        if result:
            flash('Question already exists!', 'error')
            return render_template("admin.html")
        else:
            questionquery = QuestionModel(question=question, option1=opt1, option2=opt2, option3=opt3, option4=opt4, answer=ans)
            db.session.add(questionquery)
            db.session.commit()
            flash('Successfully added question!', 'success')
            return render_template("admin.html")


@app.route("/deleteq", methods=["GET", "POST"])
def deleteq():
    if request.method == "POST":
        my_str = str(request.form['delete'])
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('DELETE FROM question_model WHERE question="'+my_str+'";')
        con.commit()
        new_tup = ()
        for row in cur.execute("SELECT question, option1, option2, option3, option4 FROM question_model;"):
            new_tup += (row,)
        my_dict = {}
        new_tup2 = ()
        k = 0
        for i in range(len(new_tup)):
            for j in range(1, 5):
                new_tup2 += (new_tup[i][j],)

            my_dict[new_tup[i][k]] = new_tup2
            new_tup2 = ()
        email = ""
        email = session['email']
        return render_template("admin.html", content=email, data=my_dict)


@app.route('/', methods=["GET"])
def mainpage():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)


