from celao.lib.correlation_methods import *
from celao.lib.draw import draw_graph
from celao.lib.utils import *


def load_dataset(path_to_dataset):
    """Load dataset and return a DataFrame with the correct separator."""

    with open(path_to_dataset, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        if ',' in first_line and ';' in first_line:
            sep = None
        elif ';' in first_line:
            sep = ';'
        else:
            sep = ','

    data_frame = pd.read_csv(path_to_dataset, sep=sep)

    print("=======================================Loaded Data===================================================")
    print(data_frame.head(10))
    print("=====================================================================================================")

    return data_frame

def run_application():
    selected_dataset = select_dataset()
    if selected_dataset:
        dataset = load_dataset(selected_dataset)
        selected_encoding_method = select_encoding_method()
        if selected_encoding_method:
            selected_correlation_method = select_correlation_method()
            match selected_encoding_method:
                case "Label Encoding":
                    correlation_matrix, _, sigma = calculate_correlation_with_label_encoding(dataset,
                                                                                              method=selected_correlation_method)
                case "Hashing":
                    correlation_matrix, sigma = calculate_correlation_with_hashing(dataset,
                                                                                   method=selected_correlation_method)
                case "Word2Vec":
                    correlation_matrix, sigma = calculate_correlation_with_word2vec(dataset,
                                                                                   method=selected_correlation_method)
                case "GloVe":
                    correlation_matrix, sigma = calculate_correlation_with_pseudo_glove(dataset,
                                                                                   method=selected_correlation_method)
        dataset_name = os.path.splitext(os.path.basename(selected_dataset))[0]
        draw_graph(correlation_matrix, sigma_value=sigma, correlation_method=selected_correlation_method,
                          encoding_method=selected_encoding_method, dataset_name=dataset_name)


