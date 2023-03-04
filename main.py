import os
import matplotlib.pyplot as plt
from flask import Flask, flash, request, redirect, render_template, session
from werkzeug.utils import secure_filename
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from Analyzer import analyze
from Analyzer import similar_stocks
import json
import pdb

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
DATA_FOLDER = r"E:\PythonCodes\StockAnalysis\Data\IndianStocks_IntradayData"
COLUMNS_LIST = ['open', 'close', 'high', 'low', 'volume']
DEFAULT_ANALYSIS_TABLES = [pd.DataFrame().to_html(), pd.DataFrame().to_html()]
DEFAULT_ANALYSIS_TITLES = ['year', 'month']
DEFAULT_SIMILAR_STOCKS = [pd.DataFrame().to_html()]

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['.csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    session['current_stock'] = 'ACC'
    session['data_type'] = 'day'
    session['data_columns'] = COLUMNS_LIST
    session['analysis_tables'] = DEFAULT_ANALYSIS_TABLES
    session['analysis_titles'] = DEFAULT_ANALYSIS_TITLES
    session['similarity_tables'] = DEFAULT_SIMILAR_STOCKS
    update_file_path()
    data_df = get_dataframe()
    plot_json = plot_data(data_df, column_name='close')
    get_analysis(data_df)
    get_similarity()
    return render_template('index.html', plot=plot_json, columns_list=session.get('data_columns', COLUMNS_LIST),
                           display_text=session.get('text_to_show_list', ["NO TEXT to DISPLAY"]),
                           analysis_tables=session.get('analysis_tables'),
                           analysis_titles=session.get('analysis_titles'),
                           similarity_tables=session.get('similarity_tables')
                           )

def update_file_path():
    stock_name = session.get('current_stock')
    type_string = session.get('data_type')
    session['input_file_path'] = os.path.join(DATA_FOLDER, "_".join([stock_name, type_string, 'data.csv']))
    session['text_to_show_list'] = [f"Selected Stock is {stock_name} at a {type_string} data"]

def allowed_file(input_filename):
    print(f'Checking for filename, {input_filename}')
    if not input_filename.endswith('.csv'):
        return False
    return  True

@app.route('/forward', methods=['POST'])
def read_uploaded_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'filename' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['filename']
        if file.filename == '':
            print('No file selected for uploading')
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(new_uploaded_file_path)
            print('File successfully uploaded')
            flash(f'File successfully uploaded in {new_uploaded_file_path}')
            session['input_file_path'] = new_uploaded_file_path
            return processing_file()
        else:
            print('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/search', methods=['POST', 'GET'])
def search_stock():
    if 'search' not in request.args:
        print('No search in request')
        flash('No search in request')
        return redirect(request.url)
    search_string = request.args['search']
    print(f"search string is {search_string}")
    stock_info_list = search_string.split(' ')
    stock_name = stock_info_list[0].upper()
    if len(stock_info_list) > 1:
        type_string = stock_info_list[1]+"minute"
    else:
        type_string = 'day'
    session['current_stock'] = stock_name
    session['data_type'] = type_string
    update_file_path()
    print(f"New file path is {session['input_file_path']}")
    return processing_file()

def display_text():
    print("displaying text")
    text_to_show_list = session.get('text_to_show_list')

def processing_file():
    print("Reading with new file.....", )
    data_df = get_dataframe()
    plot_json = plot_data(data_df, column_name='close')
    get_analysis(data_df)
    get_similarity()
    return render_template('index.html', plot=plot_json, columns_list=session.get('data_columns', COLUMNS_LIST),
                           display_text=session.get('text_to_show_list', ["NO TEXT to DISPLAY"]),
                           analysis_tables=session.get('analysis_tables'),
                           analysis_titles=session.get('analysis_titles'),
                           similarity_tables=session.get('similarity_tables')
                           )

def get_dataframe():
    input_file_path = session.get('input_file_path', './data/input_file.csv')
    print(f'reading file {input_file_path}')
    data_df = pd.read_csv(input_file_path)
    data_df = data_df.drop(data_df.columns[0], axis=1)
    session['data_columns'] = data_df.columns.tolist()[1:]
    data_df.plot(x="date", y="close", rot=90)
    return data_df

@app.route('/plot', methods=['GET', 'POST'])
def change_plot():
    column_name = request.args['selected']
    update_file_path()
    data_df = get_dataframe()
    get_analysis(data_df)
    get_similarity()
    return plot_data(data_df, column_name)

def plot_data(input_df, column_name=None):
    print(f'plotting data....with {column_name} column')
    fig = px.line(input_df, x='date', y=column_name, title='Time Series with Rangeslider')
    fig.update_xaxes(rangeslider_visible=True)
    return fig.to_json()

def get_analysis(input_df):
    session['analysis_tables'], session['analysis_titles'] = analyze.run(input_df)

def get_similarity():
    session['similarity_tables'] = []
    session['similarity_tables'].append(similar_stocks.get_similar_stocks(session['current_stock']))


if __name__ == '__main__':
    app.run()