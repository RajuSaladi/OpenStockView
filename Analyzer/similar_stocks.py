import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


STOCKDATA_FOLDER = r"E:\PythonCodes\StockAnalysis\Data\IndianStocks_IntradayData"
SIMILARITY_FILE = './data/similarity.csv'
TOP_K = 5

class SimilarityFunction:
    def __init__(self):
        self.similarity_df = pd.DataFrame()
    
    def compute_simialrity(self):
        file_list = [os.path.join(STOCKDATA_FOLDER, x) for x in os.listdir(STOCKDATA_FOLDER) if x.endswith('_day_data.csv')]
        all_stock_df = pd.DataFrame()
        for i in range(0, len(file_list)):
            data_df = pd.read_csv(file_list[i])
            data_df = data_df.drop(data_df.columns[0], axis=1)
            data_df['date'] = pd.to_datetime(data_df['date'])
            data_df.set_index('date', inplace=True)
            stock_variation = data_df['close'].pct_change().fillna(0)
            stock_variation.name = os.path.basename(file_list[i]).split('_')[0]
            all_stock_df = pd.concat((all_stock_df, stock_variation), axis=1)
        all_stock_df.fillna(0, inplace=True)
        similarity_df = pd.DataFrame(cosine_similarity(all_stock_df.T), columns= all_stock_df.columns, index=all_stock_df.columns)
        del all_stock_df
        similarity_df.to_csv(SIMILARITY_FILE)


def read_similarity_info():
    similarity_df = pd.read_csv(SIMILARITY_FILE)
    similarity_df.rename(columns={'Unnamed: 0': 'StockName'}, inplace=True)
    similarity_df.set_index('StockName', inplace=True)
    return similarity_df

def get_similar_stocks(input_stock):
    similarity_df = read_similarity_info()
    output_df = similarity_df.loc[input_stock].sort_values(ascending=False).iloc[1:TOP_K+1].to_frame().reset_index()
    output_df.columns = ['Stocks', 'Similarity Score']
    return output_df.to_html(classes="Similarity")
