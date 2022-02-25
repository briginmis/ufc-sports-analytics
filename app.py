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

# USE THIS FOR AWS SET UP
# # create database engine 
# DB_USER = os.environ.get("DB_USER")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")
# DB_SERVER_NAME = os.environ.get("DB_SERVER_NAME")
# DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")

# connection_url = URL.create(
#     drivername = "postgresql+pg8000", 
#     username = DB_USER,
#     password = DB_PASSWORD,
#     host = DB_SERVER_NAME, 
#     port = 5432,
#     database = DB_DATABASE_NAME, 
# )

# engine = create_engine(connection_url)

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

# -------------HTML pages routes END------------- #

# -------------API routes------------- #
@api.route("/map_data")
class base_map(Resource):
    def get(self):
        df = pd.read_sql('select*from map_data',engine)
        base_map = df[["location", "date"]]
        base_map = df.groupby("location").count()
        return base_map.to_dict()

@api.route("/map_win_ratio")
class win_ratio_map(Resource):
    def get(self):
        df = pd.read_sql('select*from map_data',engine)
        win_ratio_map = df[["location","winratio"]]
        win_ratio_map = win_ratio_map.groupby("location").mean()
        return win_ratio_map.to_dict()

@api.route("/stance_graph")
class stance_graph(Resource):
    def get(self):
        df = pd.read_sql('select*from goat_data',engine)
        stance_df = df[["Stance","winratio"]]
        stance_df = stance_df.groupby("Stance").mean()
        return stance_df.to_dict()

@api.route("/age_graph")
class age_graph(Resource):
    def get(self):
        df = pd.read_sql('select*from goat_data',engine)
        age_df = df[["age","date"]]
        age_df = age_df.groupby("Stance").count()
        return age_df.to_dict()

@api.route("/fighter_list")
class fighter_list(Resource):
    def get(self):
        df = pd.read_sql('select*from goat_data',engine)
        fighter_list = pd.DataFrame(df["name"])
        return fighter_list.to_dict()

@api.route("/predictor/<selectedFighter>")
class predict(Resource):
    def get(self, selectedFighter):
        df = pd.read_sql('select*from goat_data',engine)
        df_selected_fighter = df.loc[df["name"] == selectedFighter]
        df_selected_fighter = df_selected_fighter.drop("date", axis = 1)
        return df_selected_fighter.to_dict()

@api.route("/prediction/<selectedFighter1>/<selectedFighter2>")
class predictor(Resource):
    def get(self, selectedFighter1, selectedFighter2):
        df = pd.read_sql('select*from goat_data',engine)
        df = df.drop(["date", "winratio"], axis = 1)
        df_selected_fighter1 = df.loc[df["name"] == selectedFighter1]
        df_selected_fighter2 = df.loc[df["name"] == selectedFighter2]
        clean_cols(df_selected_fighter1,df_selected_fighter2)
        prediction = predict(df_selected_fighter1,df_selected_fighter2)
        return prediction

# -------------API routes END------------- #

if __name__ == '__main__':
    app.run(debug=True)
