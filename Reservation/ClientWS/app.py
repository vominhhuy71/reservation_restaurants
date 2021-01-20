from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def check_booking(timeslot, available,res_name):
    response = requests.get("http://localhost:5000/restrv1/{}/timeslots".format(res_name))
    timeslots=response.json()
    result = True
    temp_timeslots=[]
    
    #Check available
    for member in timeslots:
        if timeslot == member["timeslot"]:
            if available != member["available"]:
                result = False
        temp_timeslots.append(member["timeslot"])
    #Check timeslot    
    if timeslot not in temp_timeslots:
        result = False
    return result
            
       
@app.route("/reservation")
def reservation():
    response = requests.get("http://localhost:5000/restrv1/get_restaurant")   
    return render_template("reservation.html",restaurants=response.json())
    
@app.route("/resv/<string:res_name>")
def available(res_name):
    response = requests.get("http://localhost:5000/restrv1/{}/timeslots".format(res_name))
    
    return render_template("resv.html",name=res_name, timeslots=response.json())
   
    
@app.route("/booking/<string:res_name>/<string:timeslot>/<int:available>",methods=['GET','POST'])
def booking_form(res_name,timeslot,available):
    if request.method == 'POST':
        check = check_booking(timeslot,available,res_name)
        if available == 0 or check == False:
            return render_template("booking.html", timeslot = timeslot, available=available, res_name = res_name)          
        booking = {
            'name': request.form["name"],
            'timeslot': timeslot,
            'seats': request.form["seats"]
        }
        print(request.form["name"])
        print(request.form["seats"])
        
        if int(request.form["seats"]) > available:
            return render_template("booking.html", timeslot = timeslot, available=available, res_name = res_name)
            
        headers = {'content-type': 'application/json'}    
        r = requests.put('http://localhost:5000/restrv1/{}/booking'.format(res_name), data=json.dumps(booking),headers=headers)
        if r.status_code == 200:
            return render_template("index.html")
            
    return render_template("booking.html", timeslot = timeslot, available=available, res_name = res_name)


   
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)