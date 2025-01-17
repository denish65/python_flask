from flask import Flask, render_template,request,redirect,url_for,flash
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flask_crud"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)

class Data(db.Model):
      id = db.Column(db.Integer,primary_key = True)
      name = db.Column(db.String(100))
      email = db.Column(db.String(100))
      phone = db.Column(db.String(100))

      def __init__(self,name,email,phone):
            self.name = name
            self.email = email
            self.phone = phone

@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html",emp =all_data)

@app.route('/insert',methods = ['POST'])
def insert():
     if request.method == 'POST':
          name = request.form['name']
          email = request.form['email']
          phone = request.form['phone']

          my_data = Data(name,email,phone)    
          db.session.add(my_data)
          db.session.commit()

          flash("data add successfully")

          return redirect(url_for('Index'))


@app.route("/update",methods = ["GET",'POST'])
def update():
     if request.method == "POST":
          my_data = Data.query.get(request.form.get("id"))
          
          my_data.name = request.form["name"]
          my_data.email = request.form["email"]
          my_data.phone = request.form["phone"]

          db.session.commit()
          flash("data updated success fully")

          return redirect(url_for("Index"))
          

@app.route("/delete/<id>/",methods = ["GET","POST"])
def delete(id):
      my_data = Data.query.get(id)
      db.session.delete(my_data)
      db.session.commit()
      flash("data deleted success fully")

      return redirect(url_for("Index"))




with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)