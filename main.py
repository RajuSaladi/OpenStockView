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
from TechnicalAnalysis import techinal_decider
from TextProcessing import search_understanding, strategy_understanding
from BackTesting import backtest
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
DEFAULT_BACKTEST_RESULTS = [pd.DataFrame().to_html()]
DEFAULT_STOCK = 'ACC'
DEFAULT_DATA_TYPE = 'day'


if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['.csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    session['current_stock'] = DEFAULT_STOCK
    session['data_type'] = DEFAULT_DATA_TYPE
    session['data_columns'] = COLUMNS_LIST
    session['analysis_tables'] = DEFAULT_ANALYSIS_TABLES
    session['analysis_titles'] = DEFAULT_ANALYSIS_TITLES
    session['similarity_tables'] = DEFAULT_SIMILAR_STOCKS
    session['backtest_results'] = DEFAULT_BACKTEST_RESULTS
    return run_app()

def run_app():
    update_file_path()
    data_df = get_dataframe()
    plot_json = plot_data(data_df, column_name='close')
    get_analysis(data_df)
    get_similarity()
    do_technical_analysis(data_df)
    return render_template('index.html', plot=plot_json, columns_list=session.get('data_columns', COLUMNS_LIST),
                           display_text=session.get('text_to_show_list', ["NO TEXT to DISPLAY"]),
                           analysis_tables=session.get('analysis_tables'),
                           analysis_titles=session.get('analysis_titles'),
                           similarity_tables=session.get('similarity_tables'),
                           technical_plots=session.get('technical_plots'),
                           backtest_results=session.get('backtest_results')
                           )

def update_file_path():
    stock_name = session.get('current_stock', DEFAULT_STOCK)
    type_string = session.get('data_type', DEFAULT_DATA_TYPE)
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
    stock_name, type_string = search_understanding.get_stock_info(search_string)
    session['current_stock'] = stock_name
    session['data_type'] = type_string
    update_file_path()
    print(f"New file path is {session['input_file_path']}")
    return processing_file()

def processing_file():
    print("Reading with new file.....", )
    data_df = get_dataframe()
    plot_json = plot_data(data_df, column_name='close')
    get_analysis(data_df)
    get_similarity()
    do_technical_analysis(data_df)
    return render_template('index.html', plot=plot_json, columns_list=session.get('data_columns', COLUMNS_LIST),
                           display_text=session.get('text_to_show_list', ["NO TEXT to DISPLAY"]),
                           analysis_tables=session.get('analysis_tables'),
                           analysis_titles=session.get('analysis_titles'),
                           similarity_tables=session.get('similarity_tables'),
                           technical_plots=session.get('technical_plots'),
                           backtest_results=session.get('backtest_results', DEFAULT_BACKTEST_RESULTS)
                           )

def get_dataframe():
    input_file_path = session.get('input_file_path', './data/input_file.csv')
    print(f'reading file {input_file_path}')
    data_df = pd.read_csv(input_file_path)
    data_df = data_df.drop(data_df.columns[0], axis=1)
    session['data_columns'] = data_df.columns.tolist()[1:]
    # data_df.plot(x="date", y="close", rot=90)
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
    session['similarity_tables'].append(similar_stocks.get_similar_stocks(session.get('current_stock', DEFAULT_STOCK)))

def do_technical_analysis(input_df):
    session['technical_plots'] = techinal_decider.plot_technical_graphs(input_df, short_window=20, longer_window=50)

@app.route('/runbacktest', methods=['GET', 'POST'])
def runbacktest():
    backtest_output_list = []
    print("backtest function running")
    if "strategy_text" not in request.args:
        print('No strategy_text in request')
        flash('No strategy_text in request')
        return redirect(request.url)
    strategy_text_string = request.args['strategy_text']
    """
SMA(50) crossover SMA20 BUY
RSI(14) < 40 BUY
ADX(20) > 40 BUY
RSI(14) > 70 SELL
ADX(20) > 80 SELL
    """
    print(f"strategy_text string is {strategy_text_string}")
    summary_html = "<h3> Selected backtesting stragies are  </h3>"
    strategy_info_list = strategy_understanding.get_strategies_from_text(strategy_text_string)
    for i, each_info in enumerate(strategy_info_list):
        summary_html += f"<p>{i}: {each_info}</p>"
    backtest_output_list.append(summary_html)

    print("Running Backtesting")
    data_df = get_dataframe()
    results_html = "<h3> Results for Backtesting</h3>"
    results_dict = backtest.run(data_df, strategy_info_list)
    if results_dict['Profit'] > 0:
        results_html += f"<p>Profit: {results_dict['Profit']}</p>"
    else:
        results_html += f"<p>Loss: {-1* results_dict['Profit']}</p>"
    results_html += f"<p>No of Trades: {results_dict['NoOfTrades']}</p>"
    results_html += f"<p>SuccessTrades: {results_dict['SuccessTrades']}</p>"
    results_html += f"<p>FailureTrades: {results_dict['FailureTrades']}</p>"
    results_html += f"<p>SuccessRatio: {results_dict['SuccessRatio']}</p>"
    results_html += f"<p>FailureRatio: {results_dict['FailureRatio']}</p>"
    results_html += "<h4> Trade Summary YoY Performance\n </h4>"
    results_html += results_dict['TradeSummary'].to_html()
    results_html += "<h4>More Trade Information \n </h4>"
    results_html += results_dict['TradeInfo'].to_html()
    backtest_output_list.append(results_html)

    session['backtest_results'] = backtest_output_list
    return run_app()

if __name__ == '__main__':
    app.run()