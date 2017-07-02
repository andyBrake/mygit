#! /usr/local/bin/python3

import cgitb
import cgi
import athletemodel
import yate

cgitb.enable()

athletes = athletemodel.get_from_store()

form_data = cgi.FieldStorage()

athlete_name = form_data['which_athlete'].value

if not athlete_name:
    exit()

print(yate.start_response())
print(yate.include_header("coach kelly's timing data:"))
print(yate.header("Athlete:" + athlete_name + ", DOB:"
                  + athletes[athlete_name].dob + ""))

print(yate.para("The top 3 time:"))
print(yate.u_list(athletes[athlete_name].top3))
print(yate.include_footer({"Home:" : "../index.html",
                           "selcet another athlete" : "generate_list.py"}))
