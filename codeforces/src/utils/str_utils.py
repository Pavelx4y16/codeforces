from typing import Tuple


def split_fio(fio: str) -> Tuple[str, str]:
    """fio: should be string of following format: '{last_name} {first_name}'"""
    last_name = None
    first_name = None
    fio = fio.strip() if fio else None
    if fio:
        fio = fio.split()
        last_name = fio[0]
        if len(fio) > 1:
            first_name = fio[1]

    return last_name, first_name
