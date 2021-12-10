import random
random.seed(42)
from virus import Virus


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        ''' We start out with is_alive = True, because we don't make vampires or zombies.
        All other values will be set by the simulation when it makes each Person object.

        If person is chosen to be infected when the population is created, the simulation
        should instantiate a Virus object and set it as the value
        self.infection. Otherwise, self.infection should be set to None.
        '''
        self._id = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None

    def did_survive_infection(self):
        ''' Generate a random number and compare to virus's mortality_rate.
        If random number is smaller, person dies from the disease.
        If Person survives, they become vaccinated and they have no infection.
        Return a boolean value indicating whether they survived the infection.
        '''
        if self.infection is not None:
            if random.random() > self.infection.mortality_rate:
                self.is_vaccinated = True
                self.infection = None
                return True
            else:
                self.is_alive = False
                return False

        else:
            return True


# thanks @angelinaolmedo7 for helping me to find the random.random() function and make it
# into a boolean value for this function.




''' These are simple tests to ensure that you are instantiating your Person class correctly. '''
def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True) # (_id, is_vaccinated, infection=None) params
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    # TODO: complete your own assert statements that test
    # the values at each attribute
    assert person._id == 2
    assert person.is_vaccinated is False
    assert person.is_alive is True
    assert person.infection is None



def test_sick_person_instantiation():
#     # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
#     # Create a Person object and give them the virus infection
    person = Person(3, False, virus)
#     # TODO: complete your own assert statements that test
#     # the values at each attribute
    assert person._id == 3
    assert person.is_vaccinated is False
    assert person.is_alive is True
    assert person.infection is virus


def test_did_survive_infection():
#     # TODO: Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
#     # TODO: Create a Person object and give them the virus infection
    person = Person(4, False, virus)

#     # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection()
#     # Check if the Person survived or not
    if survived:
        assert person._id == 4
        assert person.is_alive is True
    else:
        assert person.is_alive is False
#         # TODO: Write your own assert statements that test
#         # the values of each attribute for a Person who did not survive
        assert person.is_vaccinated is False
        assert person.infection is virus