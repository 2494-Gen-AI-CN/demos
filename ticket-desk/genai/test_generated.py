import pytest

from bands import ticket_age_band


@pytest.mark.parametrize(
    "hours, expected",
    [
        (-10, "under 4"),
        (0, "under 4"),
        (3, "under 4"),
        (3.99, "under 4"),
    ],
)
def test_ticket_age_band_under_four(hours, expected):
    assert ticket_age_band(hours) == expected


@pytest.mark.parametrize(
    "hours, expected",
    [
        (4, "4 to 24"),
        (4.0, "4 to 24"),
        (5, "4 to 24"),
        (12, "4 to 24"),
        (23, "4 to 24"),
        (23.99, "4 to 24"),
        (24, "4 to 24"),
    ],
)
def test_ticket_age_band_between_four_and_twenty_four_hours(hours, expected):
    assert ticket_age_band(hours) == expected


@pytest.mark.parametrize(
    "hours, expected",
    [
        (24.01, "over 24"),
        (25, "over 24"),
        (48, "over 24"),
        (100, "over 24"),
    ],
)
def test_ticket_age_band_over_twenty_four_hours(hours, expected):
    assert ticket_age_band(hours) == expected