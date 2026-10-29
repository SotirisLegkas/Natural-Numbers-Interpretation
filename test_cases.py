import pytest
from phone_number_interpretator import potential_numbers, check_validation


def test_ambiguity_1():
    # 20 5 -> 205 or 25
    result = potential_numbers("20 5")

    assert set(result) == {"205", "25"}


def test_ambiguity_2():
    # 75 -> 75 or 705
    result = potential_numbers("75")

    assert set(result) == {"75", "705"}


def test_ambiguity_3():
    # 725 -> 725, 700205, 70025, or 7205
    result = potential_numbers("725")

    assert set(result) == {"725","700205","70025","7205"}


def test_ambiguity_4_without_next_sequence():
    # 720 -> 720 or 70020
    result = potential_numbers("720")

    assert set(result) == {"720", "70020"}


def test_ambiguity_4_with_next_sequence():
    # 720 5 -> 7205, 700205, 725, or 70025
    result = potential_numbers("720 5")

    assert set(result) == {"7205","700205","725","70025"}


def test_ambiguity_5():
    # 702 -> 702 or 7002
    result = potential_numbers("702")

    assert set(result) == {"702", "7002"}


def test_ambiguity_6_with_one_digit_next_sequence():
    # 700 5 -> 7005 or 705
    result = potential_numbers("700 5")

    assert set(result) == {"7005", "705"}


def test_ambiguity_6_with_two_digit_next_sequence():
    # 700 14 -> 70014 or 714 or 7104 or 700104
    result = potential_numbers("700 14")

    assert set(result) == {"70014", "714", "7104", "700104"}


def test_ambiguity_6_with_11_next_sequence():
    # 700 11-> 70011 or 711
    result = potential_numbers("700 11")

    assert set(result) == {"711", "70011"}


def test_ambiguous_sequences_1():
    result = potential_numbers("2 10 6 9 30 6 6 4")

    assert set(result) == {"2106930664","210693664", "21693664", "216930664"} # Different from example

def test_ambiguous_sequences_2():
    result = potential_numbers("2 10 69 30 6 6 4")

    assert set(result) == {"2106930664","210693664", "2106093664", "21060930664"}


@pytest.mark.parametrize(
    "phone_number",
    [
        "2123456789",       # 10 digits, starts with 2
        "6912345678",       # 10 digits, starts with 69
        "00302123456789",   # 14 digits, starts with 00302
        "00306912345678",   # 14 digits, starts with 003069
    ],
)
def test_check_validation_valid(phone_number):
    assert check_validation(phone_number) is True


@pytest.mark.parametrize(
    "phone_number",
    [
        "1123456789",       # Invalid prefix
        "6812345678",       # Invalid prefix
        "212345678",        # 9 digits
        "21234567890",      # 11 digits
        "00304123456789",   # Invalid prefix
        "0030212345678",    # 13 digits
        "003021234567890",  # 15 digits
        "",
    ],
)
def test_check_validation_invalid(phone_number):
    assert check_validation(phone_number) is False
