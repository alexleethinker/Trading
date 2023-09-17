import os

data_dir = 'investin/data' if os.getenv('DATA_DIR') == None else os.getenv('DATA_DIR')