from flask import Flask, session, request, redirect, render_template, Blueprint, jsonify
import pandas as pd
from flask_restx import Api, Resource, fields
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.engine import URL
import os 
from prediction import predict, clean_cols

#################################################
# Flask Setup
#################################################
app = Flask(__name__,static_url_path='/static')

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/fighter_data.sqlite")


# create api blueprint 
blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, doc="/doc/")
app.register_blueprint(blueprint)

# -------------HTML pages routes------------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/predictor")
def fight_predictor():
    return render_template("predictor.html")

@app.route("/goat")
def goat():
    return render_template("goat.html")

# -------------HTML pages routes END------------- #

# -------------API routes------------- #

@api.route("/fighter_list")
class fighter_list(Resource):
    def get(self):
        df = pd.read_sql('select*from goat_data',engine)
        fighter_list = pd.DataFrame(df["name"])
        return fighter_list.to_dict()

@api.route("/predictor/<selectedFighter>")
class fighter_data(Resource):
    def get(self, selectedFighter):
        df = pd.read_sql('select*from goat_data',engine)
        df_selected_fighter = df.loc[df["name"] == selectedFighter]
        df_selected_fighter = df_selected_fighter.drop("date", axis = 1)
        return df_selected_fighter.to_dict()

@api.route("/predictor/<selectedFighter1>/<selectedFighter2>")
class prediction(Resource):
    def get(self, selectedFighter1, selectedFighter2):
        df = pd.read_sql('select*from goat_data',engine)
        df_selected_fighter1 = df.loc[df["name"] == selectedFighter1]
        df_selected_fighter2 = df.loc[df["name"] == selectedFighter2]
        fighter1, fighter2 = clean_cols(df_selected_fighter1,df_selected_fighter2)
        prediction = predict(fighter1,fighter2)
        return prediction.to_dict()

# -------------API routes END------------- #

if __name__ == '__main__':
    app.run(debug=True)
