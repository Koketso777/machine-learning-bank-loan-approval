from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np


app = Flask("Loan Elegibility Prediction")
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict",methods=["POST"])
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    if (output == 1):
        textOut = " HIGH!"
    else:
        textOut = " LOW!"

    return render_template("index.html", prediction_text= "THE PROBABILITY THAT YOUR LOAN WILL BE APPROVED IS ; {}".format(textOut))


@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == '__main__':
	app.run(debug=True)