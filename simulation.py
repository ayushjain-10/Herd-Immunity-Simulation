import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, initial_infected=1, virus=None):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # TODO: Store each newly infected person's ID in newly_infected attribute.

        self.population = [] # List of Person objects
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = f"logs/{virus.name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt"
        # change recommended by TA
        self.logger = Logger(self.file_name)   # Logger object binded to self.logger


        self.newly_infected = []

    def create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used.

        ppl_infected = 0
        # (per TA) calculate number of people who need to be vaccinated based on the percentage
        # removed: random.random() < self.vacc_percentage

        peeps_vaccinated = self.pop_size * self.vacc_percentage
        while len(self.population) != self.pop_size:  # while the number of person objects in the population list is not equal to the population size
            if ppl_infected != self.initial_infected:  # if the number of ppl infected is not equal to the number passed in to initial_infected
                self.population.append(Person(self.next_person_id, False, self.virus)) # we add a person to the population list who is unvaccinated
                ppl_infected += 1
                self.next_person_id += 1
            elif peeps_vaccinated > 0:  # if the random float is less than the percentage of people who are vaccinated in the population
                self.population.append(Person(self.next_person_id, True, None))#we add a person object who is vaccinated
                self.next_person_id += 1
                peeps_vaccinated -= 1
            else:
                self.population.append(Person(self.next_person_id, False, None))#otherwise we add a person object who is unvaccinated
                self.next_person_id += 1
        self.current_infected = ppl_infected
        return self.population


    def simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        dead_count = []
        for person in self.population:
            if person.is_alive == False:
                dead_count.append(person)

        if len(dead_count) == self.pop_size: # if the whole population is dead
            return False #stop simulation

        elif self.current_infected == 0: #if no one's infected, stop sim
            return False

        else:
            return True #continue sim
        # TODO: Complete this helper method.  Returns a Boolean.

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Keep track of the number of time steps that have passed.
        # TODO: Set this variable using a helper
        time_step_counter = 0

        self.create_population(self.initial_infected)

        simulation_continue = self.simulation_should_continue()
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while simulation_continue:
            self.current_infected = 0

            for person in self.population:
                if person.infection is not None and person.is_alive == True:
                    self.current_infected += 1

            self.logger.log_time_step(time_step_counter)
            time_step_counter +=1
            self.time_step()
            simulation_continue = self.simulation_should_continue()

        print(f"{self.total_dead} people have died from infection.\n")
        print(f"The simulation is ending after {time_step_counter -1} turns.")
        print(f"Entire population is either dead or vaccinated after {time_step_counter - 1} timesteps.")

        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        for person in self.population:
            interaction_count = 0
            if person.is_alive == True and person.infection == self.virus:
                while interaction_count <= 100:
                    random_person = random.choice(self.population)
                    # person cannot interact with random dead person or itself
                    while random_person.is_alive == False or random_person._id == person._id:
                        random_person = random.choice(self.population)

                    self.interaction(person, random_person)
                    interaction_count += 1

        for person in self.population:
            if person.infection == self.virus and person.is_alive == True:
                did_survive = person.did_survive_infection()
                self.logger.log_infection_survival(person, did_survive)

                if did_survive == False:
                    self.total_dead += 1

        self.infect_newly_infected()

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated == True:
            self.logger.log_interaction(person, random_person, False, True, False)

        elif random_person.infection == self.virus:
            self.logger.log_interaction(person, random_person, True, False, False)

        elif random_person.is_vaccinated == False:
            if random.random() < virus.repro_rate:
                self.logger.log_interaction(person, random_person, False, False, True)
                self.newly_infected.append(random_person._id)
            else:
                self.logger.log_interaction(person, random_person, False, False, False)

    def infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        for id in self.newly_infected:
            for person in self.population:
                if person._id == id:
                    person.infection = self.virus
                    self.current_infected += 1
        self.newly_infected = []

        # TODO: Call this method at the end of every time step and infect each Person.

if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate,)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()

# test creat population function:
# if __name__ == "__main__":

#     virus = Virus("COVID", .25, .7)
#     sim = Simulation(30, .9, virus, 1)

#     print(sim.create_population(1))

# --- to run: python3 simulation.py virus, repro, mort, pop, vacc

