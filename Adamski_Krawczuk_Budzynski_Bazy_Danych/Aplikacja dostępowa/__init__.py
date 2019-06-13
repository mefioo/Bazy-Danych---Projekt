from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify, json

from wtforms import Form, TextField, validators, PasswordField, BooleanField, StringField, IntegerField

from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart

import gc

import datetime

from flask_mail import Mail, Message

import dbconnect

from decorators import login_required, logout_required, isspecialist, isadmin
from send_mail import mail


from get_data import get_data, get_columns, get_columns2
import get_data

app = Flask(__name__)


@login_required
@app.route('/logged/')
def alredy_logged_in():
    return render_template("you_are_already_logged_in.html")


@app.route('/send-mail/')
def send_mail():
    try:
        msg = Message("Send Mail Tutorial!",
          sender="piotr635@gmail.com",
          recipients=["k.r.budzynski@gmail.com"])
        msg.body = "Tugot triumfator x2!!!"
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return(str(e))


@app.route('/register/', methods=["GET", "POST"])
@logout_required
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            # email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            # c, conn = connection()


            # if int(x) > 0:
            #     flash("That email is already registrated, please choose another")
            #     return render_template('register.html', form=form)
            #
            # else:
            #     c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
            #               (thwart(username), thwart(password), thwart(email),
            #                thwart("/introduction-to-python-programming/")))
            #
            #     conn.commit()
            #     flash("Thanks for registering!")
            #     c.close()
            #     conn.close()
            dbconnect.insert_account((username, password, 0))
            gc.collect()

            session['logged_in'] = True
            session['username'] = username
            session['permission'] = 0

            return redirect(url_for('homepage'))

        return render_template("register.html", form=form)

    except Exception as e:
        return (str(e))

@app.route('/addactivity/', methods=["GET", "POST"])
@login_required
def addactivity():
    try:
        data = dbconnect.set_diet(session["username"])
        diet_id = dbconnect.insert_diet(data)
        gc.collect()
        day_number = len(dbconnect.find_weekly_diet_by_login_and_day(session["username"]))+1
        dbconnect.insesrt_week_diet((session["username"], diet_id, day_number))
        form = AddActivityForm(request.form)
        activity_list = [item[1] for item in list(dbconnect.select_all_test('aktywnosci'))[0]]
        if request.method == "POST" and form.validate():
            name = form.name.data
            activity_id = dbconnect.find_activity_id(name)
            hours = form.hours.data
            dbconnect.insert_activity_row((session["username"], activity_id, hours))
            gc.collect()
            return redirect(url_for('userinfo'))

        return render_template("addactivity.html", form=form, my_list=activity_list)

    except Exception as e:
        return (str(e))


@app.route('/adddiet/', methods=["GET", "POST"])
@login_required
def adddiet():
    i = 0
    while i<7:
        try:
            data = dbconnect.set_diet(session["username"])
            diet_id = dbconnect.insert_diet(data)
            gc.collect()
            day_number = len(dbconnect.find_weekly_diet_by_login_and_day(session["username"]))+1
            i+=1
            if day_number<=7:
                dbconnect.insesrt_week_diet((session["username"], diet_id, day_number))
            else:
                break
        except Exception as e:
            pass
    return redirect(url_for('userinfo'))



@app.route('/removediet/', methods=["GET", "POST"])
@login_required
def removediet():
    try:
        dbconnect.delete_week_diet_by_login(session["username"])
        return redirect(url_for('userinfo'))
    except Exception as e:
        return (str(e))

