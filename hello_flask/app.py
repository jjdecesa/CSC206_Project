import time
from flask import Flask, render_template, request
app = Flask(__name__)

def intTryParse(value):
    try:
        return int(value)
    except ValueError:
        return False

def getPrimes(inp):
    sTime  = time.time()
    listOfPrime = []
    tempBool = True

    high = inp

    for all in range(3, high + 1, 2):
        tempBool = True
        #print(all, "a")
        for all2 in range(2, all):
            if (all % all2 == 0):
                tempBool = False
        
        if tempBool:
            listOfPrime.append(all)
                

    string1 = ("All primes: ", listOfPrime)
    string2 = ("Time in Seconds: ", time.time() - sTime)
    
    size = len(listOfPrime)

    if size < 20:
        string3 = ("There is less than 20 primes in the list")
        string4 = ""
    else: 
        string3 = ("First 10 primes: ", listOfPrime[0:10])
        string4 = ("Last 10 primes: ", listOfPrime[size - 10: size])

    return string1, string2, string3, string4


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<num>")
def index(num):
    
    input = intTryParse(num)

    if not (input):
        return render_template("typeError.html", top = num)

    ss = getPrimes(input)

    return render_template("index.html", s1 = ss[0], s2 = ss[1], s3 = ss[2], s4 = ss[3])


@app.route('/primeOut/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /primeOut is accessed directly. Try going to '/' to submit form"
    if request.method == 'POST':
        form_data = request.form
        input = intTryParse(form_data.get('upperLimit'))

        if not (input):
            return render_template("typeError.html", top = num)

        ss = getPrimes(input)
        return render_template("index.html", s1 = ss[0], s2 = ss[1], s3 = ss[2], s4 = ss[3])

if __name__ == '__main__':
    app.run(debug=True)

##python "app.py" //to run it




