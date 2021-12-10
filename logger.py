from person import Person
from virus import Virus
import os

class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''

    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, repro_rate):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''

        first_line = str((f"Population: {pop_size}\nPercentage of population that is vaccinated: {vacc_percentage}\nVirus Name: {virus_name}\nVirus Mortality Rate: {mortality_rate}\nVirus Reproduction Rate: {repro_rate}\n"))

        with open(self.file_name, "w") as file:
            file.write(first_line)

        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.

    def log_interaction(self, person, random_person, random_person_sick=None,random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.
s
        or the other edge cases:
        '''
        infected_person =  f"{person._id} infects {random_person._id} \n"
        already_sick = f"{person._id} didn't infect {random_person._id} because already sick \n"
        vaccinated = f"{person._id} didn't infect {random_person._id} because vaccinated \n"
        with open(self.file_name, "a") as file:
            if did_infect == True:
                file.write(infected_person)
            elif random_person_sick == True:
                file.write(already_sick)
            else:
                file.write(vaccinated)

        # TODO: Finish this method. Think about how the booleans passed (or not passed)

    def log_infection_survival(self, person, did_survive_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .did_survive_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection

        with open(self.file_name, "a") as file:
            if did_survive_from_infection == False:
                file.write(f"{person._id} died from infection.\n")
            elif did_survive_from_infection == None:
                file.write(f"{person._id} has not been infected yet.\n")
            else:
                file.write(f"{person._id} survived the infection.\n")


    def log_time_step(self, time_step_number):
        '''
        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        with open(self.file_name, "a") as file:
            file.write(f"Time step {time_step_number} ended, beginning {time_step_number + 1}\n")

