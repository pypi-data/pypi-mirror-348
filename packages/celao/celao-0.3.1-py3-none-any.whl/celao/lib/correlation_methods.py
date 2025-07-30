from sklearn.preprocessing import LabelEncoder
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
import celao.lib.utils as utils
import hashlib


def calculate_correlation_with_label_encoding(data_frame, method: str):
    """Calculate correlation, including string attributes with Label Encoding."""
    print("Started Label Encoding correlation calculation...")
    alpha = utils.choose_alpha_value()
    label_encoders = {}
    encoded_columns = []

    new_data_frame = data_frame.copy()

    for name in data_frame.columns:
        if data_frame[name].dtype == 'object':
            label_encoder = LabelEncoder()
            new_column_name = f"{name}_LE"
            new_data_frame[new_column_name] = label_encoder.fit_transform(data_frame[name]) + 1
            label_encoders[name] = label_encoder
            encoded_columns.append(new_column_name)
    encoded_colums_counter = len(encoded_columns)
    print(f"Encoding columns quantity: {encoded_colums_counter}")
    new_data_frame.drop(columns=[name for name in data_frame.columns if data_frame[name].dtype == 'object'], inplace=True)

    correlation_matrix = new_data_frame.corr(method=method)
    print("=======================================Correlation Matrix===================================================")
    print(correlation_matrix)
    print("============================================================================================================")
    print("=======================================Columns that were label encoded======================================")
    print(encoded_columns)
    print("============================================================================================================")

    sigma = correlation_matrix.values.std() + alpha
    print("=======================================Sigma value==========================================================")
    print(sigma)
    print("============================================================================================================")
    np.fill_diagonal(correlation_matrix.values, 0)

    filtered_correlation = np.where(
        (correlation_matrix > sigma) | (correlation_matrix < -sigma),
        correlation_matrix,
        0
    )

    filtered_correlation_df = pd.DataFrame(filtered_correlation,
                                           index=correlation_matrix.index,
                                           columns=correlation_matrix.columns)
    print("Finished Label Encoding correlation calculation.")
    print("Saving result to csv file...")
    new_data_frame.to_csv("dataframe_LE.csv")
    correlation_matrix.to_csv("correlation_matrix_LE.csv")
    print("Finished saving result to csv file...")
    return filtered_correlation_df, label_encoders, sigma

def simple_string_hash(value: str, n_buckets: int = 1000) -> int:
    """Hash a string into an integer bucket using SHA256."""
    return int(hashlib.sha256(value.encode()).hexdigest(), 16) % n_buckets

def calculate_correlation_with_hashing(data_frame: pd.DataFrame, method: str):
    """Calculate correlation using manual hashing for categorical attributes."""
    print("Started manual Hashing correlation calculation...")

    alpha = utils.choose_alpha_value()
    n_buckets = 1000

    new_data_frame = data_frame.copy()
    encoded_columns = []

    for name in data_frame.columns:
        if data_frame[name].dtype == 'object':
            print(f"Hashing column: {name}")
            new_column_name = f"{name}_HS"
            new_data_frame[new_column_name] = data_frame[name].astype(str).apply(lambda x: simple_string_hash(x, n_buckets))
            encoded_columns.append(new_column_name)

    print(f"Encoded columns count: {len(encoded_columns)}")

    new_data_frame.drop(columns=[name for name in data_frame.columns if data_frame[name].dtype == 'object'], inplace=True)

    correlation_matrix = new_data_frame.corr(method=method)

    print("======================================= Correlation Matrix ===============================================")
    print(correlation_matrix)
    print("==========================================================================================================")
    print("======================================= Encoded columns ==================================================")
    print(encoded_columns)
    print("==========================================================================================================")

    correlation_matrix.fillna(0, inplace=True)
    sigma = correlation_matrix.values.std() + alpha

    print("======================================= Sigma value ======================================================")
    print(sigma)
    print("==========================================================================================================")

    np.fill_diagonal(correlation_matrix.values, 0)

    filtered_correlation = np.where(
        (correlation_matrix > sigma) | (correlation_matrix < -sigma),
        correlation_matrix,
        0
    )

    filtered_correlation_df = pd.DataFrame(filtered_correlation,
                                           index=correlation_matrix.index,
                                           columns=correlation_matrix.columns)

    print("Finished manual Hashing correlation calculation.")
    print("Saving result to CSV file...")
    new_data_frame.to_csv("dataframe_HS.csv", index=False)
    correlation_matrix.to_csv("correlation_matrix_HS.csv")
    print("Finished saving result to CSV file.")

    return filtered_correlation_df, sigma



