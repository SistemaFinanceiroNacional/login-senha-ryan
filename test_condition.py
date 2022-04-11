import condition

def test_projectioncolumns_returning_all_the_columns():
    x = condition.projectioncolumns(["a","b","c"])
    y = str(x)
    assert y == '"a","b","c"'

def test_projectioncolumns_with_one_column():
    x = condition.projectioncolumns(["a"])
    y = str(x)
    assert y == '"a"'

def test_columnname_only_one_column():
    x = condition.columnname("a")
    y = str(x)
    assert y == '"a"'