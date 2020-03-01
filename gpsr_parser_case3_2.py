'''
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
'''

class Parser():
    def __init__(self):
        self.verb_dict = {
            "take" : ["VGUIDE", "took"],
            "give" : ["VDEL", "gave"],
            "bring" : ["VDEL", "brought"],
            "deliver" : ["VDEL", "delivered"],
            "tell" : ["VTTELL", "told"],
            "go" : ["VGOPL", "went"],
            "navigate" : ["VGOPL", "navigated"],
            "find" : ["VFIND", "found"],
            "locate" : ["VFIND", "located"],
            "look for" : ["VFIND", "looked for"],
            "guide" : ["VGUIDE", "guided"],
            "escort" : ["VGUIDE", "escorted"],
            "lead" : ["VGUIDE", "led"],
            "accompany" : ["VGUIDE", "accompanied"],
            "follow" : ["VFOLLOW", "followed"],
            "go after" : ["VFOLLOW", "went after"],
            "come after" : ["VFOLLOW", "came after"],
            "meet" : ["VTMEET", "met"]
        }

        self.verb = [k for k in self.verb_dict]
        self.verb_past = [self.verb_dict[k][1] for k in self.verb_dict]

        self.obj_sing = ["scrubby", "sponge", "cloth", "cascade pod", "pringles",
                        "crackers", "potato chips", "apple", "orange", "paprika",
                        "cereal", "noodles", "sausages", "chocolate drink", "coke",
                        "orange juice", "grape juice", "sprite", "fork", "knife",
                        "spoon", "dish" , "bowl" , "cup", "tray" , "basket" , "bag"]

        self.obj_plur = ["scrubbies", "sponges", "clothes", "cascade pods",
                        "crackers", "potato chips", "apples", "oranges", "paprikas",
                        "cereals", "noodles", "sausages", "chocolate drinks", "cokes",
                        "orange juices", "grape juices", "sprites", "forks", "knives",
                        "spoons", "dishes" , "bowls" , "cups", "trays" , "baskets" , "bags"]

        self.obj_singisplur = ["noodle ", "sausage ", "cracker ", "potato chip "]

        self.cat_sing = ["cleaning stuff", "snacks", "fruits", "food", "drinks", "cutlery", "tableware", "containers"]

        self.cat_plur = ["cleaning stuffs", "snacks", "fruits", "foods", "drinks", "cutleries", "tablewares", "containers"]

        self.cat_singisplur = ["snack ", "fruit ",  "drink ", "container "]

        self.room = ["bedroom", "dining room", "living room", "kitchen", "corridor"]

        self.bec_sing = ["bed", "desk", "dining table", "exit", "couch", "end table",
                        "bookcase", "sink", "dishwasher", "entrance"]

        self.bec_plur = ["beds", "desks", "dining tables", "exits", "couches", "end tables",
                        "bookcases", "sinks", "dishwashers", "entrances"]

        self.plc_sing = ["side table", "desk", "dining table",  "end table", "bookcase",
                        "cupboard", "counter" , "storage table", "sink", "entrance"]

        self.plc_plur = ["side tables", "desks", "dining tables",  "end tables", "bookcases",
                        "cupboards", "counters" , "storage tables", "sinks", "entrances"]

        self.name = ["alex", "charlie", "elizabeth", "francis", "jennifer", "linda",
                     "mary", "patricia", "robin", "skyler", "james", "john", "michael",
                     "robert", "william"]

        self.erase = [" the ", " from " , " on ", " to ", " at " , " of ", " in ", " a ",
                      " there ", " are ", " is ", " and ", " may ", " can ", " will "]

        self.pronoun = ["it", "him", "her"]
        self.op = ["me"]


        self.gender_sing = ["man", "woman", "boy", "girl", "male person", "female person"]
        self.gender_plur = ["men", "women", "boys", "girls", "male", "female"]
        self.pose = ["sitting", "standing", "lying down"]
        self.gesture = ["waving", "raising their left arm", "raising their right arm",
                        "pointing left", "pointing right"]
        self.oprop = ["biggest", "largest", "smallest", "heaviest", "lightest", "thinnest"]
        self.num = ["3", "three"]


        self.all = self.verb + self.obj_sing + self.obj_plur + self.room + self.bec_sing + \
                   self.bec_plur + self.plc_sing + self.plc_plur + self.name + self.erase + \
                   self.pronoun + self.op + self.gender_sing +self.gender_plur + self.pose + \
                   self.gesture + self.oprop + self.num + self.cat_sing + self.cat_plur + \
                   self.verb_past#TODO: update

        self.plur = self.obj_plur + self.bec_plur + self.plc_plur + self.cat_plur + self.gender_plur
        self.sing = list(set(self.all) - set(self.plur))

        self.rep_list = [
            ('chocolate drink', ['chocolate', 'choco drink', 'choco']),
            ('coke', ['coca-cola', 'coca cola', 'cola', 'cook', 'code','hulk']),
            ('sprite', ['cider', 'flight', 'price', 'stride', 'stripe', 'brides', 'sprint', 'prince', 'spry']),
            ('orange juice', ['jiu-jitsu', 'horseshoe']),
            ('grape juice', ['grape', 'pictures', 'vape juice', 'grapes', 'richest', 'ranger']),
            ('james', ['games']),
            ('skyler', ['skylar', 'skyla']),
            ('william', ['alien', 'williams', 'volume']),
            ('bed', ['fats']),
            ('standing',['sending', 'stepping']),
            ('cupboard',['cardboard']),
            ('couch',['clutch','college','coach']),
            ('cutlery',['cartoons', 'cartoon','cut learn']),
            ('bowl',['ball']),
            ('heaviest', ['best']),
            ('cloth',['close', 'clock']),
            ('fruit', ['brute']),
            ('drink', ['brink']),
            ('cereal', ['surreal']),
            ('noodle', ['google']),
            ('orange', ['french', 'wrench']),
            ('paprika', ['africa', 'pepper guy']),
            ('snack', ['snap']),
            ('cracker', ['soccer', 'croacker']),
            ('tableware', ['cable wear', 'table where', 'cable where']),
            (' knife ', [' nice ']),
            ('spoon', ['school']),
            ('fork', ['phone']),
            ('cleaning stuff', ['cleaning stops'])
        ]

    def singular(self, plur):
        if plur[-3:] == 'ves' and plur[:-3]+'fe' in self.sing:
            return plur[:-3] + 'fe'
        if plur[-3:] == 'ies' and plur[:-3]+'y' in self.sing:
            return plur[:-3] + 'y'
        if plur[-2:] == 'es' and plur[:-2] in self.sing:
            return plur[:-2]
        if plur[-1:] == 's' and plur[:-1] in self.sing:
            return plur[:-1]
        if plur[:-1] in self.sing:
            return plur[:-1]
        return plur

    def present(self, past):
        for k in self.verb:
            if self.verb_dict[k][1] is past:
                return k
        return ''

    def verb_task(self, verb):
        return self.verb_dict[verb][0]

    def sen2task(self, sentence):

        idx = []
        idx += [sentence.find(verb) for verb in self.verb]
        idx.append(len(sentence))
        idx.sort()
        idx = [i for i in idx if i != -1]
        subsentence = [ sentence[idx[i]:idx[i+1]] for i in range(len(idx)-1) ]
        subsentence = [ s.strip(" ") for s in subsentence if s != "" ]
        print(subsentence)
        subtask = []
        for s in subsentence:
            verb = [ v for v in self.verb if v in s ]
            verb = verb[0]
            target = s.replace(verb,"",1).strip(" ")
            subtask.append([verb,target])
        print(subtask)
        return subtask

    def get_element(self, string, list):
        split = string.split()
        ret = []
        for i in range(len(split)-1):
            w = split[i] + ' ' + split[i+1]
            if w in list:
                ret.append(w)
        for s in split:
            if s in list:
                ret.append(s)
        return ret

    def get_info(self, target):
        object = self.get_element(target, self.obj_sing)
        category = self.get_element(target, self.cat_sing)
        placement = self.get_element(target, self.plc_sing)
        beacon = self.get_element(target, self.bec_sing)
        room = self.get_element(target, self.room)
        name = self.get_element(target, self.name)
        gesture = self.get_element(target, self.gesture)

        return object, category, placement, beacon, room, name, gesture

    def task2plan(self, task, plan):
        verb_types = [ self.verb_task(subtask[0]) for subtask in task ]
        infos = [ subtask[1] for subtask in task ]
        if len(verb_types) == 1:
            obj, cat, plc, bec, room, name, gesture = self.get_info(infos[0])
            if "VTTELL" in verb_types[0]:
                if ("how" in infos[0] or "many" in infos[0]) and len(obj) > 0 and len(plc) > 0:
                    plan.append(['go', plc[0]])
                    plan.append(['count', obj[0]])
                    plan.append(['go', 'operator'])
                    plan.append(['tell', 'count'])
                elif ("which" in infos[0] or "three" in infos[0] or "3" in infos[0]) and len(plc) > 0:
                    opr = [opr for opr in self.oprop if opr in infos[0]]
                    if opr == []:
                        return False
                    plan.append(['go' , plc[0]])
                    if len(cat) > 0:
                        plan.append(['find', cat[0], opr[0], 3])
                    else:
                        plan.append(['find', 'object', opr[0], 3])
                    plan.append(['go','operator'])
                    plan.append(['tell','object',3])
            elif "VFIND" in verb_types[0] and len(room) > 0:
                if len(obj) > 0:
                    plan.append(['go', room[0]])
                    plan.append(['find', obj[0]])
                elif len(cat) > 0:
                    plan.append(['go', room[0]])
                    plan.append(['find', cat[0], 3])
                    plan.append(['go', 'operator'])
                    plan.append(['tell', 'object',3])
            elif "VFOLLOW" in verb_types[0] and len(name) > 0:
                plan.append(['ask_bec','BEC',name[0]])
                plan.append(['go','BEC'])
                plan.append(['find', name[0]])
                plan.append(['follow', ''])
            elif "VDEL" in verb_types[0] and len(cat) > 0:
                plan.append(['ask_obj','OBJ',cat[0]])
                if 'me' in infos[0]:
                    plan.append(['get_cat3', 'OBJ'])
                    plan.append(['go','operator'])
                elif len(name) > 0:
                    plan.append(['ask_bec','BEC',name[0]])
                    plan.append(['get_cat3', 'OBJ'])
                    plan.append(['go','BEC'])
                    plan.append(['find', name[0]])
                elif len(gesture) > 0 and len(room) > 0:
                    plan.append(['get_cat3', 'OBJ'])
                    plan.append(['go', room[0]])
                    plan.append(['find', gesture[0]])
                plan.append(['give', ''])
            elif "VGUIDE" in verb_types[0] and len(bec) > 0:
                if len(obj) > 0: #TODO: multiple: order!!!!!!!!!!!!!!!
                    plan.append(['error', obj[0], 'NAME1'])
                    plan.append(['go', bec[0]])
                    plan.append(['find', 'NAME1'])
                    plan.append(['guide', bec[0]])
                elif len(cat) > 0:
                    plan.append(['error', cat[0], 'NAME1'])
                    plan.append(['go', bec[0]])
                    plan.append(['find', 'NAME1'])
                    plan.append(['guide', bec[1]])
                elif len(bec) > 1:
                    plan.append(['find_not', name[0], bec[0]])
                    plan.append(['guide', bec[1]])
                elif len(bec) < 2 and infos[0].replace(bec[0],'',1).find(bec[0]) != -1:
                    plan.append(['error', bec[0], 'BEC2'])
                    plan.append(['go', bec[0]])
                    plan.append(['find', name[0]])
                    plan.append(['guide', 'BEC2'])
                elif len(bec) < 2:
                    plan.append(['ask_bec','BEC',name[0]])
                    plan.append(['go','BEC'])
                    plan.append(['find', name[0]])
                    plan.append(['guide', bec[0]])

        if len(verb_types) == 2:
            if "VTMEET" in verb_types[0] and "VGUIDE" in verb_types[1]:
                obj, cat, plc, bec, room, name, gesture = self.get_info(infos[0])
                if len(name) == 0:
                    return False
                plan.append(['ask_bec','BEC',name[0]])
                plan.append(['go','BEC'])
                plan.append(['find', name[0]])
                plan.append(['ask_guide', 'BEC2'])
                plan.append(['guide_cat3', 'BEC2'])

        elif len(verb_types) == 3:
            if "VTMEET" in verb_types[0] and "VFOLLOW" in verb_types[1]:
                obj, cat, plc, bec, room, name, gesture = self.get_info(infos[0])
                _, _, _, _, room2, _, _ = self.get_info(infos[2])
                if len(bec) < 0:
                    return False
                if len(name) < 0:
                    return False
                plan.append(['go', bec[0]])
                plan.append(['find', name[0]])
                plan.append(['follow', ''])
                if len(room2) > 0:
                    plan.append(['go', room2[0]])
                else:
                    plan.append(['guide', bec[0]])
            elif "VGOPL" in verb_types[0] and "VTMEET" in verb_types[1]:
                _, _, _, bec, _, _, _ = self.get_info(infos[0])
                obj, cat, _, _, _, name, _ = self.get_info(infos[1])
                _, _, _, bec2, room2, _, _ = self.get_info(infos[2])
                if len(obj) > 0 and len(bec) > 0:
                    plan.append(['error', obj[0], 'NAME1'])
                    plan.append(['go', bec[0]])
                    plan.append(['find', 'NAME1'])
                    plan.append(['follow', ''])
                elif len(cat) > 0 and len(bec) > 0:
                    plan.append(['error', cat[0], 'NAME1'])
                    plan.append(['go', bec[0]])
                    plan.append(['find', 'NAME1'])
                    plan.append(['follow', ''])
                elif len(bec2) > 0 and len(name) > 0:
                    plan.append(['error', bec[0], 'ROOM2'])
                    plan.append(['go', bec[0]])
                    plan.append(['find', name[0]])
                    plan.append(['follow', 'ROOM2'])
                elif len(room2) > 0 and len(bec) > 0 and len(name) > 0:
                    plan.append(['go', bec[0]])
                    plan.append(['find_not', name[0], bec[0]])
                    plan.append(['follow', room2[0]])
                elif len(bec) > 0 and len(name) > 0:
                    plan.append(['go', bec[0]])
                    plan.append(['find', name[0]])
                    plan.append(['ask_guide', 'BEC2'])
                    plan.append(['guide_cat3', 'BEC2'])

        if len(plan) == 0:
            return False
        return True

    def replace(self, sentence):
        sentence = sentence.lower().replace('.','').replace(',','') .replace('\'','').replace('\"','').strip(' ')
        sentence = sentence + ' '
        for rep_tuple in self.rep_list:
            for rep in rep_tuple[1]:
                sentence = sentence.replace(rep, rep_tuple[0])
        for plur in self.plur:
            sentence = sentence.replace(plur, self.singular(plur))
        for past in self.verb_past:
            sentence = sentence.replace(past, self.present(past))
        for eras in self.erase:
            sentence = sentence.replace(eras, ' ')
        for singplur in self.obj_singisplur:
            sentence = sentence.replace(singplur, singplur[:-1]+'s ')
        for singplur in self.cat_singisplur:
            sentence = sentence.replace(singplur, singplur[:-1]+'s ')
        return sentence

    def parse(self, sentence):
        try:
            sentence = self.replace(sentence)
            task = self.sen2task(sentence)
            plan = []
            ret = self.task2plan(task, plan)
            if ret is True and plan is not []:
                return plan
            return None
        except Exception as e:
            return None
        return None

if __name__ == '__main__':
    parser = Parser()

    #parser.singular()

    while True:
        sentence = raw_input('input sentence : ')
        plan = parser.parse(sentence)
        print(plan)