def calculate_correlation_with_word2vec(data_frame, method: str):
    """Calculate correlation using Word2Vec encoding for categorical attributes."""
    print("Starting Word2Vec correlation calculation.")
    alpha = utils.choose_alpha_value()
    encoded_columns = []
    for name in data_frame.columns:
        if data_frame[name].dtype == 'object':
            unique_values = data_frame[name]
            sentences = [[str(val)] for val in unique_values]
            model = Word2Vec(sentences, vector_size=1, min_count=1)
            value_to_vector = {val: model.wv[str(val)] for val in unique_values}
            vector_df = data_frame[name].map(value_to_vector).apply(pd.Series)
            vector_df.columns = [f"{name}_vec_{i}" for i in range(1)]
            data_frame = pd.concat([data_frame.drop(columns=[name]), vector_df], axis=1)
            encoded_columns.append(name)
    encoded_colums_counter = len(encoded_columns)
    print(f"Encoding columns quantity: {encoded_colums_counter}")
    correlation_matrix = data_frame.corr(method=method)
    print("=======================================Correlation Matrix===================================================")
    print(correlation_matrix)
    print("============================================================================================================")
    print("=======================================Columns that were word2vec encoded===================================")
    print(encoded_columns)
    print("============================================================================================================")

    sigma = correlation_matrix.values.std() + alpha
    print("=======================================Sigma value==========================================================")
    print(sigma)
    print("============================================================================================================")
    np.fill_diagonal(correlation_matrix.values, 0)

    filtered_correlation = np.where(
        (correlation_matrix > sigma) | (correlation_matrix < -sigma),
        correlation_matrix,
        0
    )

    filtered_correlation_df = pd.DataFrame(filtered_correlation,
                                           index=correlation_matrix.index,
                                           columns=correlation_matrix.columns)
    print("Finished Word2Vec correlation calculation.")
    print("Saving result to csv file...")
    data_frame.to_csv("dataframe_W2V.csv")
    correlation_matrix.to_csv("correlation_matrix_W2V.csv")
    print("Finished saving result to csv file...")
    return filtered_correlation_df, sigma


def calculate_correlation_with_pseudo_glove(data_frame, method: str, vector_size=1):
    print("Started GloVe correlation calculation")
    alpha = utils.choose_alpha_value()
    np.random.seed(42)
    encoded_columns = []

    for name in data_frame.columns:
        if data_frame[name].dtype == 'object':
            unique_values = data_frame[name].unique()
            value_to_vector = {val: np.random.rand(vector_size) for val in unique_values}
            vector_df = data_frame[name].map(value_to_vector).apply(pd.Series)
            vector_df.columns = [f"{name}_vec_{i}" for i in range(vector_size)]
            data_frame = pd.concat([data_frame.drop(columns=[name]), vector_df], axis=1)
            encoded_columns.append(name)
    encoded_colums_counter = len(encoded_columns)
    print(f"Encoding columns quantity: {encoded_colums_counter}")
    correlation_matrix = data_frame.corr(method=method)
    print("=======================================Correlation Matrix===================================================")
    print(correlation_matrix)
    print("============================================================================================================")
    print("=======================================Columns that were pseudo-glove encoded===============================")
    print(encoded_columns)
    print("============================================================================================================")

    sigma = correlation_matrix.values.std() + alpha
    print("=======================================Sigma value==========================================================")
    print(sigma)
    print("============================================================================================================")
    np.fill_diagonal(correlation_matrix.values, 0)

    filtered_correlation = np.where(
        (correlation_matrix > sigma) | (correlation_matrix < -sigma),
        correlation_matrix,
        0
    )
    filtered_correlation_df = pd.DataFrame(filtered_correlation,
                                           index=correlation_matrix.index,
                                           columns=correlation_matrix.columns)
    print("Finished GloVe correlation calculation")
    print("Saving result to csv file...")
    data_frame.to_csv("dataframe_PG.csv")
    correlation_matrix.to_csv("correlation_matrix_PG.csv")
    print("Finished saving result to csv file...")
    return filtered_correlation_df, sigma