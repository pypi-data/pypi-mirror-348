# CELAO

CELAO is a program for visualizing Correlation N-ptychs of Linguistic Attributes.

## 🔧 Installation

1) Use the package manager [pip](https://pip.pypa.io/en/stable/) to install CELAO.

```bash
  pip install celao
```
2) Create the folder called "data" in the root of your program.
```bash
  mkdir data
```
3) Place a dataset file inside the created folder

## 🚀 Usage

```python
from celao import run_cela

if __name__ == "__main__":
    run_cela()
```

### Run your script, and CELAO will:

* Automatically load the dataset from the data/ directory

* Detect attribute relationships

* Visualize the correlation n-ptychs

## 📂 Notes

* The dataset should be in a tabular format, such as .csv

