from datetime import date
import pytest

from descriptor import BankCard


@pytest.mark.parametrize(
    "input_card_type", [1, 0.1, [1, 2, 3], (1, 2, 3), {"1": 1}, None]
)
def test_card_type_type(input_card_type):
    with pytest.raises(TypeError) as exception:
        assert BankCard(input_card_type, "5555555555555555", date(2024, 10, 29))
    assert "Card type must be str" in str(exception.value)


@pytest.mark.parametrize("input_card_type", ["VISA", "MIR", "MASTERCARD"])
def test_correct_card_type(input_card_type):
    visa_card = BankCard(input_card_type, "5555555555555555", date(2024, 10, 29))
    assert visa_card.card_type == input_card_type


@pytest.mark.parametrize(
    "input_card_type, expected_card_type",
    [("vIsA", "VISA"), ("MiR", "MIR"), ("mastercard", "MASTERCARD")],
)
def test_input_card_type_case_insensitive(input_card_type, expected_card_type):
    visa_card = BankCard(input_card_type, "5555555555555555", date(2024, 10, 29))
    assert visa_card.card_type == expected_card_type


def test_incorrect_card_type():
    with pytest.raises(ValueError) as exception:
        assert BankCard("EXPRESS", "5555555555555555", date(2024, 10, 29))
    assert "Allowed card types: VISA, MASTERCARD, MIR" in str(exception.value)


@pytest.mark.parametrize("input_number", [1, 0.1, [1, 2, 3], (1, 2, 3), {"1": 1}, None])
def test_card_number_type(input_number):
    with pytest.raises(TypeError) as exception:
        assert BankCard("VISA", input_number, date(2024, 10, 29))
    assert "Card number must be str" in str(exception.value)


def test_correct_card_number():
    card = BankCard("VISA", "1616161616161616", date(2024, 10, 29))
    assert card.number == "1616161616161616"


@pytest.mark.parametrize("input_number", ["1", "151515151515151", "17171717171717171"])
def test_incorrect_card_number_length(input_number):
    with pytest.raises(ValueError) as exception:
        assert BankCard("VISA", input_number, date(2024, 10, 29))
    assert "Card number must consist of exactly 16 digits" in str(exception.value)


def test_card_number_is_not_digit():
    with pytest.raises(ValueError) as exception:
        assert BankCard("VISA", "16CharString0000", date(2024, 10, 29))
    assert "Card number must consist of exactly 16 digits" in str(exception.value)


@pytest.mark.parametrize(
    "input_date",
    [
        (6, 10, 2024),
        [6, 10, 2024],
        "06-10-2024",
        6102024,
        {"date": "06-10-2024"},
        0.1,
        None,
    ],
)
def test_expiration_date_type(input_date):
    with pytest.raises(TypeError) as exception:
        assert BankCard("VISA", "1234123412341234", input_date)
    assert "Expiration date must be datetime.date object" in str(exception.value)


@pytest.mark.parametrize(
    "input_date", [date(2022, 10, 10), date(2024, 10, 11), date(2025, 1, 1)]
)
def test_correct_expiraton_date(input_date):
    card = BankCard("VISA", "1234123412341234", input_date)
    assert card.expiration_date == input_date
