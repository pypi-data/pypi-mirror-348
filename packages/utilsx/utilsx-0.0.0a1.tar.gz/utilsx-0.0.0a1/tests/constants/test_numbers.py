from utilsx.constants._numbers import BILLION, MILLION, THOUSAND, TRILLION


def test_numbers() -> None:
    """Test that numeric constants are mutually consistent."""
    assert BILLION / THOUSAND == MILLION
    assert MILLION * MILLION == TRILLION
