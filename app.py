from flask import Flask, render_template, request, redirect, url_for
from data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/internships/<program_type>') #baguhin
def internships(program_type): #baguhin
    programs_list = read_programs_by_program_type(program_type) #baguhin
    return render_template("internship.html", program_type=program_type, programs=programs_list) #baguhin

@app.route('/internships/<int:program_id>') #baguhin
def program(program_id):
    program = read_programs_by_program_type(program_id) #baguhin
    return render_template("program.html",program=program) #baguhin


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processed', methods=['post'])
def processing():
    program_data = { #baguhin
        "program_type": request.form['program_type'], #baguhin
        "program_name": request.form['program_name'], #baguhin
        "salary": request.form['program_salary'], #baguhin
        "duration": request.form['program_duration'], #baguhin
        "description": request.form['program_desc'], #baguhin
        "url": request.form['program_url'] #baguhin
    }
    insert_program(program_data) #baguhin
    return redirect(url_for('internships', program_type=request.form['program_type'])) #baguhin


@app.route('/modify', methods=['post'])
def modify():
    # 1. identify whether user clicked edit or delete
       # if edit, then do this:
    if request.form["modify"] == "edit":
        # retrieve record using id
        program_id = request.form["program_id"] #baguhin
        program = read_programs_by_program_type(program_id) #baguhin
        # update record with new data
        return render_template('update.html', program=program) #baguhin
    # if delete, then do this
    elif request.form["modify"] == "delete":
        # retrieve record using id
        program_id = request.form["program_id"] #baguhin
        program = read_programs_by_program_type(program_id) #baguhin
        # delete the record
        delete_program(program_id) #baguhin
        # redirect user to pet list by pet type
        return redirect(url_for("internships", program_type=program["internship_type"])) #baguhin

@app.route('/update', methods=['post'])
def update():
    program_data = { #baguhin
        "program_id" : request.form["program_id"], #baguhin
        "program_type": request.form['program_type'], #baguhin
        "program_name": request.form['program_name'], #baguhin
        "salary": request.form['program_salary'], #baguhin
        "duration": request.form['program_duration'], #baguhin
        "description": request.form['program_desc'], #baguhin
        "url": request.form['program_url'] #baguhin
    }
    update_program(program_data) #baguhin
    return redirect(url_for('program',program_id = request.form['program_id'])) #baguhin

def delete_program(program_id): #baguhin
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM programs WHERE id = ?" #baguhin
    values = (program_id,) #baguhin
    cur.execute(query, values)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)