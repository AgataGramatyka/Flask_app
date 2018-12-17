from flask import Flask, url_for, request, render_template, make_response
import requests
from sklearn.externals import joblib
app = Flask(__name__)

darkskyapikey = '8b668ff713f28f6f70dea7d1bbe4662f'
ipstackkey = '724a2410360a41d357ce504b7d7595d9'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html', name='Agata')
    elif request.method == "POST":
        response = make_response(render_template('predict.html'))
    return response

@app.route("/about")
def about():
    return "this is the about page"

@app.route('/project', methods=["GET", "POST"])
def project():
    current_location = requests.get("http://api.ipstack.com/check", params={'access_key':ipstackkey})
    current_location = current_location.json()
    lat = current_location["latitude"]
    long = current_location["longitude"]
    weather = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(darkskyapikey, lat, long))
    weather = weather.json()
    if request.method == 'GET':
        return render_template('project.html', weather = weather)
    elif request.method == 'POST':
        nom = request.form["nom_utilisateur"]
        email = request.form["email_utilisateur"]
        response = make_response(render_template('project.html', weather = weather))
        response.set_cookie('Nom', nom)
    return response


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    regressor = joblib.load("./linear_regression_model.pkl")
    xp = [[float(request.form["regression"])]]
    y_pred = float(regressor.predict(xp))
    return render_template("predict.html", xp=xp[0][0], y_pred=y_pred)


@app.route("/urls")
def urls():
    nom = request.cookies.get('Nom')
    return render_template('url.html', nom = nom)

if __name__ == "__main__":
    app.run(debug=True)
