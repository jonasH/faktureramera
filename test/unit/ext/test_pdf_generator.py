from ext.pdf_generator import split_text


def test_split_text_one_part():
    s = "a test text shorter than 50"
    exp_res = [s]
    res = split_text(s)
    assert exp_res == res


def test_split_text_too_long_word():
    s = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    exp_res = ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-", "aaaaaa"]
    res = split_text(s)
    assert exp_res == res


def test_split_text_way_too_long_word():
    s = "a" * 50 + "b" * 50 + "c" * 25
    exp_res = ["a" * 50 + "-", "b" * 50 + "-", "c" * 25]
    res = split_text(s)
    assert exp_res == res


def test_split_text():
    p1 = "a text much longer than 50 chars but the 50 mark"
    p2 = "is right in the middle of a word"
    s = f"{p1} {p2}"
    exp_res = [p1, p2]
    res = split_text(s)
    assert exp_res == res
