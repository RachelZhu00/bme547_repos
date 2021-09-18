


def test_celsius_to_farhenheit():
    from temp_conversion import celsius_to_farhenheit
    result = celsius_to_farhenheit(20)
    expected = 68
    assert result == expected
