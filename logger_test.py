from logger import Logger
from person import Person
from virus import Virus
import os

virus1 = Virus("COVID", 0.25, 0.70)
virus2 = Virus("HIV", 0.35, 0.80)

person = Person(1, False, virus1)
person2 = Person(2, True, None)
person3 = Person(3, False, virus1)
print(person3.did_survive_infection())
person4 = Person(4, False, virus2)
print(person4.did_survive_infection())



def test_write_metadata():
    logger = Logger("tester_log.txt")
    logger.write_metadata(100, 0.90, "COVID", 0.80, 0.25)

    with open('tester_log.txt', 'r') as file:
        test_value = file.read()
        assert test_value == 'Population: 100\nPercentage of population that is vaccinated: 0.9\nVirus Name: COVID\nVirus Mortality Rate: 0.8\nVirus Reproduction Rate: 0.25\n'

    os.remove('tester_log.txt')


def test_log_interaction_already_sick():
    logger = Logger("tester_log.txt")
    logger.log_interaction(person, person2, True, False, False)

    with open('tester_log.txt', 'r') as file:
        test_value = file.read()
        print(test_value)
        assert "1 didn't infect 2 because already sick \n"

    os.remove("tester_log.txt")

def test_log_interaction_vaccinated():
    logger = Logger("tester_log.txt")
    logger.log_interaction(person, person2, False, True, False)

    with open('tester_log.txt', 'r') as file:
        test_value = file.read()
        print(test_value)
        assert "1 didn't infect 2 because vaccinated \n"

    os.remove("tester_log.txt")

def test_log_interaction_infected_person():
    logger = Logger("tester_log.txt")
    logger.log_interaction(person, person2, False, False, True)


    with open('tester_log.txt', 'r') as file:
        test_value = file.read()
        print(test_value)
        assert "1 infects 2 \n"

    os.remove("tester_log.txt")

def test_infection_survival_true():
    logger = Logger("tester_log.txt")

    logger.log_infection_survival(person2, False)

    with open('tester_log.txt', "r") as file:
        test_value = file.read()
        assert "1 died from infection.\n"

    os.remove("tester_log.txt")

def test_infection_survival_false():
    logger = Logger("tester_log.txt")

    logger.log_infection_survival(person, True)

    with open('tester_log.txt', "r") as file:
        test_value = file.read()
        assert "1 survived the infection.\n"

    os.remove("tester_log.txt")

# def test_log_infection_survival():


def test_log_time_step():
    logger = Logger("tester_log.txt")

    logger.log_time_step(1)
    with open("tester_log.txt", "r") as file:
        tester_value = file.read()
        assert "Time step 1 ended, beginning 2\n"

    logger.log_time_step(2)
    with open("tester_log.txt", "r") as file:
        tester_value = file.read()
        assert "Time step 2 ended, beginning 3\n"

    os.remove("tester_log.txt")