@app.route('/adminarea/', methods=["GET", "POST"])
@login_required
@isadmin
def adminarea():
    try:
        activity = AddActivityForm(request.form)
        reset_delete = ResetPasswordForm(request.form)
        permission = ChangePermissionLevelForm(request.form)

        if request.method == "POST" and activity.validate():
            new_act = activity.name.data
            energy = activity.hours.data
            dbconnect.insert_activity((new_act, energy))
            gc.collect()
            flash("Operacja zakończona sukcesem!")
            return redirect(url_for('homepage'))
        if request.method == "POST" and reset_delete.validate():
            login = reset_delete.login.data
            password = reset_delete.password.data
            if (password):
                dbconnect.update_user_password(login, password)
            else:
                dbconnect.delete_account(dbconnect.find_user_by_login(login))
            flash("Operacja zakończona sukcesem!")
            return redirect(url_for('homepage'))
        if request.method == "POST" and permission.validate():
            login = permission.login.data
            new_perm = permission.permission_level.data
            dbconnect.update_permission(login, new_perm)
            gc.collect()
            flash("Operacja zakończona sukcesem!")
            return redirect(url_for('homepage'))
        return render_template("adminarea.html", activity=activity, form=reset_delete, permission=permission)

    except Exception as e:
        flash("Coś poszło nie tak...")
        return (str(e))


@app.route('/new_act/', methods=["GET", "POST"])
@login_required
@isadmin
def new_act():
    try:
        activity = AddActivityForm(request.form)

        if request.method == "POST" and activity.validate():
            new_acti = activity.name.data
            energy = activity.hours.data
            dbconnect.insert_activity((new_acti, energy))
            gc.collect()
            flash("Operacja zakończona sukcesem!")
            return redirect(url_for('homepage'))

    except Exception as e:
        flash("Coś poszło nie tak...")
        return (str(e))

@app.route('/new_permission/', methods=["GET", "POST"])
@login_required
@isadmin
def new_permission():
    try:
        permission = ChangePermissionLevelForm(request.form)
        if request.method == "POST" and permission.validate():
            login = permission.login.data
            new_perm = permission.permission_level.data
            dbconnect.update_permission(login, new_perm)
            gc.collect()
            flash("Operacja zakończona sukcesem!")
            return redirect(url_for('homepage'))

    except Exception as e:
        flash("Coś poszło nie tak...")
        return (str(e))

@app.route('/manage_account/', methods=["GET", "POST"])
@login_required
@isadmin
def manage_account():
    try:
        reset_delete = ResetPasswordForm(request.form)

        if request.method == "POST" and reset_delete.validate():
            login = reset_delete.login.data
            not_encrypted = reset_delete.password.data
            password = sha256_crypt.encrypt((str(reset_delete.password.data)))
            if (not_encrypted):
                dbconnect.update_user_password(login, password)
            else:
                dbconnect.delete_account(dbconnect.find_account_by_login(login))
            flash("Operacja zakończona sukcesem!")
            return redirect(url_for('homepage'))
        return  redirect(url_for('homepage'))

    except Exception as e:
        flash("Coś poszło nie tak...")
        return (str(e))

@app.route('/removeactivity/', methods=["GET", "POST"])
@login_required
def removeactivity():
    try:
        form = RemoveActivityForm(request.form)
        activity_list = [dbconnect.find_activity_name(item[0]) for item in list(dbconnect.find_activity_id_and_time_per_week_by_login(session['username']))]
        if request.method == "POST" and form.validate():
            name = form.name.data
            activity_id = dbconnect.find_activity_id(name)
            dbconnect.delete_activities_row(session["username"], activity_id)
            gc.collect()
            return redirect(url_for('userinfo'))

        return render_template("removeactivity.html", form=form, my_list = activity_list)

    except Exception as e:
        return (str(e))

@app.route('/userdata/', methods=["GET", "POST"])
@login_required
def userdata():
    try:
        form = UserActivitiesForm(request.form)
        if request.method == "POST" and form.validate():
            name = form.name.data
            surname = form.surname.data
            age = form.age.data
            weight = form.weight.data
            height = form.height.data
            sex = form.sex.data
            if ( sex == 0):
                sex = "K"
            else:
                sex = "M"
            # email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            data = (name, surname, age, weight, height, sex)
            dbconnect.update_user_data(session["username"], data)
            if(str(form.password.data)!=""):
                dbconnect.update_user_password(session["username"], password)
            gc.collect()
            return redirect(url_for('homepage'))
        data = dbconnect.find_user_by_login(session["username"])
        form.name = data[1]
        form.surname = data[2]
        form.age = data[3]
        form.weight = data[4]
        form.height = data[5]
        return render_template("userdata.html", form=form)

    except Exception as e:
        return (str(e))


