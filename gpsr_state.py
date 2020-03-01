#!usr/bin/python2.7
from __future__ import print_function
import enum
import os
import random
import time
from functools import reduce
import cv2

import gpsr_config as config
import gpsr_func as func
from gpsr_parser_case1 import GPSR_parser_case1
from gpsr_parser_case2 import GPSR_parser_case2
from gpsr_parser_case3_2 import Parser as GPSR_parser_case3

count = 0 # TODO: just for test


# TODO: **************** find_object_at_location : do exception *************************
# TODO: check: guide_flag & new_loc & new_name

class StateResult(enum.IntEnum):
    SUCCESS = 0
    FAILURE = 1
    INTERRUPT = 2
    SKIP = 3
    DETOUR = 4
    REVERT = 5
    DEBUGGING = -2
    ABORT_TEST = -1


class State(enum.IntEnum):
    INIT = 0
    GO_TO_OPERATOR = 1
    FIRST_COMMAND = 10
    FIRST_COMMAND_EXECUTE = 11
    SECOND_COMMAND = 20
    SECOND_COMMAND_EXECUTE = 21
    THIRD_COMMAND = 30
    THIRD_COMMAND_EXECUTE = 31
    EXIT_ARENA = 40
    FINISHED = -1


class StateMachine(object):

    def __init__(self):
        self.parser_1 = GPSR_parser_case1()
        self.parser_2 = GPSR_parser_case2()
        self.parser_3 = GPSR_parser_case3()

        if config.pio is None:
            print("config.pio should be initialized first")
            return
        self.state = State.INIT
        self.elapsed_times = []
        self.start_time = 0.0
        self.prev_state = State.INIT
        self.prev_tic = 0.0
        self.subtask_list = []
        self.wp_operator = 'operator'
        self.wp_exit = 'exit'
        # for test, need to delete
        self.object_list = reduce(lambda x, y: x+y, list(func.category_dict.values()))
        self.name_list = func.name_list
        self.location_dict = func.location_dict
        self.room_list = func.room_list
        self.category_dict = func.category_dict
        self.question_dict = func.question_dict
        self.pose_list = func.pose_list
        self.gesture_list = func.gesture_list
        self.pgenders_list = func.pgenders_list
        self.pgenderp_list = func.pgenderp_list
        self.beacon_list = func.beacon_list
        self.category_location_dict = func.category_location_dict

        self.flag_terminate = False
        self.logger = config.pio.logger

        # flags
        self.ltarget = None
        self.rtarget = None
        self.get_fail = False
        self.get_obj = None
        self.new_loc = None
        self.new_name = None
        self.new_obj = None
        self.find_person = None
        self.find_obj_cat_sin = None
        self.find_obj_cat_pop = None
        self.count_target = None
        self.count_target_num = 0
        self.ask_name = None
        self.see_target = None
        self.see_target_kind = None
        ###
        self.num = 0

    def __del__(self):
        pass

    def terminate(self):
        self.flag_terminate = True

    def init_flag(self):

        self.ltarget = None
        self.rtarget = None
        self.get_fail = False
        self.get_obj = None
        self.new_loc = None
        self.new_name = None
        self.new_obj = None
        self.find_person = None
        self.find_obj_cat_sin = None
        self.find_obj_cat_pop = None
        self.count_target = None
        self.count_target_num = 0
        self.ask_name = None
        self.see_target = None
        self.see_target_kind = None


    def ready(self):
        config.pio.say("I am ready. Please open the door.")
        if config.params.debugging:
            pass
        else:
            time.sleep(3)
        config.pio.set_static_map(True)
        config.pio.clear_map()
        return StateResult.SUCCESS

    ##############

    # TODO: needed?
    def pad(self, w):
        return ' ' + w + ' '

    def replace_words(self, string, rep_list):
        """Replace wrong words/phrases to desired ones"""
        replaced = self.pad(string)  # avoid: "smiles".replace("mile","1.6km") == "s1.6kms"
        for right, wrongs in rep_list:
            for wrong in wrongs:
                replaced = replaced.replace(self.pad(wrong), self.pad(right))
        return replaced.strip()


    def randsay(self, speech_list):
        rand_idx = random.randint(0, len(speech_list) - 1)
        config.pio.say(speech_list[rand_idx])

    def confirm(self, max_trials=3):
        for t in range(max_trials):
            #yesno = self.catch_words(config.params.yes_or_no)
            yesno = True#config.pio.start_recording(reset=True,base_duration=5.0)()
            if yesno:
                #yesno = yesno[0]
                break
            config.pio.say("Sorry, tell me yes or no again.")
        else:
            return 0
        return 1 if yesno in config.params.positives else -1

    ##############

    def parse_command(self, command,category):
        if category == 1:
            command_list = self.parser_1.parse(command)
        elif category == 2:
            command_list = self.parser_2.parse(command)
        elif category == 3:
            command_list = self.parser_3.parse(command)
        else :
            return None

        return command_list

    def subtasks_to_str(self, subtask_list):
        print(subtask_list) # TODO
        return ''

    def convert(self, sentence):
        sentence = sentence.replace("curry", "corridor")
        sentence = sentence.replace("with", "meet")
        sentence = sentence.replace("bathroom", "bedroom")
        sentence = sentence.replace("meets", "meet")
        sentence = sentence.replace("midtown", "meet")
        sentence = sentence.replace("timetable", "dining table")
        return sentence


    def get_command(self, category ,max_trials=10, timeout=60,input_command=None):
        hint = self.parser_3.all
        config.pio.set_speech_hints(hints=hint)
        command = ""
        input_command = []
        global count
        trial = 0
        tic = time.time()
        config.pio.say("hello i am pepper, i will execute g p s r")
        while trial < max_trials and time.time() - tic < timeout:
            if trial >= 1:
                config.pio.say("sorry i cant understand a command by speech")
                config.pio.say("please show me the QR code in front of my eyes for a while")
                while not config.pio.barcode_memory:
                    time.sleep(0.6)
                    print("WHILE" + config.pio.barcode_memory)
                    command = config.pio.barcode_memory
                config.pio.barcode_memory = ""
            else :
                config.pio.say("please give me a command")
                try:
                    command = config.pio.simple_stt()
                except Exception:
                    trial += 1
                    continue

            command = self.convert(command)
            config.pio.logger.info(command) # TODO
            print("COMMAND" + command)
            subtask_list = self.parse_command(command,category)
            if subtask_list is None :
                config.pio.say("sorry i cannot understand your command")
                config.pio.say("please show QR code")
            print(subtask_list)
            if subtask_list:
                config.pio.say("your command is " + command)
                command_str = self.subtasks_to_str(subtask_list)  # TODO
                #confirm = config.pio.hri.confirm_speech(command) # TODO
                confirm=0
                if confirm == 0:
                    break
            else:
                self.randsay(["Sorry, tell me your command again.",
                              "Sorry, I didn't catch that.",
                              "Sorry, Would you repeat again?",
                              ])
            trial += 1
        else:
            return StateResult.FAILURE

        config.pio.hri.got_it()
        self.subtask_list = subtask_list
        print(self.subtask_list)
        return StateResult.SUCCESS

    def exec_command(self):
        print("[---EXEC FLAG---]")
        subtask_list = self.subtask_list  # self.subtask_list: [ [], [], ... , [] ]
        if subtask_list is None:
            return StateResult.FAILURE
        # ----------------------------------------------------------- execute command
        for i in range(0,len(subtask_list)) :
            config.pio.logger.info(subtask_list[i])  # print execute info
            verb = subtask_list[i][0]

            if verb == "get" :
                # CMD******
                # get obj *
                # *********
                # using self.ltarget
                # *********
                print("[GET FLAG] start")

                obj = subtask_list[i][1]

                # *******************TODO*****************
                #if obj == "coke" or obj =="cookies":
                #    obj = "bottle"
                # ****************************************


                room = None
                # case: [['go', 'cabinet'], ['get', 'pringles']]
                if self.ltarget is not None:
                    room = self.ltarget
                # case: when should guess where the object is
                else: 
                    room = func.get_loc_from_obj(obj)

                if room is None:
                    config.pio.say("i cannot get a %s" % obj)
                    return StateResult.FAILURE

                if self.ltarget is not None:
                    config.pio.say("i will get a %s" % (obj))
                else:
                    config.pio.say("i will go to the %s \\pau=10\\ and get a %s" %(room, obj))
                    result = func.go_to_location(room)
                    if result is False:
                        return StateResult.FAILURE


                get_obj = func.find_object_at_location(obj,find_again=False)
                if get_obj is False:
                    self.get_fail = True
                    self.get_obj = obj
                    continue

                result = config.pio.go_to_target_2018(target=get_obj)
                if result is not True:
                    result = config.pio.go_to_target_2018(target=get_obj)
                    if result is not True:
                        return StateResult.FAILURE

                config.pio.rotate_in_degree(180, speed=0.8)
                person = func.delivery_find_person(timeout=40)
                if person is None:
                    self.get_fail = True 
                    self.get_obj = obj
                    continue

                func.grab_bincan(drink=obj, person_name=person)

                print("[GET FLAG] finished")

            elif verb == "go" :
                # CMD***************************
                # go plc/bec/room/operator/BEC *
                # ******************************
                print("[GO FLAG] start")

                target = subtask_list[i][1]

                if target is "BEC":
                    target = self.new_loc

                # CAT1 go to room & go to operator
                if target in self.room_list or target is "operator":
                    result = func.go_to_location(target)
                # CAT1 go to location ( bed, sideboard etc...)
                else : # if target is in locations or target is unvalid

                    room = func.find_room_from_loc(target)
                    loc = target

                    if room is None:
                        print("[FAILURE] [GO] unvalid location")
                        return StateResult.FAILURE

                    result = func.go_to_location(loc)

                    if result is False:
                        # if loc is wrong, go to room
                        result = func.go_to_location(room)
                        if result is False:
                            return StateResult.FAILURE

                    # case: e.g. [['go', 'bathroom cabinet'], ['get', 'pringles']]
                    self.ltarget = loc
                    self.rtarget = room

                print("[GO FLAG] finished")

            elif verb == "find" :
                # CMD*****************************
                # find obj/cat/name/anyone/NAME1 *
                # ********************************
                # obj/cat/name/anyone
                # genders/gesture/pose
                # 'object' oprop/'object' oprop 3
                # cat 3/cat oprop/cat oprop 3
                # NAME1
                # ********************************
                print("[FIND FLAG] start")
                
                target = subtask_list[i][1]
                print(target)

                if target is "NAME1":
                    target = self.new_name # e.g. ['error', 'cookies', 'NAME1']



                # *****************TODO: tmp****************
                #if target == "fruits":
                #    target = "drinks"
                # *************************************



                # name
                if target in self.name_list :
                    config.pio.say(target)
                    config.pio.say("\\pau=10\\ please wave your hand")
                    self.find_person = func.find_person_at_location(target) # TODO
                # "object" string
                elif target is "object" :
                    # find 'object' oprop
                    if len(subtask_list[i]) == 3:
                        oprop = subtask_list[i][2]
                        if oprop in ["biggest", "largest", "heaviest"]:
                            res = func.sort_object_by_size(target, ascending=False, numbers=1)

                            if res is False:
                                res = None
                            self.find_obj_cat_sin = res
                        elif oprop in ["smallest", "thinnest", "lightest"]:
                            res = func.sort_object_by_size(target, ascending=True, numbers=1)

                            if res is False:
                                res = None
                            self.find_obj_cat_sin = res
                    # find 'object' oprop 3
                    elif len(subtask_list[i]) == 4:
                        oprop = subtask_list[i][2]
                        number = subtask_list[i][3]
                        if oprop in ["biggest", "largest", "heaviest"]:
                            res = func.sort_object_by_size(self.object_list, ascending=False, numbers=number)
                            if res is False:
                                res = []
                            self.find_obj_cat_pop = res
                        elif oprop in ["smallest", "thinnest", "lightest"]:
                            res = func.sort_object_by_size(self.object_list, ascending=True, numbers=number)
                            if res is False:
                                res = []
                            self.find_obj_cat_pop = res
                    else:
                        return StateResult.FAILURE
                   
                # CATEGORY
                elif target in self.category_dict:
                    # CMD*****************
                    # find cat
                    # find cat 3
                    # find cat oprop
                    # find cat oprop 3
                    # ********************

                    # find cat
                    if len(subtask_list[i]) == 2:
                        res = func.find_category_at_location(target)
                        self.find_obj_cat_sin = res
                        config.pio.say("I see %s" % (res.class_string))
                    # find cat 3
                    # find cat oprop
                    elif len(subtask_list[i]) == 3 :
                        oprop = subtask_list[i][2]
                        if oprop in ["biggest","largest","heaviest"] :
                            res = func.sort_category_by_size(target,ascending=False,numbers=1)
                            if res is False:
                                res = None
                            self.find_obj_cat_sin = res
                        elif oprop in ["smallest", "thinnest", "lightest"] :
                            res = func.sort_category_by_size(target,ascending=True,numbers=1)
                            if res is False:
                                res = None
                            self.find_obj_cat_sin = res
                        elif str(oprop).isdigit(): # TODO
                            res = func.find_multiple_objects_by_category(category=target)
                            if res is False:
                                res = []
                            self.find_obj_cat_pop = res
                    # find cat oprop 3
                    elif len(subtask_list[i]) == 4:
                        print(target)
                        oprop = subtask_list[i][2]
                        number = subtask_list[i][3]
                        if oprop in ["biggest","largest","heaviest"] :
                            res = func.sort_category_by_size(target,ascending=False,numbers=number)
                            if res is False:
                                res = []
                            self.find_obj_cat_pop = res
                        elif oprop in ["smallest","thinnest","lightest"] :
                            res = func.sort_category_by_size(target,ascending=True,numbers=number)
                            if res is False:
                                res = []
                            self.find_obj_cat_pop = res
                    else:
                        return StateResult.FAILURE

                # OBJECT
                elif target in self.object_list:
                    # find obj
                    if len(subtask_list[i]) == 2:
                        res = func.find_object_at_location(target)
                        if res is False:
                            res = None
                        self.find_obj_cat_sin = res
                        config.pio.say("I see the target")
                    else:
                        return StateResult.FAILURE
                   
                # anyone
                elif target == "anyone" :
                    result = func.find_person_anyone()
                    config.pio.say("i see person")
                # genders/gesture/pose
                #elif target in func.condition_dict.keys() :
                elif target in func.gender_gesture_pose_list:
                    print("gender_gesture_pose")
                    const = ()
                    if target is "man":
                        const = ("male")
                    elif target is "women":
                        const = ("female")
                    elif target is "boy":
                        const = ("male", "young")
                    elif target is "girl":
                        const = ("female", "young")
                    elif target is "(male person)":
                        const = ("male")
                    elif target is "(female person)":
                        const = ("female")
                    else:
                        const = (target)
                    print("constratin:")
                    print(target)

                    find_result = func.find_by_constraint(constraint=const)
                    if find_result is False:
                        return StateResult.FAILURE
                    config.pio.say("i see person with %s" % (target))

                    result = config.pio.go_to_target_2018(find_result)

                    if result is None:
                        return StateResult.FAILURE
                else:
                    return StateResult.FAILURE

                print("[FIND FLAG] finished")

            elif verb == "answer" :
                # CMD**************************
                # answer predefined/whattosay *
                # *****************************
                print("[ANSWER FLAG] start")

                target = subtask_list[i][1]

                # answer predefined
                if target == "predefined" :
                    result = func.reply_question()
                # answer whattosay
                else :
                    result = func.tell_information(target)

                print("[ANSWER FLAG] finished")

            elif verb == "count" :
                # CMD****************
                # count
                # obj/pgenderp/pose
                # *******************
                print("[COUNT FLAG] start")

                target = subtask_list[i][1]

                # ***************** TODO *****************
                if target is "cookies" or target is "apple" :
                    target = "bottle"

                # count obj
                if target in self.object_list :
                    num = func.count_objects(target)
                    self.count_target = target
                    self.count_target_num = num
                # count pgenderp
                elif target in self.pgenderp_list :
                    num = func.count_objects(target)
                    self.count_target = target
                    self.count_target_num = num
                # count pose
                elif target in self.pose_list :
                    num = func.count_objects(target)
                    self.count_target = target
                    self.count_target_num = num
                elif target in self.category_dict.keys():
                    num = func.count_category(target)
                    self.count_target = target
                    self.count_target_num = num
                else:
                    return StateResult.FAILURE

            elif verb == "ask" :
                # CMD*******
                # ask name *
                # **********
                print("[ASK FLAG] start")

                target = subtask_list[i][1]
                # ask name
                if target is "name" :
                    self.ask_name = func.ask_name()
                else:
                    return StateResult.FAILURE
                
                print("[ASK FLAG] finished")

            elif verb == "tell" :
                # CMD**************
                # tell
                # count/name/gender/pose
                # "object"/"object" 3
                # *****************
                print("[TELL FLAG] start")

                target = subtask_list[i][1]

                # count obj/pgenderp/pose
                if target == "count":
                    if self.count_target is not None:
                        config.pio.say("there are \\pau=10\\" + str(self.count_target_num) + " \\pau=10\\" + self.count_target)
                    else:
                        config.pio.say("I cannot find anything")
                # ask name
                elif target == "name":
                    if self.ask_name is not None:
                        config.pio.say("the name is \\pau=10\\" + self.ask_name)
                    else:
                        config.pio.say("I cannot get a name")
                # see gender/pose
                elif target == "gender" or target == "pose":
                    if self.see_target is None:
                        config.pio.say("I cannot see \\pau=10\\" + self.see_target_kind + " of the person")
                    else:
                        config.pio.say("the " + self.see_target_kind + " of the person is " + self.see_target)
                # find
                # object/cat/'object' oprop/cat oprop
                # cat 3/'object' oprop 3/ cat oprop 3
                elif target == "object":
                    # tell "object"
                    if len(subtask_list[i]) == 2:
                        if self.find_obj_cat_sin is not None:
                            config.pio.say("I see \\pau=10\\" + self.find_obj_cat_sin.class_string)
                        else:
                            config.pio.say("I cannot find anything")
                    # tell "object" 3
                    elif len(subtask_list[i]) == 3:
                        print("tell object 3")
                        if self.find_obj_cat_pop: #is not None:
                            obj_cat_strs = ""
                            for i in range(len(self.find_obj_cat_pop)):
                                obj_cat_strs += self.find_obj_cat_pop[i].class_string
                                obj_cat_strs += " \\pau=10\\"
                            config.pio.say("I see \\pau=10\\" + obj_cat_strs)
                        else:
                            config.pio.say("I cannot find anything")
                    else:
                        return StateResult.FAILURE

                print("[TELL FLAG] finished")

            elif verb == "put" :
                # CMD**
                # put *
                # *****
                print("[PUT FLAG] start")

                if self.get_fail is True:
                    config.pio.say("sorry i failed to get " + self.get_obj)
                    config.pio.say("so i cant give you a " + self.get_obj)
                else :
                    config.pio.say("Sorry \\pau=10\\ i cannot put the drink")
                    config.pio.say("Can you pick up the drink \\pau=10\\ in my hand?")
                    func.delivery()

                print("[PUT FLAG] finished")

            elif verb == "give" :
                # CMD***
                # give *
                # ******
                print("[GIVE FLAG] start")

                if self.get_fail is True:
                    config.pio.say("sorry i  failed to get " + self.get_obj)
                    config.pio.say("so i cant give you a " + self.get_obj)
                else :
                    func.delivery()

                print("[GIVE FLAG] finished")

            elif verb == "see" :
                # CMD**************
                # see gender/pose *
                # *****************
                print("[SEE FLAG] start")

                cat = subtask_list[i][1]

                # see gender
                if cat is "gender":
                    result = func.recognize_feature("gender")
                    self.see_target = result
                    self.see_target_kind = "gender"
                # see pose
                elif cat is "pose":
                    result = func.recognize_feature("pose")
                    self.see_target = result
                    self.see_target_kind = "pose"

                print("[SEE FLAG] finished")

            elif verb == "guide":
                # CMD*************
                # guide bec/BEC2 *
                # ****************
                print("[GUIDE FLAG] start")

                target = subtask_list[i][1]

                if target is "BEC2":
                    target = self.new_loc

                # TODO
                person = self.find_person

                if target in self.beacon_list : # ltarget is location (not room)
                    config.pio.say("I can guide you \\pau=20\\ please follow me")
                    result = func.guide_person(waypoint=target) # TODO
                    if not result:
                        result = config.pio.go_to_waypoint_2018(target)
                        if result is None:
                            return StateResult.FAILURE
                    else :
                        config.pio.say("arrive at " + target + ", have a nice day")
                else:
                    return StateResult.FAILURE

                print("[GUIDE FLAG] finished")

            elif verb == "follow" :
                # CMD*******************
                # follow ''/room/ROOM2 *
                # **********************
                print("[FOLLOW FLAG] start")

                fff = True
                dest = subtask_list[i][1]
                stop = "stop"

                if dest is '':
                    dest = None
                    stop = "stop"
                    fff = False
                elif dest is "ROOM2":
                    dest = self.new_loc

                if self.find_person is None:
                    return StateResult.FAILURE

                result = func.follow_person(target=self.find_person,stop_word=stop, destination=dest)
                if result is False and fff is True:
                    print("going to %s" % dest)
                    func.go_to_location(dest, say=False)
                print("[FOLLOW FLAG] finished")

            elif verb == "get_cat3":
                # CMD***********
                # get_cat3 OBJ *
                # **************
                # using self.new_obj
                # **************
                print("[GET_CAT3 FLAG] start")

                obj = self.new_obj
                category = self.new_obj  

                if category not in self.category_dict.keys():
                    for i, j in self.category_dict.items():
                        if obj in j:
                            category = i
                if category not in self.category_dict.keys():
                    category = "drinks"

                room = self.category_location_dict[category]

                # TODO
                # go to room and get obj
                config.pio.say("i will go to the \\pau=10\\ %s \\pau=10\\ and i will get a %s" % (room, obj))
                result = config.pio.go_to_waypoint_2018(room)

                if result is None:
                    return StateResult.FAILURE

                get_obj = func.find_object_at_location(obj,find_again=False)
                if get_obj is False:
                    self.get_fail = True # TODO: is it right?
                    self.get_obj = obj
                    continue
                result = config.pio.go_to_target_2018(target=get_obj)
                if result is not True:
                    result = config.pio.go_to_target_2018(target=get_obj) # TODO
                    if result is not True: 
                        return StateResult.FAILURE
                config.pio.rotate_in_degree(180, speed=0.8)
                person = func.delivery_find_person(timeout=40)
                if person is None:
                    self.get_fail = True  # TODO: is it right?
                    self.get_obj = obj
                    continue
                func.grab_bincan(drink=obj, person_name=person)

                print("[GET_CAT3 FLAG] finished")

            elif verb == "guide_cat3":
                # CMD**************
                # guide_cat3 BEC2 *
                # *****************
                print("[GUIDE_CAT3 FLAG] start")

                target = self.new_loc # because of BEC2 
                person = self.find_person

                config.pio.say("please follow me")
                result = func.guide_person(waypoint=target) 
                if not result:
                    return StateResult.FAILURE

                print("[GUIDE_CAT3 FLAG] finished")
                
            elif verb == "ask_guide":
                # CMD*************
                # ask_guide BEC2 *
                # ****************
                # self.new_loc updated
                # ****************
                print("[ASK_GUIDE] start")

                config.pio.say("where do you want to go? \\pau=20\\ i can guide you")

                while True:
                    target = config.pio.simple_stt()
                    for b in self.beacon_list:
                        c = b.split()

                        result = True
                        for j in c:
                            if not config.pio.find_word(j, source=target):
                                result = False

                        if result:
                            break

                    if result:
                        target = "you want to go " + b
                        result = config.pio.hri.confirm_speech(target)
                        if result is 0:
                            target = b
                            break

                    config.pio.say("please say again")

                if result is 0:
                    self.new_loc = target.strip()
                    print("[ASK GUIDE] new loc: %s" % (self.new_loc))
                else:
                    self.new_loc = None

                print("[ASK_GUIDE] finished")

            elif verb == "ask_bec":
                # CMD***************
                # ask_bec BEC name *
                # ******************
                # self.new_loc updated
                # ******************
                print("[ASK_BEC FLAG] start")

                # e.g. ['ask_bec', 'BEC', 'john']
                name = subtask_list[i][2]

                config.pio.say("where \\pau=10\\ can i find %s" % name)

                while True:
                    target = config.pio.simple_stt()

                    for b in self.beacon_list:
                        print(b)
                        c = b.split()

                        result = True
                        for j in c:
                            if not config.pio.find_word(j, source=target):
                                result = False

                        if result:
                            break

                    if result:
                        target = b
                        result = config.pio.hri.confirm_speech(target)
                        if result is 0:
                            target = b
                            break
                    
                    config.pio.say("please say again")

                print("[ASK BEC FLAG] target: %s" % target)
                if result is 0:
                    self.new_loc = target.strip()
                    print("[ASK BEC FLAG] new loc: %s" % self.new_loc)
                else:
                    self.new_loc = None

                print("[ASK_BEC FLAG] finished")

            elif verb == "ask_obj":
                # CMD***************
                # ask_obj OBJ cat *
                # ******************
                # self.new_obj updated
                # ******************
                print("[ASK_OBJ FLAG] start")

                config.pio.say("i think your command is incomplete \\pau=10\\ let me know object to get")

                while True:
                    target = config.pio.simple_stt()
                    for _, a in self.category_dict.items():
                        f = False
                        for b in a:
                            result = False
                            if b is "orange":
                                result = True

                            if b is "orange":
                                t = "orange juice".split()
                                for j in t:
                                    if not config.pio.find_word(j, source=target):
                                        result = False
                            if result:
                                f = True
                                b = "orange juice"
                                break

                            print(b)
                            result = True
                            t = b.split()
                            for j in t:
                                if not config.pio.find_word(j, source=target):
                                    result = False

                            if result:
                                f = True
                                break
                        if f:
                            break

                    if result:
                        target = "you say " + b
                        result = config.pio.hri.confirm_speech(target)
                        if result is 0:
                            target = b
                            break
                    
                    config.pio.say("please say again")

                self.new_obj = target

                print("[ASK_OBJ FLAG] finished")

            elif verb == "find_not":
                # CMD****************
                # find_not name bec *
                # *******************
                # self.ltarget
                # self.rtarget updated
                # *******************
                print("[FIND_NOT FLAG] start")
                

                # name is not in bec but in same room
                person_name = subtask_list[i][1] # self. needed?
                self.ltarget = subtask_list[i][2]

                self.rtarget = func.find_room_from_loc(self.ltarget)

                if self.rtarget is None:
                    print("[FIND_NOT ERROR] no room")
                    return StateResult.FAILURE

                config.pio.say("I cannot find you \\pau=20\\ I will go to the room")
                result = func.go_to_location(self.rtarget)

                config.pio.say("%s \\pau=20\\ I should find you \\pau=10\\ please wave your hand" % person_name)

                target = config.pio.search_target(target=["waving"], angle_range=[-60.0, 60.0], speed=0.05)

                self.find_person = target

                config.pio.say("I will go to you")
                result = config.pio.go_to_target_2018(target, thsld=[0.7, 1.2, 0.02], time_limit=10.0)

                print("[FIND_NOT FLAG] finished")

            elif verb == "error": # **********TODO: error cat name*************
                # CMD***************
                # error            *
                #       bec1 BEC2  *
                #       bec1 ROOM2 *
                #       obj NAME1  *
                #       cat NAME1  *
                # ******************
                # self.new_name
                # self.new_loc updated
                # ******************
                print("[ERROR FLAG] start")


                origin = subtask_list[i][1]
                cate = subtask_list[i][2] # 'NAME1', 'ROOM2', 'BEC2'

                config.pio.say("the command is wrong")
                find_list = None # name_list, room_list, beacon_list

                # cmd: error obj NAME1
                # cmd: error cat NAME1
                # e.g. error food NAME1
                if cate is 'NAME1':
                    config.pio.say("you should give me \\pau=10\\ person name \\pau=10\\ not %s" % origin)
                    config.pio.say("please tell me name")
                    find_list = self.name_list
                # cmd: error bec1 ROOM2
                elif cate is 'ROOM2':
                    config.pio.say("please give me \\pau=10\\ correct room except \\pau=20\\ %s" % origin)
                    config.pio.say("please tell me room")
                    find_list = self.room_list
                # cmd: error bec1 BEC2
                # e.g. error sink BEC2
                elif cate is 'BEC2':
                    config.pio.say("please give me \\pau=10\\ correct place except \\pau=20\\ %s" % origin)
                    config.pio.say("please tell me correct place")
                    find_list = self.beacon_list
                else:
                    print("wrong command")
                    config.pio.say("you give me \\pau=10\\ wrong command")
                    return StateResult.FAILURE

                tic = time.time()    
                dest = None
                target = None
                # get new information from the operator
                while time.time() - tic < 150: # timeout is 150
                    target = config.pio.simple_stt()
                    for b in find_list:
                        c = b.split()
                        result = True
                        for j in c:
                            if not config.pio.find_word(j, source=target):
                                result = False
                        if result:
                            break

                    if result:
                        target = "okay! got it! you say " + b
                        result = config.pio.hri.confirm_speech(target)
                        if result is 0:
                            target = b
                            break
                    config.pio.say("please say again")

                dest = target
                config.pio.say("Thank you")

                if cate is 'NAME1':
                    self.new_name = dest.strip()
                elif cate is 'ROOM2':
                    self.new_loc = dest.strip()
                elif cate is 'BEC2':
                    self.new_loc = dest.strip()

                print("[ERROR FLAG] finished")

        return StateResult.SUCCESS

    def exit_arena(self):
        config.pio.go_to_waypoint_2018(self.wp_exit)
        return StateResult.SUCCESS

    def go_to_operator(self):
        config.pio.say("I'm going to the operator")

        config.pio.navigation.reflex_going = True

        for i in range(8):
            config.pio.set_velocity(0.4, 0, 0, 1.0)

        config.pio.navigation.reflex_going = False

        while True :
            result = config.pio.go_to_waypoint_2018(self.wp_operator)
            if result is True :
                return StateResult.SUCCESS

    def log_time(self):
        if self.prev_state != self.state:
            time_elapsed = time.time() - self.prev_tic
            self.elapsed_times.append((self.prev_state, time_elapsed))
            self.logger.warning("{}: {:.3f}s".format(self.prev_state, time_elapsed))
            self.prev_state = self.state
            self.prev_tic = time.time()
            self.logger.warning("enter {}".format(self.state.name))
        elif self.state != State.INIT:
            self.logger.warning("redo {}".format(self.state.name))

    def transit_state(self, result, on_success, on_failure=None, on_interuppt=None,
                      on_skip=None, on_detour=None, on_debugging=None):
        if result == StateResult.SUCCESS:
            self.state = on_success
        elif result == StateResult.FAILURE:
            if on_failure is not None:
                self.state = on_failure
        elif result == StateResult.INTERRUPT:
            if on_interuppt is not None:
                self.state = on_interuppt
            else:
                self.logger.warning("{}: on_interrupt should be specified".format(self.state.name))
                raise ValueError
        elif result == StateResult.SKIP:
            if on_skip is not None:
                self.state = on_skip
            else:
                self.logger.warning("{}: on_skip should be specified".format(self.state.name))
                raise ValueError
        elif result == StateResult.DETOUR:
            if on_detour is not None:
                self.state = on_detour
            else:
                self.logger.warning("{}: on_detour should be specified".format(self.state.name))
                raise ValueError
        elif result == StateResult.DEBUGGING:
            if on_debugging is not None:
                self.state = on_debugging
            else:
                self.logger.warning("{}: on_debugging should be specified".format(self.state.name))
                raise ValueError
        elif result == StateResult.ABORT_TEST:
            self.logger.warning("abort test!")
            self.terminate()
        else:
            self.logger.error("unknown state result: {}".format(result))
            raise ValueError

    def set_viz_step(self,state):
        step = 0
        if state == State.INIT :
            step = 0
        elif state == State.GO_TO_OPERATOR :
            step = 1
        elif state == State.FIRST_COMMAND :
            step = 2
        elif state == State.FIRST_COMMAND_EXECUTE :
            step = 3
        elif state == State.SECOND_COMMAND :
            step = 4
        elif state == State.SECOND_COMMAND_EXECUTE :
            step = 5
        elif state == State.THIRD_COMMAND :
            step = 6
        elif state == State.THIRD_COMMAND_EXECUTE :
            step = 7
        elif state == State.EXIT_ARENA :
            step = 8
        config.pio.hri.publish_step(step)

    def run(self, state=State.INIT,categories=(3,3,3)):
        if state is not None:
            self.state = state
        self.prev_tic = time.time()
        self.start_time = self.prev_tic
        config.pio.hri.publish_story("GPSR",["READY"
                                           "GO TO OPERATOR",
                                           "GET FIRST COMMAND",
                                           "EXECUTE FIRST COMMAND",
                                           "GET SECOND COMMAND",
                                           "EXECUTE SECOND COMMAND",
                                           "GET THIRD COMMAND",
                                           "EXECUTE THIRD COMMAND"
                                           "EXIT ARENA",
                                          ])

        while not self.flag_terminate:
            self.log_time()
            self.set_viz_step(self.state)
            if self.state == State.INIT:
                self.transit_state(self.ready(),
                                   on_success=State.GO_TO_OPERATOR)
            elif self.state == State.GO_TO_OPERATOR :
                self.transit_state(self.go_to_operator(),
                                   on_success=State.FIRST_COMMAND)
            elif self.state == State.FIRST_COMMAND:
                self.transit_state(self.get_command(categories[0]),
                                   on_failure=State.FIRST_COMMAND,
                                   on_success=State.FIRST_COMMAND_EXECUTE)
            elif self.state == State.FIRST_COMMAND_EXECUTE:
                self.init_flag()
                try:
                    self.transit_state(self.exec_command(),
                                       on_failure=State.SECOND_COMMAND,
                                       on_success=State.SECOND_COMMAND)
                except:
                    self.state = State.SECOND_COMMAND
            elif self.state == State.SECOND_COMMAND:
                self.go_to_operator()
                self.transit_state(self.get_command(categories[1]),
                                   on_failure=State.THIRD_COMMAND,
                                   on_success=State.SECOND_COMMAND_EXECUTE)
            elif self.state == State.SECOND_COMMAND_EXECUTE:
                self.init_flag()
                try:
                    self.transit_state(self.exec_command(),
                                       on_failure=State.THIRD_COMMAND,
                                       on_success=State.THIRD_COMMAND)
                except:
                    self.state = State.THIRD_COMMAND
            elif self.state == State.THIRD_COMMAND:
                self.go_to_operator()
                self.transit_state(self.get_command(categories[2]),
                                   on_failure=State.THIRD_COMMAND,
                                   on_success=State.THIRD_COMMAND_EXECUTE)
            elif self.state == State.THIRD_COMMAND_EXECUTE:
                self.init_flag()
                try:
                    self.transit_state(self.exec_command(),
                                   on_failure=State.EXIT_ARENA,
                                   on_success=State.EXIT_ARENA)
                except:
                    self.state = State.EXIT_ARENA
            elif self.state == State.EXIT_ARENA:
                self.transit_state(self.exit_arena(),
                                   on_success=State.FINISHED)
            elif self.state == State.FINISHED:
                config.pio.say("Task finished.")
                break
            else:
                self.logger.error("unknown step number: {}".format(self.state.value))
                raise ValueError

        config.pio.stop()

        end_time = time.time()
        for s, t in self.elapsed_times:
            self.logger.info("{}: {:.3f}s".format(s.name, t))
        self.logger.info("==================")
        self.logger.info("total: {:.3f}s".format(end_time - self.start_time))
