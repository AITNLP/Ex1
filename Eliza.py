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
                   'EXIT': {1: '[{0}] Bye! {1}', 2: '[{0}] Have a good day! {1}', 3: '[{0}] Enjoy your rest of the day! {1}'}
                  }

# Regex library used to fetch information from user responses based on state.
STATE_I_LIBRARY = {'GREET': (r'([Aa][Mm]\s*(.+))$', r'([IS|is]\s*(.+))$'),
                  }

            
# Converstion state transition table based on the ability of machine to fetch info from user responses.
STATE_TRANSITION_TABLE = {('GREET', 'CONFUSED'):'GREET', ('GREET', 'EXIT'):'EXIT', ('GREET', 'INFO'): 'HELP',
                          ('HELP', 'CONFUSED'): 'HELP', ('HELP', 'EXIT'): 'EXIT', ('HELP', 'INFO'): 'DECIDE_STATE',
                          ('WANT', 'CONFUSED'): 'WANT', ('WANT', 'EXIT'): 'EXIT', ('WANT', 'INFO'): 'DECIDE_STATE',
                          ('FEEL', 'CONFUSED'): 'FEEL', ('FEEL', 'EXIT'): 'EXIT', ('FEEL', 'INFO'): 'DECIDE_STATE',
                          ('HAVE', 'CONFUSED'): 'HAVE', ('HAVE', 'EXIT'): 'EXIT', ('HAVE', 'INFO'): 'DECIDE_STATE'
                         }

class Machine(object):
    ''' Bot Machine which traverses through the conversations states and uses necessary state infromation 
    to process and respond to the user.
    '''

    def __init__(self, agent_name, current_state):
        self.current_state = current_state
        self.previous_state = None
        self.__low = 1
        self.__high = 3
        self.machine_name = agent_name
        self.user_name = None
    
    def ask_question(self, current_state, args):
        question = STATE_Q_LIBRARY.get(current_state).get(randint(self.__low, self.__high))
        return question.format(*args)

    @staticmethod
    def get_response():
       string = input()
       return string.strip()
    
    @staticmethod
    def classify(response):
        if response is None:
            return 'CONFUSED'
        elif any(x in response.upper() for x in ['BYE', 'EXIT', 'QUIT', 'GOOD NIGHT']):
            return 'EXIT'
        else:
            return 'INFO'

    def decide_state(self, previous_state, input_string):
        response = None
        for state, regexes in STATE_I_LIBRARY:
                responses = list({re.search(regex, input_string).groups(0)[1] for regex in regexes})
                response = responses[0] if len(responses) == 1: else responses[randint(0,len(responses)-1)]
            _class = classify(response)
            next_state = STATE_TRANSITION_TABLE.get(current_state, _class)
                return (next_state, response)

        return (next_state, response)

    def run(self):
        " Run methodology where the machine computes and makes state jumps using state information and response classification"
        input_string = None
        while(True):
            if self.current_state == 'GREET':
                print(self.ask_question(self.current_state, [self.machine_name]))
                input_string = self.get_response()
                responses = list({re.search(regex, input_string).groups(0)[1] for regex in regexes})
                response = responses[0] if len(responses) == 1: else responses[randint(0, len(responses)-1)]
                _class = self.classify(response)
                next_state = STATE_TRANSITION_TABLE.get(current_state, _class)
                if next_state == 'HELP':
                    self.user_name = response
                self.previous_state = self.current_state
                self.current_state = next_state
                continue
                
            elif self.current_state == 'HELP':
                print(self.ask_question(self.current_state, [self.machine_name, self.user_name]))
                input_string = self.get_response()
                next_state, response = thinking_state(self.current_state, input_string)
                
                self.previous_state = self.current_state
                self.current_state = next_state
                continue
            elif self.current_state == 'WANT':
                print(self.ask_question(self.current_state, [self.machine_name]))
                self.previous_state = self.current_state
                self.current_state = next_state
                continue
            elif self.current_state == 'FEEL':

                self.previous_state = self.current_state
                self.current_state = next_state
                continue
            elif self.current_state == 'HAVE':
                self.previous_state = self.current_state
                self.current_state = next_state
                continue
            elif self.current_state == 'DID':
                self.previous_state = self.current_state
                self.current_state = next_state
                continue
            elif self.current_state == 'CONFUSED':
                self.current_state = self.previous_state
                continue
            elif self.current_state == 'EXIT':
                print(self.ask_question(self.current_state, [self.machine_name, self.user_name]))
                break
            elif self.current_state == 'DECIDE_STATE':
                self.current_state =
                continue


if __name__ == '__main__':
    current_state = 'GREET'
    agent_name = 'Eliza'
    orange_bot = Machine(agent_name, current_state)
    orange_bot.run()
