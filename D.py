'''
@ Description:
@ Author: Sri Ram Sagar Kappagantula,
          Harsimrat Kaur and
          Ritika De.
@ Date:
'''
import re
import logging
from random import randint

# Questions library based on state.
STATE_Q_LIBRARY = {'GREET': {1:'Hi! I am {}!', 2:'Hello! This is {}!', 3:'I am {}, and you are?'}, 
                   'CONFUSED': {1:'Hmmm! Can you elaborate {}.', 2:'Tell me more! {}', 3:'I did not understand what you said. {}!'},
                   'EXIT': {1:'Bye! {}', 2:'Have a good day! {}', 3:'Enjoy your rest of the day! {}'}
                  }

# Regex library used to fetch information from user responses based on state.
STATE_I_LIBRARY = {'GREET': (r'([Aa][Mm]\s*(.+))$', r'([IS|is]\s*(.+))$'),
                  }

# Converstion state transition table based on the ability of machine to fetch info from user responses.
STATE_TRANSITION_TABLE = {('GREET', 'CONFUSED'):'GREET', ('GREET', 'EXIT'):'EXIT', ('GREET', 'INFO'):'S1'}

class Machine(object):
    ''' Bot Machine which traverses through the conversations states and uses necessary state infromation 
    to process and respond to the user.
    '''

    def __init__(self, agent_name, current_state):
        self.current_state = current_state
        self.__low = 1
        self.__high = 2
        self.machine_name = agent_name
        self.user_name = None
    
    def ask_question(self, current_state, info=None):
        question = STATE_Q_LIBRARY.get(current_state).get(randint(self.__low, self.__high))
        if info:
            return question.format(info)
        return question
        
    def get_response(self):
       string = input()
       return string.strip()

    def process_response(self, current_state, input_string):
       responses = list({re.search(regex, input_string) for regex in STATE_I_LIBRARY.get(current_state)})
       return responses[0].groups()[1]

    def classify(self, response):
        if response is None:
            return ('CONFUSED', response)
        elif any(x in response.upper() for x in ['BYE', 'EXIT', 'QUIT', 'GOOD NIGHT']):
            return ('EXIT', response)
        else:
            return ('INFO', response)

    def get_next_state(self, current_state, trigger):
        return STATE_TRANSITION_TABLE.get((current_state, trigger))

    def run(self):
        " Run methodology where the machine computes and makes state jumps using state information and response classification"
        input_string = None
        while(True):
            if self.current_state == 'GREET':
                print(self.ask_question(self.current_state, self.machine_name))
                input_string = self.get_response()
                response = self.process_response(self.current_state, input_string)
                trigger, response = self.classify(response)
                if trigger == 'INFO':
                    self.user_name = response
                self.current_state = self.get_next_state(self.current_state, trigger)
                continue
            elif self.current_state == 'EXIT':
                print(self.ask_question(self.current_state, self.user_name))
                break
            print(self.user_name)
            break

if __name__ == '__main__':
    current_state = 'GREET'
    agent_name = 'Orange'
    orange_bot = Machine(agent_name, current_state)
    orange_bot.run()
