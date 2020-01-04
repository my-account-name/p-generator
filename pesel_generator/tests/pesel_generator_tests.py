import unittest

from pesel_generator.exception import PeselGeneratorException
from pesel_generator.pesel import population_description, pesel_generator


class TestPesel(unittest.TestCase):

    def test_population_description0(self):
        try:
            with population_description.PopulationDescription() as ep:
                ep.define_population_range(age_start=24, age_stop=25, female_quantity=1200, male_quantity=2400)
                ep.define_population_range(age_start=26, age_stop=28, female_quantity=1200, male_quantity=2400)
                ep.define_population_range(age_start=25, age_stop=26, female_quantity=1200, male_quantity=2400)
        except PeselGeneratorException:
            self.fail()

    def test_population_description1(self):
        with self.assertRaises(Exception):
            with population_description.PopulationDescription() as ep:
                ep.define_population_range(age_start=24, age_stop=25, female_quantity=1200, male_quantity=2400)
                ep.define_population_range(age_start=26, age_stop=28, female_quantity=1200, male_quantity=2400)
                ep.define_population_range(age_start=25, age_stop=27, female_quantity=1200, male_quantity=2400)

    def test_pesel_generator0(self):
        try:
            with population_description.PopulationDescription() as ep:
                ep.define_population_range(age_start=24, age_stop=25, female_quantity=1200, male_quantity=2400)
                ep.define_population_range(age_start=26, age_stop=28, female_quantity=1200, male_quantity=2400)
                with pesel_generator.PeselGenerator() as pg:
                    _ = pg.gen_based_on_desc(ep)

        except PeselGeneratorException:
            self.fail()


if __name__ == '__main__':
    unittest.main()
