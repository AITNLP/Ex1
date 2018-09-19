import re
STATE_I_LIBRARY = {'GREET': r'(AM | am | is | IS)\s*(?P<response>[a-zA-Z0-9]+).*$',
                   'WANT': r'(need| want |crave| NEED | WANT | CRAVE)\s+(?P<response>.*).*$',
                   'FEEL': r'(feel | FEEL | Feel | feel)(ings|ing)?\s+(?P<response>.*).*$',
                   'HAVE': r'(have | had | HAVE | HAD)(?P<response>.*).*$',
                   'DID': r'(think | taught | mind)\s+(?P<response>.*).*$'
                  }

def run_all_regex(input_string):
        ''' Regex runner for all states.'''
        response = None
        results = {}
        for state, regex in STATE_I_LIBRARY.items():
            re_obj = re.search(regex, input_string)
            try:
                    response = re_obj.group('response')
            except:
                    continue
            print(response)
            results[state] = (response, 'INFO')
        print(results)
        return results

run_all_regex('I am Ram.')
run_all_regex('This is Ram.')
run_all_regex('I need Car stand.')
run_all_regex('I feel headache.')
run_all_regex('I HAVE lunch.')
run_all_regex('I had lunch.')


