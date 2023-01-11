from codeforces.src.utils.utils import to_int, to_date_str


class TestUtils:
    def test_to_int(self):
        assert to_int("32") == 32
        assert to_int("32.0") == 32
        assert to_int("32.443") == 32
        assert to_int("not castable") is None
        assert to_int(None) is None

    def test_to_date_str(self):
        assert to_date_str("1652978100") == "19.05.2022"
        assert to_date_str("1652978100.932") == "19.05.2022"
        assert to_date_str("3daef3") is None
        assert to_date_str(None) is None


