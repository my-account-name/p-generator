import time
from pesel_generator.pesel import pesel_generator, population_description

"""
Simple example of pesel generator usage.
"""

example_population = population_description.PopulationDescription()
example_population.define_population_range(age_start=24, age_stop=25, female_quantity=128432, male_quantity=240000)
example_population.define_population_range(age_start=20, age_stop=24, female_quantity=112320, male_quantity=324000)
xd = 2
example_population.define_population_range(age_start=33, age_stop=37, female_quantity=12000, male_quantity=2400000)
example_population.define_population_range(age_start=51, age_stop=53, female_quantity=1324331, male_quantity=2400000)

generator = pesel_generator.PeselGenerator()

start = time.time()
results = generator.gen_based_on_desc(example_population)
# results = generator.gen_based_on_year(1960, 600000, True)
stop = time.time()
print(stop-start)
#print(results)