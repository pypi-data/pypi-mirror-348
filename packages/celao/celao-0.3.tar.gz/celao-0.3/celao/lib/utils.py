import os



def list_datasets(directory=None):
    if directory is None:
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            print(f"Directory '{directory}' is empty.")
        return [os.path.join(directory, f) for f in files]
    except FileNotFoundError:
        print(f"Directory '{directory}' was not found.")
        return []


def select_dataset(directory="data"):
    files = list_datasets(directory)
    if not files:
        return None

    print("Available datasets:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {os.path.basename(file)}")

    while True:
        try:
            choice = int(input("Choose a dataset: "))
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                print(f"Chosen file: {selected_file}")
                return selected_file
            else:
                print("Wrong choice. Try again.")
        except ValueError:
            print("Wrong choice. Try again.")

def select_encoding_method():
    methods = ["Label Encoding","Hashing","Word2Vec","GloVe"]

    print("Methods to choose:")
    for i, method in enumerate(methods):
        print(f"{i + 1}. {method}")

    while True:
        try:
            choice = int(input("Choose encoding method: "))
            if 1 <= choice <= len(methods):
                selected_method = methods[choice - 1]
                print(f"Selected method: {selected_method}")
                return selected_method
            else:
                print("Wrong number. Try again.")
        except ValueError:
            print("Incorrect number. Try again.")

def select_correlation_method():
    methods = ["Pearson","Spearman","Kendall"]
    print("Methods to choose:")
    for i, method in enumerate(methods):
        print(f"{i + 1}. {method}")
    while True:
        try:
            choice = int(input("Choose method of correlation computation: "))
            if 1 <= choice <= len(methods):
                selected_method = methods[choice - 1]
                print(f"Selected method: {selected_method}")
                return selected_method.lower()
            else:
                print("Wrong number. Try again.")
        except ValueError:
            print("Incorrect number. Try again.")

def choose_alpha_value():
    while True:
        choice = input("Do you want to add alpha value to sigma?(y/n): ").lower()
        if choice == "y":
            alpha = float(input("Choose alpha value: "))
            return alpha
        elif choice == "n":
            alpha = 0
            return alpha
        else:
            print("Wrong choice. Try again.")
