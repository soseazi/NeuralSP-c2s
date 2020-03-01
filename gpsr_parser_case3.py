
from lark import Lark
from lark.lexer import Token

# Convert to lower case, appostrophy
# common_guide : guided person will deviate before reaching
# common_follow - follow 3,4 : destination room may not be specified

# find OBJ? get OBJ?

# conflict list
# tell me what's the heaviest snacks on the fireplace : i didn't assign fndobj
# bring the banana from the dining room to the cabinet : used VTAKE iso VBTAKE

class GPSR_parser_case3():
    def __init__(self, max_iter = 1, debug = False):
        grammar = """
            sentence: polite? (fndobj | incomplete | erroneous | followout)

            polite: "please" | "could you" | "could you please" | "robot please"

            fndobj: common_fndobj1 | common_fndobj2 | fndobj1 | fndobj2
            followout: followout1 | followout2
            incomplete: incomplete1 | incomplete2 | incomplete3 | incomplete4 | incomplete5
            erroneous: erroneous1 | erroneous3 | erroneous4 | erroneous5 | erroneous6

            common_fndobj1: VTTELL OP THOWMANY OBJ ADV BE DET DET PLC
            common_fndobj2: VFIND DET OBJ DET DET ROOM

            fndobj1: VTTELL OP TWHICH BE DET NUM OPROP (TOBJECT | CAT) DET DET PLC1
            fndobj2: VFIND NUM CAT DET DET ROOM

            followout1: VTMEET NAME1 DET DET BEC1 VFOLLOW PRONOUN AND goroom
            followout2: VTMEET NAME1 DET DET BEC1 VFOLLOW PRONOUN AND VGUIDE PRONOUN TBACK

            incomplete1: VFOLLOW NAME1
            incomplete2: VDEL CAT DET someone
            incomplete3: VGUIDE NAME1 DET DET BEC2
            incomplete4: VTMEET inguidewho AND VGUIDE PRONOUN
            incomplete5: gobeacon VTMEET inguidewho AND VGUIDE PRONOUN

            inguidewho: NAME1

            erroneous1: VGUIDE NAME1 DET DET BEC1 DET DET BEC2

            erroneous3: VGUIDE DET ernamperobj DET DET BEC1 DET DET BEC2
            erroneous4: gobeacon VTMEET NAME1 AND VFOLLOW PRONOUN DET DET BEC1
            erroneous5: gobeacon VTMEET errnoper AND VFOLLOW PRONOUN DET DET ROOM2
            erroneous6: gobeacon VTMEET DET ernamperobj AND VFOLLOW PRONOUN

            errnoobj: OBJ1
            errnoper: NAME1
            ernamperobj: OBJ1 | CAT1

            guideto: VGUIDE PRONOUN DET DET BEC2
            gobeacon: VGOPL DET DET BEC1
            gdwhere: TYOU MODAL VTFIND PRONOUN DET DET BEC1

            fllwdest: DET DET ROOM2

            whowhere: NAME1 | DET GESTURE TPERSON DET DET ROOM
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
            OBJ1: OBJ
            OBJ2: OBJ1
            CAT1: CAT
            CAT2: CAT1



            OBJ: KOBJ
            AOBJ: OBJ_FRU
            KOBJ: OBJ_CLN | OBJ_SNK | OBJ_FRU | OBJ_FOD| OBJ_DRI | OBJ_CUT | OBJ_TAB | OBJ_CON

            CAT: "cleaning stuff" | "snacks" | "fruits" | "food" | "drinks" | "cutlery" | "tableware" | "containers"

            OBJ_CLN: "scrubby" | "sponge" | "cloth" | "cascade pod"
            OBJ_SNK: "pringles" | "crackers" | "potato chips"
            OBJ_FRU: "apple" | "orange" | "paprika"
            OBJ_FOD: "cereal" | "noodles" | "sausages"
            OBJ_DRI: "chocolate drink" | "coke" | "orange juice" | "grape juice" | "sprite"
            OBJ_CUT: "fork" | "knife" | "spoon"
            OBJ_TAB: "dish" | "bowl" | "glass"
            OBJ_CON: "tray" | "basket" | "bag"

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
            TWHICH: "which"
            TYOU: "you"
            TOBJECT: "object" "s"?
            TBACK: "back"

            PGENDERS: "man" | "woman" | "boy" | "girl" | "male person" | "female person"
            PGENDERP: "men" | "women" | "boys" | "girls" | "male" | "female"
            POSE: "sitting" | "standing" | "lying down"
            GESTURE: "waving" | "raising their left arm" | "raising their right arm" | "pointing to the left" | "pointing to the right"
            OPROP: "biggest" | "largest" | "smallest" | "heaviest" | "lightest" | "thinnest"

            NUM: "3" | "three"

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
            'TBACK': "back",

            'PGENDERS': "man" ,
            'PGENDERP': "men" ,
            'POSE': "sitting" ,
            'GESTURE': "waving",
            'OPROP': "biggest",

            'NUM' : "3",

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
            'WHATTOSAY0': "a joke",
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
        return idx

    def search(self, dic, key):
        for k in dic:
            if k == key: return True
        return False

    def tree2plan(self, tree):
        plan = []
        try:
            question_type = tree.children[0].children[0].data
        except:
            question_type = tree.children[1].children[0].data
        #print('question type : ' + question_type)
        #print('')
        terminals = self.getTerminals(tree)
        #print(terminals)
        #print('')

        if question_type == 'common_fndobj1':
            plan.append(['go', terminals['PLC']])
            plan.append(['count', terminals['OBJ']])
            plan.append(['go', 'operator'])
            plan.append(['tell', 'count'])

        elif question_type == 'common_fndobj2':
            plan.append(['go', terminals['ROOM']])
            plan.append(['find', terminals['OBJ']])

        elif question_type == 'fndobj1':
            plan.append(['go' , terminals['PLC1']])
            if self.search(terminals, 'CAT'):
                plan.append(['find', terminals['CAT'], terminals['OPROP'], 3])
            else:
                plan.append(['find', 'object', terminals['OPROP'], 3])
            plan.append(['go','operator'])
            plan.append(['tell','object',3])

        elif question_type == 'fndobj2':
            plan.append(['go', terminals['ROOM']])
            plan.append(['find', terminals['CAT'], 3])
            plan.append(['go', 'operator'])
            plan.append(['tell', 'object',3])


        elif question_type in ['followout1', 'followout2']:
            plan.append(['go', terminals['BEC1']])
            plan.append(['find', terminals['NAME1']])
            plan.append(['follow', ''])
            if self.search(terminals,'ROOM1'):
                plan.append(['go', terminals['ROOM1']])
            else:
                plan.append(['guide', terminals['BEC1']])

        elif question_type == 'incomplete1':
            plan.append(['ask_bec','BEC',terminals['NAME1']])
            plan.append(['go','BEC'])
            plan.append(['find', terminals['NAME1']])
            plan.append(['follow', ''])

        elif question_type == 'incomplete2':
            plan.append(['ask_obj','OBJ',terminals['CAT']])
            if self.search(terminals, 'OP'):
                plan.append(['get_cat3', 'OBJ'])
                plan.append(['go','operator'])
            elif self.search(terminals, 'NAME1'):
                plan.append(['ask_bec','BEC',terminals['NAME1']])
                plan.append(['get_cat3', 'OBJ'])
                plan.append(['go','BEC'])
                plan.append(['find', terminals['NAME1']])
            else:
                plan.append(['get_cat3', 'OBJ'])
                plan.append(['go', terminals['ROOM']])
                plan.append(['find', terminals['GESTURE']])
            plan.append(['give', ''])

        elif question_type == 'incomplete3':
            plan.append(['ask_bec','BEC',terminals['NAME1']])
            plan.append(['go','BEC'])
            plan.append(['find', terminals['NAME1']])
            plan.append(['guide', terminals['BEC2']])

        elif question_type == 'incomplete4':
            plan.append(['ask_bec','BEC',terminals['NAME1']])
            plan.append(['go','BEC'])
            plan.append(['find', terminals['NAME1']])
            plan.append(['ask_guide', 'BEC2'])
            plan.append(['guide_cat3', 'BEC2'])

        elif question_type == 'incomplete5':
            plan.append(['go', terminals['BEC1']])
            plan.append(['find', terminals['NAME1']])
            plan.append(['ask_guide', 'BEC2'])
            plan.append(['guide_cat3', 'BEC2'])

        elif question_type == 'erroneous1':
            if terminals['BEC1'] == terminals['BEC2']:
                plan.append(['error', terminals['BEC1'], 'BEC2'])
                plan.append(['go', terminals['BEC1']])
                plan.append(['find', terminals['NAME1']])
                plan.append(['guide', 'BEC2'])
            else:
                plan.append(['find_not', terminals['NAME1'], terminals['BEC1']])
                plan.append(['guide', terminals['BEC2']])

        elif question_type == 'erroneous3':
            if self.search(terminals, 'OBJ1'):
                plan.append(['error', terminals['OBJ1'], 'NAME1'])
            else:
                plan.append(['error', terminals['CAT1'], 'NAME1'])
            plan.append(['go', terminals['BEC1']])
            plan.append(['find', 'NAME1'])
            plan.append(['guide', terminals['BEC2']])

        elif question_type == 'erroneous4':
            plan.append(['error', terminals['BEC1'], 'ROOM2'])
            plan.append(['go', terminals['BEC1']])
            plan.append(['find', terminals['NAME1']])
            plan.append(['follow', 'ROOM2'])

        elif question_type == 'erroneous5':
            plan.append(['go', terminals['BEC1']])
            plan.append(['find_not', terminals['NAME1'], terminals['BEC1']])
            plan.append(['follow', terminals['ROOM2']])

        elif question_type == 'erroneous6':
            if self.search(terminals, 'OBJ1'):
                plan.append(['error', terminals['OBJ1'], 'NAME1'])
            else:
                plan.append(['error', terminals['CAT1'], 'NAME1'])
            plan.append(['go', terminals['BEC1']])
            plan.append(['find', 'NAME1'])
            plan.append(['follow', ''])

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
        if len(sentence.split()) < 2:
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
    parser = GPSR_parser_case3(max_iter = 1, debug = True)
    while True:
        sentence = input("\nInput sentence : ")
        plan = parser.parse(sentence)
        if parser.debug:
            print(plan)
