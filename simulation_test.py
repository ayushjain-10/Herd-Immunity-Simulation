from simulation import Simulation
# import simulation
from person import Person
from virus import Virus
import unittest
import pytest

initial_infected = 12


class xfunction(unittest.TestCase):

    def xtype_of_cases(self):
        # tests normal cases (x,y,z)
        virus = Virus("COVID", .25, .7)
        sim = Simulation(100, .9, virus, 1)
        assert sim.create_population(1) is []

    def test_simulation_init(self):
        virus = Virus("AIDS", .25, .7)
        sim = Simulation(100, 0.75, 1, virus)
        assert sim.pop_size == 100
        assert sim.vacc_percentage == 0.75
        assert sim.initial_infected == 1
        assert sim.virus == virus

    def test_create_population(self):
        virus = Virus("AIDS", .25, .7)
        sim = Simulation(4, 0.75, 1, virus)
        expected_pop = [Person(0, True, None), Person(1, True, None),
                        Person(2, True, None), Person(3, False, "AIDS")]
        pop_test_result = sim.create_population(1)
        # check that expected == test result
        print(expected_pop, pop_test_result)
        assert len(pop_test_result) == len(expected_pop)

        check_vacc_count = 0
        for person in pop_test_result:
            if person.is_vaccinated:
                check_vacc_count += 1

        assert check_vacc_count == 3



if __name__ == '__main__':
    unittest.main()