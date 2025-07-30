from ..list_ope import get_value_by_index


def test_get_value_by_index():
    value = get_value_by_index((1, 2, 3), 1)
    print(value)
