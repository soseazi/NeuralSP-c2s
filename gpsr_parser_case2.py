
from lark import Lark
from lark.lexer import Token

# Convert to lower case, appostrophy
# common_guide : guided person will deviate before reaching
# common_follow - follow 3,4 : destination room may not be specified

# find OBJ? get OBJ?

# conflict list
# tell me what's the heaviest snacks on the fireplace : i didn't assign fndobj
# bring the banana from the dining room to the cabinet : used VTAKE iso VBTAKE

class GPSR_parser_case2():
    def __init__(self, max_iter = 1, debug = False):
        grammar = """
            sentence: manipulation | fndppl | fndobj | common_manipulation | common_fndppl | common_fndobj | common_guide | common_follow

            manipulation: manipulation1 | manipulation2 | manipulation3 | manipulation4 | manipulation5
            fndppl: fndppl1 | fndppl2 | fndppl3 | fndppl4 | fndppl5 | fndppl6 | fndppl7 | fndppl8
            fndobj: fndobj1 | fndobj2 | fndobj3 | fndobj4

            common_manipulation: common_manipulation1 | common_manipulation2 | common_manipulation3 | common_manipulation4 | common_manipulation5 | common_manipulation6 | common_manipulation7 | common_manipulation8
            common_fndppl: common_fndppl1 | common_fndppl2 | common_fndppl3 | common_fndppl4 | common_fndppl5 | common_fndppl6
            common_fndobj: common_fndobj1 | common_fndobj2

            common_manipulation1: take DET DET PLC2
            common_manipulation2: VPLACE DET OBJ DET DET PLC2
            common_manipulation3: VBRING OP DET OBJ
            common_manipulation4: VDEL DET OBJ DET someone
            common_manipulation5: takefrom DET DET PLC2
            common_manipulation6: goplace VFIND DET OBJ AND delivme
            common_manipulation7: goplace VFIND DET OBJ AND delivat
            common_manipulation8: goplace VFIND DET OBJ AND place

            manipulation1: VBTAKE DET AOBJ DET DET ROOM DET DET PLC2
            manipulation2: VBRING OP DET AOBJ DET DET PLC
            manipulation3: takefrom AND delivme
            manipulation4: takefrom AND delivat
            manipulation5: takefrom AND place

            common_fndppl1: answer DET whowhere
            common_fndppl2: speak DET whowhere
            common_fndppl3: findp DET DET ROOM AND answer
            common_fndppl4: findp DET DET ROOM AND speak
            common_fndppl5: goroom findp AND answer
            common_fndppl6: goroom findp AND speak

            fndppl1: VTTELL OP DET TNAME DET DET TPERSON DET DET BEC
            fndppl2: VTTELL OP DET TGENDER DET DET TPERSON DET DET BEC
            fndppl3: VTTELL OP DET TPOSE DET DET TPERSON DET DET BEC
            fndppl4: VTTELL OP DET TNAME DET DET TPERSON DET DET ROOM
            fndppl5: VTTELL OP DET TGENDER DET DET TPERSON DET DET ROOM
            fndppl6: VTTELL OP DET TPOSE DET DET TPERSON DET DET ROOM
            fndppl7: VTTELL OP THOWMANY TPEOPLE DET DET ROOM BE PGENDERP
            fndppl8: VTTELL OP THOWMANY TPEOPLE DET DET ROOM BE POSE

            common_fndobj1: VTTELL OP THOWMANY OBJ ADV BE DET DET PLC
            common_fndobj2: VFIND DET OBJ DET DET ROOM

            fndobj1: VFIND DET CAT DET DET ROOM
            fndobj2: VTTELL OP THOWMANY CAT ADV BE DET DET PLC
            fndobj3: VTTELL OP TWHATS DET OPROP TOBJECT DET DET PLC
            fndobj4: VTTELL OP TWHATS DET OPROP CAT DET DET PLC

            common_guide: gdcmd1 | gdcmd2 | gdcmd3 | gdcmd4
            gdcmd1: VGUIDE NAME1 DET DET BEC1 DET DET BEC2
            gdcmd2: VTMEET NAME1 DET DET BEC1 AND guideto
            gdcmd3: gobeacon VTMEET NAME1 AND guideto
            gdcmd4: VGUIDE NAME1 DET DET BEC2 gdwhere

            guideto: VGUIDE PRONOUN DET DET BEC2
            gobeacon: VGOPL DET DET BEC1
            gdwhere: TYOU MODAL VTFIND PRONOUN DET DET BEC1

            common_follow: follow1 | follow2 | follow3 | follow4
            follow1: VFOLLOW NAME1 DET DET BEC1 DET DET ROOM2
            follow2: VTMEET NAME1 DET DET BEC1 AND VFOLLOW PRONOUN fllwdest
            follow3: VTMEET NAME1 DET DET BEC1 AND VFOLLOW PRONOUN
            follow4: gobeacon VTMEET NAME1 AND VFOLLOW PRONOUN

            fllwdest: DET DET ROOM2


            whowhere: DET TPERSON GESTURE DET DET ROOM
            someone: OP | whowhere

            takefrom: VTAKE DET OBJ DET DET PLC1
            delivme: VDEL PRONOUN DET OP
            delivat: VDEL PRONOUN DET NAME DET DET BEC
            place: VPLACE PRONOUN DET DET PLC2
            goplace: VGOPL DET DET PLC1
            talk: answer | speak
            answer: TANSWER DET TQUESTION
            speak: VSPEAK whattosay
            findp: VFIND DET PGENDERS | VFIND DET TPERSON GESTURE | VFIND DET TPERSON POSE
            goroom: VGOPL DET DET ROOM1
            whattosay: WHATTOSAY1 | WHATTOSAY2 | WHATTOSAY3 | WHATTOSAY4 | WHATTOSAY5 | WHATTOSAY6 | WHATTOSAY7 | WHATTOSAY8 | WHATTOSAY9 | WHATTOSAY0
            take: VTAKE DET OBJ


            PLC1: PLC
            PLC2: PLC1
            BEC1: BEC
            BEC2: BEC1
            ROOM1: ROOM
            ROOM2: ROOM1



            OBJ: KOBJ | AOBJ
            AOBJ: OBJ_FRU
            KOBJ: OBJ_CLN | OBJ_SNK | OBJ_FRU | OBJ_FOD| OBJ_DRI | OBJ_CUT | OBJ_TAB | OBJ_CON

            CAT: "cleaning stuff" | "snacks" | "fruits" | "food" | "drinks" | "cutlery" | "tableware" | "containers"

            OBJ_CLN: "scrubby" | "sponge"
            OBJ_SNK: "pringles" | "crackers" | "potato chips"
            OBJ_FRU: "apple" | "orange" | "paprika"
            OBJ_FOD: "cereal" | "noodles" | "sausages"
            OBJ_DRI: "chocolate drink" | "coke" | "orange juice" | "grape juice" | "sprite"
            OBJ_CUT: "-"
            OBJ_TAB: "dish" | "bowl" | "glass"
            OBJ_CON: "bag"

            ROOM: "bedroom" | "dining room" | "living room" | "kitchen"
                | "corridor"

            PLC: PLC_BED | PLC_DIN | PLC_LIV
                | PLC_KIT | PLC_COR

            BEC: BEC_BED | BEC_DIN | BEC_LIV
                | BEC_KIT | BEC_COR

            BEC_BED: "bed" | "desk"
            PLC_BED: "side table" | "desk"

            BEC_DIN: "dining table"
            PLC_DIN: "dining table"

            BEC_LIV: "exit" | "couch" | "end table" | "bookcase"
            PLC_LIV:  "end table" | "bookcase"

            BEC_KIT: "sink" | "dishwasher"
            PLC_KIT: "cupboard" | "counter" | "storage table" | "sink"

            BEC_COR: "entrance"
            PLC_COR: "entrance"

            NAME1: NAME
            NAME2: NAME1
            NAME: "alex" | "charlie" | "elizabeth" | "francis" | "jennifer"
                | "linda" | "mary" | "patricia" | "robin" | "skyler" | "james" | "john"
                | "michael" | "robert" | "william"



            VBTAKE: "bring" | "take"
            VPLACE: "place" | "put"
            VBRING: "bring" | "give"
            VDEL: VBRING | "deliver"
            VTAKE: "get" | "grasp" | "take" | "pick up"
            VSPEAK: "tell" | "say"
            VGOPL: "go" | "navigate"
            VGOR: VGOPL | "enter"
            VFIND: "find" | "locate" | "look for"
            VGUIDE: "guide" | "escort" | "take" | "lead" | "accompany"
            VFOLLOW: "follow" | "go after" | "come after"

            VTTELL: "tell"
            VTMEET: "meet"
            VTFIND: "find"

            TNAME: "name"
            TPERSON: "person"
            TSOMEONE: "someone"
            TANSWER: "answer"
            THOWMANY: "how many"
            TQUESTION: "question"
            TGENDER: "gender"
            TPOSE: "pose"
            TPEOPLE: "people"
            TWHATS: "whats"
            TYOU: "you"
            TOBJECT: "object"

            PGENDERS: "man" | "woman" | "boy" | "girl" | "male person" | "female person"
            PGENDERP: "men" | "women" | "boys" | "girls" | "male" | "female"
            POSE: "sitting" | "standing" | "lying down"
            GESTURE: "waving" | "raising their left arm" | "raising their right arm" | "pointing to the left" | "pointing to the right"
            OPROP: "biggest" | "largest" | "smallest" | "heaviest" | "lightest" | "thinnest"

            ADV: "there"
            BE: "are" | "is"
            DET: "the" | "from" | "on" | "to" | "at" | "of" | "in" | "a"
            AND: "and"
            PRONOUN: "it" | "him" | "her"
            MODAL: "may" | "can" | "will"
            OP: "me"

            WHATTOSAY1: "something about yourself"
            WHATTOSAY2: "the time"
            WHATTOSAY3: "what day is today"
            WHATTOSAY4: "what day is tomorrow"
            WHATTOSAY5: "your teams name"
            WHATTOSAY6: "your teams country"
            WHATTOSAY7: "your teams affiliation"
            WHATTOSAY8: "the day of the week"
            WHATTOSAY9: "the day of the month"
            WHATTOSAY0: "a joke"

            %import common.WS
            %ignore WS
        """

        self.parser = Lark(grammar, start='sentence', ambiguity='explicit')

        self.term_dic={
            'OBJ': 'soap',
            'KOBJ': 'pasta',
            'AOBJ': 'apple',
            'CAT': 'fruits',
            'PLC': 'desk',
            'PLC1': 'sofa',
            'PLC2': 'bar',
            'BEC': 'shower',
            'BEC1': 'sink',
            'BEC2': 'chair',
            'ROOM': 'bedroom',
            'ROOM1': 'living room',
            'ROOM2': 'bathroom',
            'NAME1': 'alex',
            'NAME': 'michael',

            'VBTAKE': "bring",
            'VPLACE': "place",
            'VBRING': "give",
            'VDEL': "deliver",
            'VTAKE': "take",
            'VSPEAK': "tell",
            'VGOPL': "go",
            "VGOR": "enter",
            "VFIND": "find",
            "VGUIDE": "guide",
            "VFOLLOW": "follow",
            "VTTELL": "tell",
            "VTMEET": "meet",
            "VTFIND": "find",

            'TNAME': "name",
            'TPERSON': "person",
            'TSOMEONE': "someone",
            'TANSWER': "answer",
            'THOWMANY': "how many",
            'TQUESTION': "question",
            'TGENDER': "gender",
            'TPOSE': "pose",
            'TPEOPLE': "people",
            'TWHATS': "whats",
            'TYOU': "you",
            'TOBJECT': "object",

            'PGENDERS': "man" ,
            'PGENDERP': "men" ,
            'POSE': "sitting" ,
            'GESTURE': "waving",
            'OPROP': "biggest",


            'ADV': "there",
            'BE': "is",
            'DET': "the",
            'AND': "and",
            'PRONOUN': "it",
            'MODAL': "may" ,
            'OP': "me",


            'WHATTOSAY1': "something about yourself",
            'WHATTOSAY2': "the time",
            'WHATTOSAY3': "what day is today",
            'WHATTOSAY4': "what day is tomorrow",
            'WHATTOSAY5': "your teams name",
            'WHATTOSAY6': "your teams country",
            'WHATTOSAY7': "your teams affiliation",
            'WHATTOSAY8': "the day of the week",
            'WHATTOSAY9': "the day of the month",
            'WHATTOSAY0': "a joke"
        }

        self.max_iter = max_iter
        self.debug = debug

    def getTerminals(self, subtree):
        terminals = {}
        if isinstance(subtree, Token):
            terminals[subtree.type] = subtree.value
        else:
            for subsubtree in subtree.children:
                subterminals = self.getTerminals(subsubtree)
                for t in subterminals:
                    terminals[t] = subterminals[t]
        return terminals

    def find_predefined_idx(self, dic):
        idx = None
        for k in dic:
            if k.startswith('PREDEF'):
                idx = k.replace('PREDEF','')
            elif k.startswith('WHATTOSAY'):
                idx = k.replace('WHATTOSAY','')
        #print(idx)
        return idx

    def search(self, dic, key):
        for k in dic:
            if k == key: return True
        return False

    def tree2plan(self, tree):
        plan = []

        question_type = tree.children[0].children[0].data
        #print('question type : ' + question_type)
        #print('')
        terminals = self.getTerminals(tree)
        #print(terminals)
        #print('')

        if question_type == 'common_manipulation1':
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['PLC2']])
            plan.append(['put', ''])

        elif question_type == 'common_manipulation2':
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['PLC2']])
            plan.append(['put', ''])

        elif question_type == 'common_manipulation3':
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', 'operator'])
            plan.append(['give', ''])

        elif question_type == 'common_manipulation4':
            plan.append(['get', terminals['OBJ']])
            if self.search(terminals, 'OP'):
                plan.append(['go','operator'])
            else:
                plan.append(['go', terminals['ROOM']])
                plan.append(['find', terminals['GESTURE']])
            plan.append(['give', ''])

        elif question_type == 'common_manipulation5':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['PLC2']])
            plan.append(['put', ])

        elif question_type == 'common_manipulation6':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', 'opertor'])
            plan.append(['give', ''])

        elif question_type == 'common_manipulation7':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['BEC']])
            plan.append(['find', terminals['NAME']])
            plan.append(['give', ''])

        elif question_type == 'common_manipulation8':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['PLC2']])
            plan.append(['put', ''])

        elif question_type == 'common_fndppl1':
            plan.append(['go', terminals['ROOM']])
            plan.append(['find', terminals['GESTURE']])
            plan.append(['answer', 'predefined'])

        elif question_type == 'common_fndppl2':
            plan.append(['go',terminals['ROOM']])
            plan.append(['find',terminals['GESTURE']])
            plan.append(['answer',terminals['WHATTOSAY'+self.find_predefined_idx(terminals)]])

        elif question_type == 'common_fndppl3':
            plan.append(['go', terminals['ROOM']])
            if self.search(terminals, 'PGENDERS'):
                plan.append(['find', terminals['PGENDERS']])
            elif self.search(terminals, 'GESTURE'):
                plan.append(['find', terminals['GESTURE']])
            else:
                plan.append(['find', terminals['POSE']])
            plan.append(['answer', 'predefined'])

        elif question_type == 'common_fndppl4':
            plan.append(['go',terminals['ROOM']])
            if self.search(terminals, 'PGENDERS'):
                plan.append(['find', terminals['PGENDERS']])
            elif self.search(terminals, 'GESTURE'):
                plan.append(['find', terminals['GESTURE']])
            else:
                plan.append(['find', terminals['POSE']])
            plan.append(['answer',terminals['WHATTOSAY'+self.find_predefined_idx(terminals)]])

        elif question_type == 'common_fndppl5':
            plan.append(['go', terminals['ROOM1']])
            if self.search(terminals, 'PGENDERS'):
                plan.append(['find', terminals['PGENDERS']])
            elif self.search(terminals, 'GESTURE'):
                plan.append(['find', terminals['GESTURE']])
            else:
                plan.append(['find', terminals['POSE']])
            plan.append(['answer', 'predefined'])

        elif question_type == 'common_fndppl6':
            plan.append(['go',terminals['ROOM1']])
            if self.search(terminals, 'PGENDERS'):
                plan.append(['find', terminals['PGENDERS']])
            elif self.search(terminals, 'GESTURE'):
                plan.append(['find', terminals['GESTURE']])
            else:
                plan.append(['find', terminals['POSE']])
            plan.append(['answer',terminals['WHATTOSAY'+self.find_predefined_idx(terminals)]])

        elif question_type == 'common_fndobj1':
            plan.append(['go', terminals['PLC']])
            plan.append(['count', terminals['OBJ']])
            plan.append(['go', 'operator'])
            plan.append(['tell', 'count'])

        elif question_type == 'common_fndobj2':
            plan.append(['go', terminals['ROOM']])
            plan.append(['find', terminals['OBJ']])

        elif question_type == 'manipulation1':
            plan.append(['go', terminals['ROOM']])
            plan.append(['get', terminals['AOBJ']])
            plan.append(['go', terminals['PLC2']])
            plan.append(['put', ''])

        elif question_type == 'manipulation2':
            plan.append(['go', terminals['PLC']])
            plan.append(['get', terminals['AOBJ']])
            plan.append(['go', 'operator'])
            plan.append(['give', ''])

        elif question_type == 'manipulation3':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', 'operator'])
            plan.append(['give', '' ])

        elif question_type == 'manipulation4':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['BEC']])
            plan.append(['find', terminals['NAME']])
            plan.append(['give', '' ])

        elif question_type == 'manipulation5':
            plan.append(['go', terminals['PLC1']])
            plan.append(['get', terminals['OBJ']])
            plan.append(['go', terminals['PLC2']])
            plan.append(['put', '' ])

        elif question_type in ['fndppl1', 'fndppl2', 'fndppl3', 'fndppl4', 'fndppl5', 'fndppl6']:
            idx = int(question_type[6])
            if idx <= 3:
                plan.append(['go', terminals['BEC']])
            else:
                plan.append(['go', terminals['ROOM']])
            if idx%3 == 1:
                plan.append(['ask', 'name'])
                plan.append(['go', 'operator'])
                plan.append(['tell', 'name'])
            elif idx%3 == 2:
                plan.append(['see', 'gender'])
                plan.append(['go', 'operator'])
                plan.append(['tell', 'gender'])
            else:
                plan.append(['see', 'pose'])
                plan.append(['go', 'operator'])
                plan.append(['tell', 'pose'])

        elif question_type in ['fndppl7', 'fndppl8']:
            idx = int(question_type[6])
            plan.append(['go', terminals['ROOM']])
            if idx == 7:
                plan.append(['count',terminals['PGENDERP']])
            else:
                plan.append(['count',terminals['POSE']])
            plan.append(['go','operator'])
            plan.append(['tell','count'])

        elif question_type == 'fndobj1':
            plan.append(['go' , terminals['ROOM']])
            plan.append(['find' ,terminals['CAT']])

        elif question_type == 'fndobj2':
            plan.append(['go' , terminals['PLC']])
            plan.append(['count' ,terminals['CAT']])
            plan.append(['go','operator'])
            plan.append(['tell','count'])

        elif question_type in ['fndobj3', 'fndobj4']:
            idx = int(question_type[6])
            plan.append(['go' , terminals['PLC']])
            if idx == 3:
                plan.append(['find', 'object',terminals['OPROP'] ])
            else:
                plan.append(['find', terminals['CAT'], terminals['OPROP'] ])
            plan.append(['go','operator'])
            plan.append(['tell','object'])

        elif question_type in ['gdcmd1', 'gdcmd2', 'gdcmd3', 'gdcmd4']:
            plan.append(['go' , terminals['BEC1']])
            plan.append(['find' , terminals['NAME1']])
            plan.append(['guide' , terminals['BEC2']])

        elif question_type in ['follow1', 'follow2', 'follow3', 'follow4']:
            idx = int(question_type[6])
            plan.append(['go' , terminals['BEC1']])
            plan.append(['find' , terminals['NAME1']])
            if idx <= 2:
                plan.append(['follow' , terminals['ROOM2']])
            else:
                plan.append(['follow' , ''])

        return plan

    def handle_error(self, sentence, error):
        # replace errored word with all possible alternatives and return recoverd sentences
        # recovered = list of ['sentence', 'expected type']
        # alternative = list of 'alternative'
        error_part = error.context.strip(' ').split(' ')[0]
        c = error.column
        while sentence[c] is not ' ' and c > 0:
            c -= 1

        before_ = sentence[:c]
        after_  = sentence[c:]
        error_part = after_.split()[0]
        after_deleted = after_.replace(error_part, '',1)
        deleted = before_ + after_deleted
        ##print(deleted)
        recovered = [[sentence, None], [deleted, None]]
        alternative = ['', '']

        for expect in list(error.allowed):
            if self.search(self.term_dic, expect):
                alternative.append(self.term_dic[expect])
                recovered.append([sentence, expect])
                alternative.append(self.term_dic[expect] + ' ' + error_part)
                recovered.append([sentence, expect])

        for i in range(2,len(recovered)):
            recovered[i][0] = before_ + after_.replace(error_part, alternative[i],1)

        ##print(recovered)
        return recovered, alternative, before_, after_deleted
    def get_plan(self, sentence):
        if len(sentence.split()) < 3:
            return False, None
        sentence = sentence.lower().replace("\'","").replace("\"","").replace(",","").replace(".","").strip(" ")
        try: # successful parsing
            parse_tree = self.parser.parse(sentence)
            #print(parse_tree.pretty())
            plan_ = self.tree2plan(parse_tree)
            return True, plan_
        except Exception as e:
            if self.debug:
                print(e)
            if 'end of input' in str(e):
                return False, None
            ##print(e)
            recovered_return = []
            recovered, alternative, before, after = self.handle_error(sentence, e)
            for r in recovered:
                if r[1] not in ['OBJ','KOBJ','AOBJ','CAT', 'PLC', 'PLC1', 'PLC2',
                            'BEC','BEC1','BEC2','ROOM', 'ROOM1','ROOM2', 'NAME']:
                    recovered_return.append(r)
            return False, recovered_return
        return False, None

    def parse(self, sentence, iter = 0):
        if iter is self.max_iter:
            return None
        #print('iter : {}, parse : {}'.format(iter,sentence))
        ##print('parse iteration ' + str(iter))
        plans = []
        try:
            ret, val = self.get_plan(sentence)
        except:
            return None
        if ret == True:
            if iter == 0:
                return val
            else:
                plans.append(val)
                return plans
        else:
            if val == None:
                return None
            recovered = val
            for r in recovered:
                planret = self.parse(r[0], iter + 1)
                if planret is not None:
                    for p in planret:
                        plans.append(p)
            if iter == 0:
                if len(plans) > 0 and plans.count(plans[0]) == len(plans):
                    return plans[0]
                else:
                    return None
            return plans


if __name__ == '__main__':
    parser = GPSR_parser_case2(max_iter = 3, debug = True)
    while True:
        sentence = input("\nInput sentence : ")
        plan = parser.parse(sentence)
        #print('final plan : ')
        if parser.debug:
            print(plan)
