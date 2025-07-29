from pyldplayer2.coms.instanceQuery import op_index_parse, query_str


def test_query_str():
    q1 = "id[3:] and name.startswith(a) and name(*b)"
    assert (
        query_str(q1) == 'id > 3 and name.startswith("a") and _ld_re_search("*b", name)'
    )

    # regex
    q2 = "a.*"
    assert query_str(q2) == '_ld_re_search("a.*", name)'


def test_op_index_parse():
    # Test positive indices
    assert op_index_parse("id[3:]") == "id > 3"
    assert op_index_parse("id[:3]") == "id < 3"
    assert op_index_parse("id[3:5]") == "id > 3 and id < 5"

    # Test with different variable names
    assert op_index_parse("x[3:]") == "x > 3"

    # Test invalid input (should return original string)
    assert op_index_parse("invalid") == "invalid"
    assert op_index_parse("id[abc]") == "id[abc]"
