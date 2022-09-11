import pandas

def parse_df(path):
    return pandas.read_csv(path, skipinitialspace = True).fillna("")