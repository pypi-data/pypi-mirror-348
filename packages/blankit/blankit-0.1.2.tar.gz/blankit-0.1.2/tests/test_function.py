def test_basic():
    assert len("mango") == 5

def test_pandas_simple():
    import pandas as pd 
    df = pd.DataFrame(data={'col1': [1,2,3]})
    assert df.shape[0] == 3