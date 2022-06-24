
from flask_app import app, bcrypt
from flask import session, redirect, render_template, request, flash
from flask_app.models.register_model import Register


# Main Page


@app.route("/")
@app.route("/register")
def front_page():
    # view_page = Register.view_main_page
    return render_template("register.html")


@app.route("/register/new/user", methods=['POST'])
def create_user():
    if not Register.validate_login_creds(request.form):
        return redirect('/')
    data = {
        "email": request.form['email']
    }
    result = Register.check_user(data)

    if result == None:
        # Add new user
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
            # Confirm password is only for validations
        }
        # id for the user will be stored in session
        id = Register.create(data)
        session["user_id"] = id
        return redirect("/dashboard")
    else:
        flash(" Name and Email already is use", "error_login")
        return redirect('/')


@app.route("/dashboard")
def welcome_page():
    data = {
        "id": session["user_id"]
    }
    user = Register.get_by_id(data)

    return render_template("dashboard.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("register.html")


@app.route('/login', methods=['POST'])
def login():

    data = {
        "email": request.form['email']
    }

    result = Register.check_user(data)
    print(result)
    if result == None:
        # Display flash
        flash(" Invalid email/password", "login_creds")
        return redirect("/")
    else:
        if not bcrypt.check_password_hash(result.password, request.form['password']):
            flash(" Invalid email/password", "login_creds")
            return redirect("/login")
        else:
            session['user_id'] = result.id
            return redirect("/dashboard")


# @app.route("/display/dashboard", methods=["POST"])
# def display_dashboard():
#     return redirect("/dashboard")
