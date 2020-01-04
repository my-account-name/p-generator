from ..pesel_constants import FEMALE_SEX_NUMBER_SET, MALE_SEX_NUMBER_SET


def get_pesel_sex_number(index: int, sex: bool):
    """
    Get pesel sex number for given sex and index.
    :param index:
    Index of requested sex number from set.
    :param sex:
    True -> female.
    False -> male.
    :return:
    Sex number from set.
    """
    return FEMALE_SEX_NUMBER_SET[index] if sex else MALE_SEX_NUMBER_SET[index]
