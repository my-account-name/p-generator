import random

from pesel_generator.exception.RandomPartitionerException import RandomPartitionerException


def int_to_random_sub_int_list(number: int, random_limit: int, list_size: int) -> list:
    """
    Turns given number in array of numbers of requested size.
    :param number:
    Number to transform.
    :param random_limit:
    Maximum value that can be stored at given array index.
    :param list_size:
    Size of requested sub int array.
    :return:
    List of requested size with numbers. Sum of that numbers equals given number.
    """
    random.seed()
    left_to_assign: int = number
    sub_int_list: list = [0] * list_size

    main_floor_divider_value: int = 2
    distributed_evenly: int = number // main_floor_divider_value

    if number > random_limit * list_size:
        raise RandomPartitionerException("Cannot divide number: ", number, " into: ", list_size,
                                         " random chunks with chunk limit: ",random_limit)

    if distributed_evenly > list_size:
        initial_index_value = distributed_evenly // list_size
        sub_int_list = [initial_index_value for x in range(list_size)]
        left_to_assign -= initial_index_value * list_size

    assign_limit_candidate = left_to_assign // list_size
    random_limit_assign: int = assign_limit_candidate if assign_limit_candidate >= 50 and left_to_assign > list_size else left_to_assign
    while left_to_assign != 0:
        for x in range(list_size):
            to_set = 0
            set_limit = random_limit - sub_int_list[x]
            while to_set == 0:
                random.seed()
                to_set = random.randrange(random_limit_assign)

            to_set = left_to_assign if to_set >= left_to_assign else to_set
            to_set = set_limit if to_set >= set_limit else to_set

            sub_int_list[x] += to_set
            left_to_assign -= to_set

    random.shuffle(sub_int_list)
    return sub_int_list


def int_to_random_sub_int_list_index_limited(number: int, limit_list: list) -> list:
    """
    Turns given number in array of numbers of requested size.
    :param number:
    Number to transform.
    :param limit_list:
    Array of limits.
    :return:
    List of requested size with numbers. Sum of that numbers equals given number.
    """
    random.seed()
    left_to_assign: int = number
    list_size: int = len(limit_list)
    sub_int_list: list = [0] * list_size

    main_floor_divider_value: int = 2
    distributed_evenly: int = number // main_floor_divider_value

    if number > sum(limit_list):
        raise RandomPartitionerException("Cannot divide number: ", number, " with given entry limits: ", limit_list)

    if distributed_evenly > list_size:
        initial_index_value = distributed_evenly // list_size
        sub_int_list = [initial_index_value for x in range(list_size)]
        left_to_assign -= initial_index_value * list_size

    assign_limit_candidate = left_to_assign // list_size
    random_limit_assign: int = assign_limit_candidate if assign_limit_candidate >= 50 and left_to_assign > list_size else left_to_assign
    while left_to_assign != 0:
        for x in range(list_size):
            to_set = 0
            set_limit = limit_list[x] - sub_int_list[x]
            while to_set == 0:
                random.seed()
                to_set = random.randrange(random_limit_assign)

            to_set = left_to_assign if to_set >= left_to_assign else to_set
            to_set = set_limit if to_set >= set_limit else to_set

            sub_int_list[x] += to_set
            left_to_assign -= to_set

    random.shuffle(sub_int_list)
    return sub_int_list
