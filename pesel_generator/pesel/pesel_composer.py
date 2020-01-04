import datetime


"""
More possible pesel weights:
(3 9 1 7 3 9 1 7 3 9 3)
(9 7 3 1 9 7 3 1 9 7 9)
(7 1 9 3 7 1 9 3 7 1 7)
"""


def __compute_pesel_control_number(pesel: str) -> int:
    """
    :arg pesel: First 10 digits of pesel number as string.
    :rtype: Control number of given pesel number as single digit.
    """
    weights: list = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    accumulator: int = 0

    for x in range(10):
        accumulator += int(pesel[x]) * weights[x]

    return accumulator % 10


def verify_pesel(pesel: str) -> bool:
    """
    :param pesel: Pesel number we want to verify.
    :return: Result of verification.
    """
    return __compute_pesel_control_number(pesel[:10]) == int(pesel[10])


def compose_pesel(birth_date: datetime.datetime, order_number: int, sex: int) -> dict:
    """
    :arg birth_date: Desired birth date of pesel number.
    :arg order_number: Desired order number.
    :arg sex: Desired sex number. Even --> female, Odd --> male.
    :rtype: Dictionary witch represents pesel.
    """
    pesel_candidate: str = birth_date.strftime('%y%m%d') + str(order_number).zfill(4) + str(sex)
    control_number: int = __compute_pesel_control_number(pesel_candidate)
    pesel_candidate += str(control_number)

    return {
        'birth_date': birth_date,
        'order_number': order_number,
        'sex': sex,
        'control_number': control_number,
        'pesel': pesel_candidate
    }





