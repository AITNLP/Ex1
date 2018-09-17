import re
import random

Chat=input("Hi, May I have you name please\n")
re_name=re.findall(r'\b[A-Z]{1}[a-z]+.?$',Chat)
print("Hi {}, how can I help you today?\n".format(" ".join(re_name).replace(".","")))

response={'I need':["why do you need","Are you sure you need"],
          'I would':["could you explain why you would","why would you"],
          'crave':["Why don't you tell me more about your cravings"],
          'I want':["What would it mean to you if you got", "Why do you want","What would you do if you got"],
          'what':["Why do you ask","How would an answer to that help you","What do you think"],}

translate={"am":"are",
           "was":"were",
           "I":"you",
           "I would":"you would",
           "I have":"you have",
           "I will":"you will",
           "are":"am",
           "your":"my",
           "yours":"mine",
           "you":"me",
           "me":"you",
           "my":"your"}
Chat=input("Hi, May I have you name please\n")
re_name=re.findall(r'\b[A-Z]{1}[a-z]+.?$',Chat)
print("Hi {}, how can I help you today?\n".format(" ".join(re_name).replace(".","")))

while not re.findall(r'([Bb]ye)$|([Ee]xit)$',Chat):
    Chat=input()
    if re.findall(r'I need (.*)',Chat):
        for k,ask in response.items():
            if 'I need' not in k:
                continue
            else:
                tran_key=translate.keys()
                ahead=Chat.split(r"need",1)[1]
                newstring=ahead.split()
                for i in range(0,len(newstring)):
                    if newstring[i] in tran_key:
                        newstring[i]=translate[newstring[i]]
                print("".join(re_name)+", "+random.choice(ask)+' {}?'.format(" ".join(newstring)))

    elif re.findall(r'I want (.*)',Chat):
        for k,ask in response.items():
            continue
        else:
            tran_key=translate.keys()
            ahead=Chat.split(r"want",1)[1]
            newstring=ahead.split()
            for i in range(0,len(newstring)):
                if newstring[i] in tran_key:
                    newstring[i]=translate[newstring[i]]
            print("".join(re_name)+", "+random.choice(ask)+' {}?'.format(" ".join(newstring)))

    else:
        pass
print("bye and keep in touch")

