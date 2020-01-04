from . import population_description
from . import pesel_constants
from . import pesel_composer
from .helpers import sex_number_helper
from pesel_generator.helpers import int_helper
import datetime
import calendar


class PeselGenerator:
    """
    PeselGenerator provides interface for generating massive amount of pesel numbers.
    Each instance stores internal generation state, that asserts each of newly generated pesel will be unique as
    long as pesel architecture limits are not exceeded.
    """

    order_numbers: dict = {}
    date_gen_assert: dict = {}

    def __init__(self):
        pass

    def __enter__(self):
        self.order_numbers = {}
        self.date_gen_assert = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.order_numbers = {}
        self.date_gen_assert = {}

    def gen_based_on_desc(self, population_desc: population_description.PopulationDescription) -> list:
        """
        Generates pesel numbers based on supplied population description.
        :param population_desc:
        Defined population description, that defines it's properties.
        :return:
        Returns list[tuple[dict, list[dict]]. Each tuple corresponds to defined range in population description.
        List of each tuple are pesel numbers composed by logic pesel_compose.py expressed as dictionaries.
        """
        desc_generated: list[tuple[dict, list[dict]]] = []
        for x in population_desc.population_description:
            desc_generated.append(self.gen_based_on_range(x))
        return desc_generated

    def gen_based_on_range(self, population_range: dict) -> tuple:
        """
        Generates pesel numbers based on supplied population range.
        :param population_range:
        Defined population range.
        :return:
        Returns tuple[dict, list[dict]], where first item of tuple is given to method range and second list of peseles
        expressed as dictionaries.
        """
        range_generated: list[dict] = []
        begin_age: int = population_range[pesel_constants.AGE_START_DICT_KEY]
        stop_age: int = population_range[pesel_constants.AGE_STOP_DICT_KEY]
        female_count: int = population_range[pesel_constants.FEMALE_QUANTITY]
        male_count: int = population_range[pesel_constants.MALE_QUANTITY]

        stop_begin_delta: int = stop_age - begin_age
        floor_divider = stop_begin_delta if stop_begin_delta == 1 else stop_begin_delta - (stop_begin_delta // 2)
        male_per_sub_range: list = int_helper.int_to_random_sub_int_list(male_count, male_count // floor_divider, stop_begin_delta)
        female_per_sub_range: list = int_helper.int_to_random_sub_int_list(female_count, female_count // floor_divider, stop_begin_delta)

        now = datetime.datetime.now()
        for x in range(stop_begin_delta):
            range_generated.extend(self.gen_based_on_year(now.year - x - begin_age, male_per_sub_range[x], False))
            range_generated.extend(self.gen_based_on_year(now.year - x - begin_age, female_per_sub_range[x], True))

        return population_range, range_generated

    def gen_based_on_year(self, year: int, quantity: int, sex: bool) -> list:
        """
        Generates requested number of pesel numbers for given year and sex.
        :param year:
        Year for which we want to generate pesel numbers.
        :param quantity:
        Quantity of pesel numbers to generate.
        :param sex:
        True -> female.
        False -> male.
        :return:
        Pesel numbers expressed as dictionary.
        """
        year_generated: list[dict] = []
        per_month: list[int] = int_helper.int_to_random_sub_int_list_index_limited(
            quantity,
            [calendar.monthrange(year, x + 1)[-1] * 50000 for x in range(12)])
        for month in range(12):
            year_generated.extend(
                self.gen_based_on_month(year=year, month=month + 1, quantity=per_month[month], sex=sex))

        return year_generated

    def gen_based_on_month(self, year: int, month: int, quantity: int, sex: bool) -> list:
        """
        Generates requested number of pesel numbers for given year, month and sex.
        :param year:
        Year for which we want to generate pesel numbers.
        :param month:
        Month of previously provided year for which we want to generate pesel numbers.
        :param quantity:
        Quantity of pesel numbers to generate.
        :param sex:
        True -> female.
        False -> male.
        :return:
        Pesel numbers expressed as dictionary.
        """
        month_generated: list[dict] = []
        max_month_days: int = calendar.monthrange(year, month)[-1]
        per_day: list[int] = int_helper.int_to_random_sub_int_list(quantity, 50000, max_month_days)
        for day in range(max_month_days):
            month_generated.extend(
                self.gen_based_on_day(year=year, month=month, day=day + 1, quantity=per_day[day], sex=sex))

        return month_generated

    def gen_based_on_day(self, year: int, month: int, day: int, quantity: int, sex: bool) -> list:
        """
        Generates requested number of pesel numbers for given year, month and sex.
        :param year:
        Year for which we want to generate pesel numbers.
        :param month:
        Month of previously provided year for which we want to generate pesel numbers.
        :param day:
        Day of previously provided month for which we want to generate pesel numbers.
        :param quantity:
        Quantity of pesel numbers to generate.
        :param sex:
        True -> female.
        False -> male.
        :return:
        Pesel numbers expressed as dictionary.
        """
        day_generated: list[dict] = []
        birth_date: datetime.datetime = datetime.datetime(year=year, month=month, day=day)
        for x in range(quantity):
            day_generated.append(
                self.gen_based_on_day_single(birth_date, sex))

        return day_generated

    def gen_based_on_day_single(self, birth_date: datetime.datetime, sex: bool) -> dict:
        """
        :param birth_date:
        Birthdate for witch we want to generate pesel number.
        :param sex:
        True -> female.
        False -> male.
        :return:
        Pesel number expressed as dictionary.
        """
        next_sex_index: int = 0
        next_order_number: int = 0
        day_index = int(str(birth_date.year).zfill(4) + str(birth_date.month).zfill(2) + str(birth_date.day).zfill(2))

        if day_index in self.order_numbers:

            if sex:
                last_order_number = self.order_numbers[day_index][0]
                last_sex_index = self.order_numbers[day_index][1]
                next_order_number = last_order_number + 1
                next_sex_index = last_sex_index if next_order_number <= pesel_constants.MAX_ORDER_NUMBER else last_sex_index + 1
                next_order_number = next_order_number if next_order_number <= pesel_constants.MAX_ORDER_NUMBER else 0
                self.order_numbers[day_index] = (
                    next_order_number,
                    next_sex_index,
                    self.order_numbers[day_index][2],
                    self.order_numbers[day_index][3])
            else:
                last_order_number = self.order_numbers[day_index][2]
                last_sex_index = self.order_numbers[day_index][3]
                next_order_number = last_order_number + 1
                next_sex_index = last_sex_index if next_order_number <= pesel_constants.MAX_ORDER_NUMBER else last_sex_index + 1
                next_order_number = next_order_number if next_order_number <= pesel_constants.MAX_ORDER_NUMBER else 0
                self.order_numbers[day_index] = (
                    self.order_numbers[day_index][0],
                    self.order_numbers[day_index][1],
                    next_order_number,
                    next_sex_index)
        else:
            if sex:
                self.order_numbers[day_index] = (0, 0, -1, 0)
            else:
                self.order_numbers[day_index] = (-1, 0, 0, 0)

        return pesel_composer.compose_pesel(birth_date=birth_date,
                                            order_number=next_order_number,
                                            sex=sex_number_helper.get_pesel_sex_number(next_sex_index, sex))
