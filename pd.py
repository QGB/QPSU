from collections import namedtuple

def df_to_namedtuples(df):
    Row = namedtuple('Row', df.columns)
    for row in df.itertuples():
        yield Row(*row[1:])
df2namedtuples=df_to_namedtuples		

