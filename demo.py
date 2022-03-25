# Horrible code, but it's a demo, no judging please.
import mariadb 
from flask import Flask, render_template

app = Flask(__name__, static_folder="")

# Credentials to connect into mariaDB,
conn = mysql.connector.connect(
    user="",
    password="",
    host="",
    port=3306,
    database="Autokauppa")

# Global variables
cursor = conn.cursor() ) 


def database_handle(target,car_id):
    if car_id != None:
        car_id = int(car_id)
    data = dict()
    count = 0

    # Select Query,

    # All Avialable cars
    if target == "cars":
       query = """
SELECT A.malli, Valmistaja.nimi, Inventaario.hinta, Inventaario.auto_id 
FROM Autot A JOIN Inventaario ON auto_id = A.id, Autot B JOIN Valmistaja ON B.valmistaja_id = Valmistaja.id
WHERE Inventaario.kpl = 1 AND A.id = B.id ;
"""
    
    # Does the car exist and is it avialable
    if target == "car_exists":
        query = "SELECT auto_id FROM Inventaario I WHERE kpl != 0;"
        
    # Further details on the selected car;
    if target == "car_details":
        query =f"""SELECT A.malli, Valmistaja.nimi, Inventaario.kilometrit, Inventaario.hinta,
A.moottoritilavuus, A.vetotapa, A.teho, A.ovet, A.polttoaine, A.vaihteisto
FROM Autot A JOIN Inventaario ON auto_id = A.id, Autot B JOIN Valmistaja ON B.valmistaja_id = Valmistaja.id
WHERE A.id = B.id AND A.id = {car_id} AND Inventaario.kpl > 0;
""" 

    # Compile the QUERY into a DICT
    cursor.execute(query)
    cur = cursor.fetchall()
    for i in cur:
        data[count] = i
        count += 1

    return data

@app.route("/")
def index():
    db_data = database_handle("cars",None)
    return render_template("index.html",data=db_data)

@app.route(f'/<file>')
def homepage(file):
    try:
        if file == "index.html":
            db_data = database_handle("cars",None)
            return render_template(file,data=db_data)

    except Exception as e:
        print(e,file)
        return f"404, /{file} is not found."

@app.route(f'/autot/<n>')
def autot_page(n):
    try:
        db_data = database_handle("car_exists",n) 
        for i in db_data:
            print(db_data[i][0], n)
            # Check if car exist's in database,
            if int(db_data[i][0]) == int(n):
                details = database_handle("car_details",n) 
                return render_template("details.html",data=details)
        else:
            return f"car not found. sorge."

    except Exception as e:
        print(e,n,db_data)
        return f"Database error."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=55006,debug=True)
    
