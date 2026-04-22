import pytest

class TestAthletes:

    events = ( \
        "2020-skuhrovska-lyze", \
        "2020-skuhrovska-steeplechase", \
        "2021-skuhrovska-steeplechase", \
        "2022-skuhrovska-lyze", \
        "2025-skuhrovska-lyze", \
        "2025-setkani-mistru" \
    )

    @pytest.mark.parametrize("event", events)
    def test_sort(self, event):
        assert "skuhrov" in event or "setkani-mistru" in event