@   app.route('/insertproduct/', methods=["GET", "POST"])
@login_required
@isspecialist
def insertproduct():
    try:
        form = InsertProductForm(request.form)
        if request.method == "POST" and form.validate():
            name = form.name.data
            protein = form.protein.data
            fat = form.fat.data
            carbohydrates = form.carbohydrates.data
            data = (name, protein, fat, carbohydrates)
            dbconnect.insert_product(data)
            gc.collect()
            return redirect(url_for('homepage'))
        return render_template("insertproduct.html", form=form)

    except Exception as e:
        return (str(e))
# @app.route('/<path:urlpath>', methods=['GET', 'POST'])
@app.route("/")
@app.route('/main/')
@app.route('/homepage/')
def homepage(urlpath='/'):
    return render_template("main.html")



@app.errorhandler(404)
def handle_404(e):
    return "Nie masz dostępu do tej storny"


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))

@app.route('/login/', methods=["GET", "POST"])
@logout_required
def login_page():
    error = ''
    try:
        if request.method == "POST":

            # data = c.execute("SELECT * FROM users WHERE username = '%s' " % (request.form["username"]))
            data = dbconnect.find_accountdata_by_login(request.form["username"])

            if data == 0:
                error = "Błędne dane, spróbuj ponownie."
                return render_template("login.html", error=error)


            permission = data[3]
            data = data[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                session['permission'] = permission
                flash("Udało Ci się zalogować  " + str(session["username"]))
                return redirect(url_for("homepage"))

            else:
                error = "Błędne dane, spróbuj ponownie."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        error = "Exception"
        return render_template("login.html", error=error)


@app.route('/include_example/')
def include_example():
	replies = {'Jack':'Cool post',
			   'Jane':'+1',
			   'Erika':'Most definitely',
			   'Bob':'wow',
			   'Carl':'amazing!',}
	return render_template("includes_tutorial.html", replies = replies)



@app.route('/interactive/')
def interactive():
    return render_template("interactive.html")

@app.route('/background_process/')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)

@app.route('/jinjaman/')
def jinjaman():
	try:
		data = [15, '0', 'Python is good','Python, Java, php, SQL, C++','<p><strong>Hey there!</strong></p>']
		return render_template("jinja-templating.html", data=data)
	except Exception as e:
		return(str(e))


@app.route('/converters/')
@app.route('/converters/<string:article>/<int:page>/')
def convertersexample(article="sss", page=1):
	try:
		return render_template("converterexample.html", page=page, article=article)
	except Exception as e:
		return(str(e))




@app.route('/__get_date__/')
def __get_date__():
    try:
        now = datetime.datetime.now()
        return jsonify(date=now)
    except Exception as e:
        return str(e)



@app.route('/date/')
def date():
    try:
        return render_template("date.html")
    except Exception as e:
        return str(e)


@app.route('/refresh/')
@login_required
def refresh():
    return render_template("users_table.html",
      data=get_data.prepare_correct_format(*dbconnect.select_all_test('konta'))[0],
      columns=get_data.prepare_correct_format(*dbconnect.select_all_test('konta'))[1],
      )

@app.route('/userinfo/')
@login_required
def userinfo():
    return render_template("activities_and_diets.html",
      data=get_data.prepare_correct_format(*dbconnect.select_all_test('konta'))[0],
      columns=get_data.prepare_correct_format(*dbconnect.select_all_test('konta'))[1],
      )

