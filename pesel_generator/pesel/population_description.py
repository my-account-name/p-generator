from pesel_generator.exception.PeselGeneratorException import PeselGeneratorException
from . import pesel_constants


class PopulationDescription:

    population_description: list = []

    def __init__(self):
        pass

    def __enter__(self):
        self.population_description = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.population_description = []

    def define_population_range(self, age_start: int, age_stop: int, female_quantity: int, male_quantity: int) -> None:
        """
        Adds new population range.
        :param age_start:
        Begin age.
        :param age_stop:
        Final age.
        :param female_quantity:
        Quantity of females in population.
        :param male_quantity:
        Quantity of females in population.
        :return:
        None
        """
        if age_start >= age_stop:
            raise PeselGeneratorException("age_start cannot be equal or greater than to age_stop.")

        temp: dict = {
            pesel_constants.AGE_START_DICT_KEY: age_start,
            pesel_constants.AGE_STOP_DICT_KEY: age_stop,
            pesel_constants.FEMALE_QUANTITY: female_quantity,
            pesel_constants.MALE_QUANTITY: male_quantity
        }
        self.__verify_given_range(temp)
        self.population_description.append(temp)

    def __verify_given_range(self, population_range_candidate: dict) -> None:
        """
        Internal method for checking if 2 ranges are not covering each other. Throws an exception if assertion failed.
        :param population_range_candidate:
        Range to check
        :return:
        None
        """
        for pop_range in self.population_description:
            existing_range: range = range(pop_range[pesel_constants.AGE_START_DICT_KEY],
                                          pop_range[pesel_constants.AGE_STOP_DICT_KEY])
            if population_range_candidate[pesel_constants.AGE_START_DICT_KEY] in existing_range or\
                    population_range_candidate[pesel_constants.AGE_STOP_DICT_KEY] in existing_range[1:]:
                raise PeselGeneratorException('Range collision detected. '
                                'There is already range that covers part of new defined range.'
                                'Existing range: ', pop_range,
                                'New defined range: ', population_range_candidate)
