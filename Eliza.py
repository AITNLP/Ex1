'''
@ Description:
@ Author: Sri Ram Sagar Kappagantula,
          Harsimrat Kaur and
          Ritika De.
@ Date: September 17, 2018
'''
import re
import logging
from random import randint

# Questions library based on state.
STATE_Q_LIBRARY = {'GREET': {1:'[{0}] Hi! I am {0}!', 2:'[{0}] Hello! This is {0}!', 3:'[{0}] I am {0}, and you are?'},
				   'HELP':{1:'[{0}]How can I help you today,{1}?',2:'[{0}] How are you doing today,{1}?'3:'[{0}]Is there anything I can help you with today,{1}?'},
                   'WANT': {1:'[{0}]Why do you think you want {1}?',2:'[{0}]Do you really need {1}?',3:'[{0}]How will you feel if you get{1}?'},
                   'FEEL': {1:'[{0}]What made you feel {1}',2:'[{0}]Do you enjoy feeling {1}',3:'[{0}]For how long have you been feeling {1}'},
                   'HAVE': {1:'[{0}] Do you feel happy having {1}?',2:'[{0}]How will you feel if you lost your {1}?',3:'[{0}] will you like sharing your {1}?'},
				   'DID':{1:'[{0}] Does it please you doing {1}?',2:'[{0}]Can you elaborate your process for doing {1}.',3:'[{0}] what made you do{1}?'},
                   'CONFUSED': {1:'[{0}] Hmmm! Can you elaborate {1}.', 2:'[{0}] Tell me more! {1}', 3:'[{0}] I did not understand what you said. {1}!'},
                   'EXIT': {1: '[{0}] Bye! {0}', 2: '[{0}] Have a good day! {0}', 3: '[{0}] Enjoy your rest of the day! {0}'}
                  }

# Regex library used to fetch information from user responses based on state.
STATE_I_LIBRARY = {'GREET': (r'([Aa][Mm]\s*(.+))$', r'([IS|is]\s*(.+))$'),
                  }

def thinking_state():
    pass

# Converstion state transition table based on the ability of machine to fetch info from user responses.
STATE_TRANSITION_TABLE = {('GREET', 'CONFUSED'):'GREET', ('GREET', 'EXIT'):'EXIT', ('GREET', 'INFO'): thinking_state,
                          ('WANT', 'CONFUSED'): 'WANT', ('WANT', 'EXIT'): 'EXIT', ('WANT', 'INFO'): thinking_state,
                          ('FEEL', 'CONFUSED'): 'FEEL', ('FEEL', 'EXIT'): 'EXIT', ('FEEL', 'INFO'): thinking_state,
                          ('HAVE', 'CONFUSED'): 'HAVE', ('HAVE', 'EXIT'): 'EXIT', ('HAVE', 'INFO'): thinking_state
                         }
                

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
            elif self.current_state == 'WANT':
                continue
            elif self.current_state == 'FEEL':
                continue
            elif self.current_state == 'HAVE':
                continue
            elif self.current_state == 'DID':
                continue
            elif self.current_state == 'CONFUSED':
                continue
            elif self.current_state == 'EXIT':
                print(self.ask_question(self.current_state, self.user_name))
                break

if __name__ == '__main__':
    current_state = 'GREET'
    agent_name = 'Eliza'
    orange_bot = Machine(agent_name, current_state)
    orange_bot.run()