@app.route('/hard')
@app.route('/hard/<string:db_name>/')
def hard(db_name = " "):
    if(db_name == "wiersze_posilkow"):
        data, row_headers = dbconnect.select_all_test('wiersze_posilkow')
        data2, row_headers2 = dbconnect.select_all_test("posilki")
        data2 = get_data.make_dict_from_tuple_lists(data2)
        data3, row_headers3 = dbconnect.select_all_test("produkty")
        data3 = get_data.make_dict_from_tuple_lists(data3)
        data, row_headers = get_data.prepare_correct_format_rows(data, data2, data3)
        return jsonify(date=data, col=row_headers)
    else:
        data, row_headers = dbconnect.select_all_test(db_name)
    # row_headers = [x[0] for x in data.description]
    # data, columns = get_data(db_name)
        data, row_headers = get_data.prepare_correct_format(data, row_headers)
        return jsonify(date = data, col = row_headers)




@app.route('/hardsingle')
@app.route('/hardsingle/<string:db_name>/')
def hardsingle(db_name = "wiersze_aktywnosci"):
    if db_name == 'wiersze_aktywnosci':
        data, row_headers = dbconnect.select_all_test_for_login(db_name, session["username"])
    # row_headers = [x[0] for x in data.description]
    # data, columns = get_data(db_name)
        for item, i in zip(data, range(len(data))):
            newitem = list(item)
            newitem[1] = str(dbconnect.find_activity_name(item[1]))
            data[i] = newitem
            row_headers[1] = 'Nazwa_aktywnosci'
    else:
        name, surname = dbconnect.find_user_by_login(session["username"])[1:3]
        data, row_headers = dbconnect.select_diet_view(name, surname)
    data, row_headers = get_data.prepare_correct_format(data, row_headers)
    return jsonify(date = data, col = row_headers)

class RegistrationForm(Form):
    username = StringField('Login', [validators.Length(min=4, max=20)])
    # email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Nowe Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasło musi być takie same w obu polach')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('Akceptuję nowe warunki polityki prywatności (Zaktualizowne 26.05.2018)', [validators.DataRequired()])

class UserActivitiesForm(Form):
    name = StringField('Imie', [validators.Length(min=2, max=20), validators.DataRequired()])
    surname = StringField('Nazwisko', [validators.DataRequired()])
    password = PasswordField('Hasło')
    age = IntegerField('Wiek', [validators.NumberRange(18, 200, "Niepoprawny wiek"), validators.DataRequired()])
    weight = IntegerField('Waga', [validators.NumberRange(5, 450, "Niepoprawna waga"), validators.DataRequired()])
    height = IntegerField('Wzrost', [validators.NumberRange(5, 450, "Niepoprawny wzrost"), validators.DataRequired()])
    sex = BooleanField('Zaznacz to pole, jeśli jesteś mężczyzną')

class InsertProductForm(Form):
    name = StringField('Imie', [validators.Length(min=2, max=50), validators.DataRequired()])
    protein = IntegerField('Białko', [validators.NumberRange(0, 100, "Niepoprawna ilosc białka w 100g"), validators.DataRequired()])
    fat = IntegerField('Tłuszcze', [validators.NumberRange(0, 100, "Niepoprawna ilosc tłuszczu w 100g"), validators.DataRequired()])
    carbohydrates = IntegerField('Węgle', [validators.NumberRange(0, 100, "Niepoprawna ilosc węgli w 100g"), validators.DataRequired()])

class AddActivityForm(Form):
    name = StringField('Nazwwa_aktywnosci', [validators.Length(min=2, max=20)])
    hours = IntegerField('Liczba_godzin', [validators.DataRequired(), validators.number_range(min=0, max=168)])
class ResetPasswordForm(Form):
    login = StringField('UserLogin', [validators.DataRequired()])
    password = StringField('Password')
class ChangePermissionLevelForm(Form):
    login = StringField('UserLogin', [validators.DataRequired()])
    permission_level = IntegerField('Permission', [validators.DataRequired(), validators.number_range(min=0, max=2)])
class RemoveActivityForm(Form):
    name = StringField('Nazwwa_aktywnosci', [validators.Length(min=2, max=20)])



if __name__ == "__main__":
    # app.run()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sessions.init_app(app)

    app.debug = True
    app.run()

















