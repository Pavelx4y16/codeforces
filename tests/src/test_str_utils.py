from codeforces.src.utils.str_utils import split_fio


def test_split_fio():
    test_cases = [None, "Savastseika", "Savastseika Pavel", " Savastseika    Pavel  ", "Sava stseika Pavel"]
    expected_results = [(None, None), ("Savastseika", None), ("Savastseika", "Pavel"), ("Savastseika", "Pavel"),
                        ("Sava", "stseika")]

    for test_case, expected_result in zip(test_cases, expected_results):
        assert split_fio(test_case) == expected_result
