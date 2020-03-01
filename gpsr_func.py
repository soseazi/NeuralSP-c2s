# -*- coding: utf-8 -*-
#!/usr/bin/python2.7

import gpsr_config as config
from nltk.translate.bleu_score import sentence_bleu
import time
import random


# TODO: remove bottles in drinks
category_dict = {
    "cleaning stuff": ["cloth", "scrubby", "sponge"],
    "containers": ["basket", "tray"],
    "cutlery": ["fork", "knife", "spoon"],
    "drinks": ["chocolate drink", "coke", "grape juice", "orange juice", "sprite", "bottle"],
    "food": ["cereal", "noodles", "sausages"],
    "snacks": ["crackers", "potato chips", "pringles"],
    "tableware": ["bowl", "cup", "dish"],
    "fruits": ["apple", "orange", "paprika"]
}


# TODO
category_location_dict = {
    "drinks": "counter",
    "cleaning stuff": "side table",
    "snacks": "bookcase",
    "fruits": "bookcase",
    "containers": "end table",
    "food": "cupboard",
    "cutlery": "storage table",
    "tableware": "storage table"
}

question_dict = {
    "Who invented the C programming language".lower(): "Ken Thompson and Dennis Ritchie.",
    "When was the C programming language invented".lower(): "C was developed after B in 1972 at Bell Labs",
    "When was the B programming language invented".lower(): "B was developed circa 1969 at Bell Labs",
    "Where does the term computer bug come from".lower(): "From a moth trapped in a relay",
    "Who invented the first compiler".lower(): "Grace Brewster Murray Hopper invented it",
    "Which robot is used in the Open Platform League".lower(): "There is no standard defined for OPL",
    "Which robot is used in the Domestic Standard Platform League".lower(): "The Toyota Human Support Robot",
    "Which robot is used in the Social Standard Platform League".lower(): "The SoftBank Robotics Pepper",
    "What's the name of your team".lower(): "...",
    "What time is it".lower(): "...",
    "What day is today".lower(): "...",
    "Do you have dreams".lower(): "I dream of Electric Sheep.",
    "In which city will next year's RoboCup be hosted".lower(): "It hasn't been announced yet.",
    "What is the origin of the name Canada.".lower(): "The name Canada comes from the Iroquois word Kanata, meaning village or settlement.",
    "What is the capital of Canada".lower(): "The capital of Canada is Ottawa.",
    "What is the national anthem of Canada".lower(): "O Canada.",
}

information_dict = {
    "something about yourself": "introduce",
    "the time": "time",
    "what day is today": "today",
    "what day is tomorrow": "tomorrow",
    "your teams name": "team_name",
    "your teams country": "team_country",
    "your teams affiliation": "team_affiliation",
    "the day of the week": "weekday",
    "the day of the month": "monthday",
    "a joke": "joke",
}

'''
location_dict = {
    "bedroom" : ["bed","night table","wardrobe","dresser","armchair","drawer","desk"],
    "dining room" : ["sideboard","cutlery drawer","dining table","chair","baby chair"],
    "living room" : ["bookshelf","sofa","coffee table","center table","bar","fireplace","tv couch"],
    "kitchen" : ["microwave","cupboard","counter","cabinet","sink","stove","fridge","freezer","washing machine","dishwasher"],
    "corridor" : ["cabinet"],
    "bathroom" : ["bidet","shower","bathtub","toilet","towel rail","bathroom cabinet","washbasin"]
}

room_list = ["bedroom","dining room","living room","kitchen","corridor","bathroom"]

placement_list = ["night table","wardrobe","dresser","drawer","desk","sideboard","cutlery drawer","dining table","bookshelf","sofa","coffee table","bar","fireplace","microwave","cupboard","counter","cabinet","sink","stove","fridge","freezer","washing machine","dishwasher","towel rail","bathroom cabinet","washbasin"]

beacon_list = ["bed","armchair","desk","dining table","chair","baby chair","sofa","coffee table","tv couch","sink","stove","cabinet","bidet","shower","bathtub","toilet","washbasin"]
'''

location_dict = {
    "corridor": ["entrance"],
    "bedroom": ["bed", "side table", "desk"],
    "dining room": ["dining table"],
    "living room": ["exit", "couch", "end table", "bookcase"],
    "kitchen": ["cupboard", "storage table", "sink", "counter", "dishwasher"],
}
room_list = ["corridor", "bedroom", "dining room", "living room", "kitchen"]
placement_list = ["side table", "desk", "dining table", "end table", "bookcase", "cupboard", "storage table", "sink", "counter"]
beacon_list = ["entrance", "bedroom", "desk", "dining table", "exit", "couch", "end table", "bookcase", "sink", "dishwasher", "bed"]

#  TODO: to lower case
#name_list = ["jamie","morgan","michael","taylor","tracy","jordan","hayden","peyton","robin","alex"]
name_list = ["alex", "charlie", "elizabeth", "francis", "jennifer", "linda", "mary", "patricia", "robin", "skyler", "james", "john", "michael", "robert", "william"]

gesture_list = ["waving","raising their left arm","raising their right arm","pointing to the left","pointing to the right"]

pose_list = ["sitting","standing","lying down"]

pgenders_list = ["man","woman","boy","girl","(male person)","(female person)"]

pgenderp_list = ["men","women","boys","girls","male","female"]

oprop_list = ["biggest","largest","smallest","heaviest","lightest","thinnest"]

gender_gesture_pose_list = gesture_list + pose_list + pgenders_list

'''
############### Navigation ###############
'''


def get_loc_from_obj(obj):
    room = None
    for i, j in category_dict.items():
        if obj in j:
            room = i

    loc = category_location_dict[room]

    return loc


# waypoint: predefined waypoint
def go_to_location(waypoint, say=True):
    if say is True:
        config.pio.hri.moving_to_waypoint(waypoint)
    while True:
        result = config.pio.go_to_waypoint_2018(waypoint, pass_doors=None)
        if result is True:
            return True
        elif result is -2:
            print("go_to_waypoint_2018 TIMEOUT; one more go_to_waypoint_2018")
            continue
        else:
            config.pio.logger.warning("bad result: " + str(result), "go_to_location")
            return False


# target: pepper_aupair object
# stop_word: stop signal
# destination: return False if final destination is not in intended_destination
def follow_person(target, stop_word=None, destination=None, pass_doors=None):
    if stop_word is not None :
        config.pio.say(("I will follow you, please call me, and say \\pau=200\\ stop \\pau=200\\ " +
                    "after the beep for stop following."), tag="Suggest")
    if destination :
        config.pio.say("I will follow you to " + destination)
    #result = config.pio.navigation.follow_person_2018_gpsr(target, stop_word=stop_word, pass_doors=pass_doors)
    result = config.pio.navigation.follow_person_2018(target, stop_word=stop_word, pass_doors=pass_doors)
    if result is True:
        if destination is not None and destination in config.pio.get_waypoints():
            dest_waypoint = config.pio.get_waypoints()[destination]
            dest_x = dest_waypoint[0]
            dest_y = dest_waypoint[1]
            dest_r = dest_waypoint[3]

            x, y, _ = config.pio.get_loc()[0]

            if config.pio.get_distance(x, y, dest_x, dest_y) > dest_r * 2:
                config.pio.logger.warning("bad result: not in " + destination, "follow_person")
                return False
        config.pio.say("stop following, thank you, have a nice day")
        return True
    else:
        config.pio.logger.warning("bad result: " + str(result), "follow_person")
        return False


# TODO: get tour guide function
def guide_person(waypoint, cat3=False, target=None) :
    config.pio.say("Please follow me.", tag="Raise_hand")
    if cat3:
        # TODO: turn around 180 and find person
        config.pio.rotate_in_degree(180)
        config.pio.say("%s \\pau=10\\ please follow me")
        config.pio.rotate_in_degree(180)
    return go_to_location(waypoint)


'''
############### Vision ###############
'''


def find_person_at_location(name=None,reid_target=None, find_again=True):
    if reid_target is not None:
        target = [reid_target.person_name]
    else:
        target = ["waving"]
    if name is not None:
        # config.pio.say(name + " \\pau=10\\ are you here?")
        # config.pio.say("if you are here, please waving your hand")
        config.pio.say("finding " + name)

    result = config.pio.search_target(target=target, angle_range=[-60.0, 60.0], speed=0.05)

    if result is not None:
        return result
    elif find_again:
        config.pio.rotate_in_degree(90, speed=0.5)
        result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.07)
        if result is None:
            config.pio.rotate_in_degree(-180, speed=0.7)
            result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.07)

            if result is None:
                config.pio.logger.warning("bad result: no target found.", "find_person_at_location")
                return False

        return result
    else:
        config.pio.logger.warning("bad result: no target found.", "find_person_at_location")
        return False


# find anyone
def find_person_anyone():
    target = ["person"]
    result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.07)
    if result is None:
        config.pio.rotate_in_degree(-180, speed=0.7)
        result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.07)

        if result is None:
            config.pio.logger.warning("bad result: no target found.", "find_person_at_location")
            return False
    return result


# feature: gender or pose
def recognize_feature(feature='gender'):
    target = config.pio.search_target(angle_range=[-60.0, 60.0], speed=0.03)
    if target is None:
        config.pio.logger.warning("bad result: no target found.", "recognize_feature")
        return False

    approach = config.pio.go_to_target_2018(target, thsld=[0.7, 1.2, 0.02], time_limit=10.0)

    person = config.pio.get_person(target.person_id)
    description = person.get_descriptions()
    print(description)
    if feature == 'gender':
        if condition_dict['male'](description):
            config.pio.say("I see a man!", tag="Raise_hand")
            return 'male'
        else:
            config.pio.say("I see a woman!", tag="Raise_hand")
            return 'female'

    elif feature == 'pose':
        if condition_dict['waving'](description):
            config.pio.say("A person is waving!", tag="Suggest")
            return 'waving'
        if 'lying' in description and description['lying'] > 0.6:
            config.pio.say("A person is lying!", tag="Suggest")
            return 'lying down'
        if 'pointing' in description and description['pointing'] > 0.6:
            config.pio.say("A person is pointing!", tag="Suggest")
            return 'pointing'
        else :
            config.pio.say("A person is not posing")
    else:
        config.pio.logger.warning("bad input: undefined feature.", "recognize_feature")


# constraint: gender or pose(gesture)
def find_by_constraint(constraint=('man'), find_again=False):
    say_string = ""
    for i in constraint:
        say_string += i
        say_string += " "
    config.pio.say("I will find person with %s \\pau=50\\" % say_string)
    targets = config.pio.search_all_people(head_trajectory=(-60.0, 60.0), speed=0.05, verbose=True)
    targets = ee2find(targets, constraint)

    if targets:
        return targets[0]
    elif find_again:
        config.pio.rotate_in_degree(90, speed=0.5)
        targets = config.pio.search_all_people(head_trajectory=(-60.0, 60.0), speed=0.05, verbose=True)
        if not targets:
            config.pio.rotate_in_degree(-180, speed=0.7)
            targets = config.pio.search_all_people(head_trajectory=(-60.0, 60.0), speed=0.05, verbose=True)

            if not targets:
                config.pio.say("sorry, i cant find " + constraint)
                config.pio.logger.warning("bad result: no target found.", "find_by_constraint")
                return False

        return targets[0]
    else:
        config.pio.say("sorry, i cant find " + constraint)
        config.pio.logger.warning("bad result: no target found.", "find_by_constraint")
        return False

    # approach = config.pio.go_to_target_2018(target, thsld=[0.7, 1.2, 0.02], time_limit=10.0)


# objcet_: target object
def find_object_at_location(object_, find_again=False):
    result = config.pio.search_target(target=[object_], angle_range=[-60.0, 60.0], speed=0.03)

    if result is not None:
        return result
    elif find_again:
        config.pio.rotate_in_degree(90, speed=0.5)
        result = config.pio.search_target(target=[object_], angle_range=[-90.0, 90.0], speed=0.05)
        if result is None:
            config.pio.rotate_in_degree(-180, speed=0.7)
            result = config.pio.search_target(target=[object_], angle_range=[-90.0, 90.0], speed=0.05)
            if result is None:
                config.pio.say("sorry, i cant find " + object_)
                config.pio.logger.warning("bad result: no target found.", "find_object_at_location")
                return False

        return result
    else:
        config.pio.say("sorry, i cant find " + object_)
        config.pio.logger.warning("bad result: no target found.", "find_object_at_location")
        return False


# category: target category
def find_category_at_location(category, find_again=False):
    target = category_dict[category]
    print(target)

    result = config.pio.search_target(target=target, angle_range=[-60.0, 60.0], speed=0.03)

    if result is not None:
        return result
    elif find_again:
        config.pio.rotate_in_degree(90, speed=0.5)
        result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.05)
        if result is None:
            config.pio.rotate_in_degree(-180, speed=0.7)
            result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.05)

            if result is None:
                config.pio.logger.warning("bad result: no target found.", "find_category_at_location")
                return False

        return result
    else:
        config.pio.logger.warning("bad result: no target found.", "find_category_at_location")
        return False


# category: target category
def find_multiple_objects_by_category(category, find_again=False):
    target = category_dict[category]

    results = config.pio.search_all_targets(target=target, angle_range=[-60.0, 60.0], speed=0.03)
    if results:
        return results
    elif find_again:
        config.pio.rotate_in_degree(90, speed=0.5)
        result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.05)
        if not result:
            config.pio.rotate_in_degree(-180, speed=0.7)
            result = config.pio.search_target(target=target, angle_range=[-90.0, 90.0], speed=0.05)

            if not result:
                config.pio.logger.warning("bad result: no target found.", "find_multiple_objects_by_category")
                return False

        return result
    else:
        config.pio.logger.warning("bad result: no target found.", "find_multiple_objects_by_category")
        return False


def count_people(find_again=False):
    targets = config.pio.search_all_people(head_trajectory=(-60.0, 60.0), speed=0.05, verbose=True)
    if targets:
        config.pio.say("Okay! I found {} people.".format(len(targets)), tag="Me")
    elif find_again:
        config.pio.rotate_in_degree(60, speed=0.5)
        targets = config.pio.search_all_people(head_trajectory=(-60.0, 60.0), speed=0.05, verbose=True)
        if not targets:
            config.pio.rotate_in_degree(-120, speed=0.7)
            targets = config.pio.search_all_people(head_trajectory=(-60.0, 60.0), speed=0.05, verbose=True)
            if not targets:
                config.pio.say("There is no person in here".format(len(targets)), tag="Me")
                return 0

        config.pio.say("Okay! I found {} people.".format(len(targets)), tag="Me")
    else:
        config.pio.say("There is no person in here".format(len(targets)), tag="Me")

    return len(targets)


def count_objects(object_, find_again=False):
    targets = config.pio.search_all_targets(target=[object_], angle_range=[-60.0, 60.0], speed=0.03)
    if targets:
        config.pio.say("Okay! I found {} objects.".format(len(targets)), tag="Me")
    elif find_again:
        config.pio.rotate_in_degree(60, speed=0.5)
        targets = config.pio.search_all_targets(target=[object_], angle_range=[-60.0, 60.0], speed=0.03)
        if not targets:
            config.pio.rotate_in_degree(-120, speed=0.7)
            targets = config.pio.search_all_targets(target=[object_], angle_range=[-60.0, 60.0], speed=0.03)
            if not targets:
                config.pio.say("There is no targets in here".format(len(targets)), tag="Me")
                return 0

        config.pio.say("Okay! I found {} targets.".format(len(targets)), tag="Me")
    else:
        config.pio.say("There is no targets in here".format(len(targets)), tag="Me")

    return len(targets)


def count_category(category, find_again=False):
    target = category_dict[category]
    targets = config.pio.search_all_targets(target=target, angle_range=[-60.0, 60.0], speed=0.03)
    if targets:
        config.pio.say("Okay! I found {} objects.".format(len(targets)), tag="Me")
    elif find_again:
        config.pio.rotate_in_degree(60, speed=0.5)
        targets = config.pio.search_all_targets(target=target, angle_range=[-60.0, 60.0], speed=0.03)
        if not targets:
            config.pio.rotate_in_degree(-120, speed=0.7)
            targets = config.pio.search_all_targets(target=target, angle_range=[-60.0, 60.0], speed=0.03)
            if not targets:
                config.pio.say("There is no targets in here".format(len(targets)), tag="Me")
                return 0

        config.pio.say("Okay! I found {} targets.".format(len(targets)), tag="Me")
    else:
        config.pio.say("There is no targets in here".format(len(targets)), tag="Me")

    return len(targets)


# category: target category
# ascending: False: biggest, True:smallest
# numbers: list length
def sort_category_by_size(category, ascending=False, numbers=1):
    target = category_dict[category]
    targets = config.pio.search_all_targets(target=target, angle_range=[-60.0, 60.0], speed=0.03)

    if len(targets) < numbers:
        config.pio.logger.warning("bad result: not enough objects found.", "sort_category_by_size")
        return False

    sorted_targets = sorted(targets, key=lambda x: (x.h * x.w), reverse=ascending)
    return sorted_targets[:numbers]


def sort_object_by_size(object_, ascending=False, numbers=1):
    target = object_
    targets = config.pio.search_all_targets(target=target, angle_range=[-60.0, 60.0], speed=0.03)
    if len(targets) < numbers:
        config.pio.logger.warning("bad result: not enough objects found.", "sort_category_by_size")
        return False

    sorted_targets = sorted(targets, key=lambda x: (x.h * x.w), reverse=ascending)
    return sorted_targets[:numbers]


'''
############### Speech ###############
'''


# target: person object. deault: None
def ask_name(pid=None):
    name = config.pio.hri.ask_name(greet=True, introduce=False, confirm=True, timeout=30)
    if pid is not None and name:
        config.pio.set_person_name(pid, name)
    return name


def reply_question(trial=3):
    config.pio.say("Do you have something to ask?")
    config.pio.say("I will answer you!", tag="Me")
    cand = config.pio.simple_stt()
    cand = cand.lower()
    cand_list = cand.split()

    max_score = 0.0
    question = ""
    for q in question_dict.keys():
        q_list = q.split()
        score = sentence_bleu([q_list], cand_list)

        if score > max_score:
            max_score = score
            question = q
        elif score == max_score:
            question = ""

    if not question:
        if trial == 1:
            config.pio.say("Sorry, I cannot understand you.", tag="Sorry")
            return False

        config.pio.hri.ask_again()
        return reply_question(trial-1)

    answer = question_dict[question]
    if answer == "...":
        if question == "What's the name of your team?":
            config.pio.hri.introduce_team()
        elif question == "What time is it?":
            config.pio.hri.current_time(time_of_day=True, month=False, day=False, year=False, weekday=False)
        else:  # question == "What day is today?":
            config.pio.hri.current_time(time_of_day=False, month=True, day=True, year=True, weekday=True)
    else:
        config.pio.hri.say("The answer is, ", tag="Thinking")
        config.pio.hri.say(answer, tag="Suggest")

    config.pio.right_arm_motion("release")
    return True


def tell_information(information):
    command = information_dict[information]

    if command == "introduce":
        config.pio.hri.introduce("pepper")
    elif command == "time":
        config.pio.hri.current_time(time_of_day=True, month=False, day=False, year=False, weekday=False)
    elif command == "today":
        config.pio.hri.current_time(time_of_day=False, month=True, day=True, year=True, weekday=True)
    elif command == "tomorrow":
        config.pio.hri.current_time(time_of_day=False, month=True, day=True, year=True, weekday=True, tomorrow=True)
    elif command == "team_name":
        config.pio.say("I am from team au pair", tag="Me")
    elif command == "team_country":
        config.pio.say("I am from South Korea", tag="Me")
    elif command == "team_affiliation":
        config.pio.say("Our team is from S N U", tag="Me")
    elif command == "weekday":
        config.pio.hri.current_time(time_of_day=False, month=False, day=False, year=False, weekday=True)
    elif command == "monthday":
        config.pio.hri.current_time(time_of_day=False, month=False, day=True, year=False, weekday=False)
    elif command == "joke":
        config.pio.say("I am pepper. But I'm not spicy.", tag="Me")
        config.pio.say("Sorry, I tried but it was not funny at all.", tag="Sorry")
    else:
        return None

    return True


def ask_something(something):
    config.pio.hri.randsay([
        "Sorry, I have some question to you.",
        "Can I ask something to you?",
        "I have some questions about it.",
         ], tag="Me")
    config.pio.hri.say(something)

    return config.pio.simple_stt()


# DELIVERY FUCNTIONS from SIKDANG


'''
def delivery_find_person(timeout1=120, timeout2=120):

    config.pio.say("Is there any person \\pau=20\\ to help me \\pau=20\\ to delivery foods?", tag="Raise_hand")
    config.pio.say("Please say \\pau=20\\ I will help you")

    config.pio.set_head_angle(horizontal=-119, speed=0.1, blocking=False)

    config.pio.speech.speech_final.clear()

    config.pio.set_volume(1.0)
    config.pio.say("Please help me!!!!!!")
    config.pio.say("please say \\pau=20\\ I will help you!")

    help_sign = False

    tic = time.time()
    while timeout1 > time.time() - tic:

        while timeout2 > time.time() - tic:
            help_sign = config.pio.speech.nonstop_find_word(["help", "hack", "hate"]) # TODO: what is the period
            config.pio.speech.speech_final.clear() # TODO? deque mutated erro

            if help_sign:
                break

            head_angle = config.pio.get_head_angle()

            if head_angle < -100:
                config.pio.set_head_angle(horizontal=110, speed=0.1, blocking=False)
            elif head_angle >= 100:
                config.pio.set_head_angle(horizontal=-110, speed=0.1, blocking=False)

        if help_sign is False:
            config.pio.say("okay \\pau=10\\ there is no person \\pau=10\\ to help me")
            return None

        config.pio.say("Could you help me?")
        config.pio.say("Please say yes!")
        config.pio.enable_head_fix(True)

        result = config.pio.hri.confirm_yesno()

        if result:
            config.pio.say("Thank you!")
            return "Angel" # find person: "Angel"
        else:
            continue

    config.pio.say("okay \\pau=10\\ there is no person \\pau=10\\ to help me")

    return None
'''
def delivery_find_person(timeout1=120, timeout2=120):

    config.pio.say("Is there any person \\pau=20\\ to help me \\pau=20\\ to delivery foods?", tag="Raise_hand")
    config.pio.say("Please say \\pau=20\\ I will help you")


    config.pio.set_volume(1.0)
    config.pio.say("Please help me!!!!!!")
    config.pio.say("please say \\pau=20\\ I will help you!")

    help_sign = False

    tic = time.time()
    while timeout1 > time.time() - tic:

        while timeout2 > time.time() - tic:
            help_sign = False
            answer = config.pio.simple_stt()
            if config.pio.find_word("help", answer):
                help_sign = True
            elif config.pio.find_word("hack", answer):
                help_sign = True
            elif config.pio.find_word("hate", answer):
                help_sign = True

            if help_sign:
                break

        if help_sign is False:
            config.pio.say("okay \\pau=10\\ there is no person \\pau=10\\ to help me")
            return None

        config.pio.say("Could you help me?")
        config.pio.say("Please say yes!")

        result = config.pio.hri.confirm_yesno()

        if result:
            config.pio.say("Thank you!")
            return "Angel" # find person: "Angel"
        else:
            continue

    config.pio.say("okay \\pau=10\\ there is no person \\pau=10\\ to help me")

    return None


def grab_bincan(drink, person_name="Hey", timeout=60):

    config.pio.say("%s please hand \\pau=20\\ me \\pau=20\\ in my hand \\pau=20\\ %s" % (person_name, drink)) # TODO
    config.pio.right_arm_motion("grab")

    tic = time.time()
    while time.time() - tic < timeout:

        config.pio.say("Are you finish? \\pau=10\\ please say yes or no!")
        result = config.pio.hri.confirm_yesno()

        if result:
            break
        else:
            config.pio.say("Okay \\pau=10\\ I will wait for you")
            continue

    config.pio.right_arm_motion("close")

    config.pio.arms_fix_while_walking()
    config.pio.say("thank you!")

    return True


def let_person_grab(drink=None, person_name="Hey", timeout=90):

    if drink is None:
        return -1

    config.pio.say("Now \\pau=10\\  please grab \\pau=20\\ %s" % drink)
    time.sleep(2.0)

    result = False

    tic = time.time()
    while time.time() - tic < timeout:
        config.pio.say("Are you finish? \\pau=10\\ Please say yes or no!")

        result = config.pio.hri.confirm_yesno()
        if not result:
            config.pio.say("I will wait for you")
            time.sleep(2.0)
            continue
        else:
            break

    if result is False:
        config.pio.say("I will go first")

    config.pio.say("Follow me!")

    return True


def person_delivery(first_say, timeout=90):

    config.pio.say(first_say)  # depends on "put" or "give"

    tic = time.time()
    while time.time() - tic < timeout:
        config.pio.say("Are you finish? \\pau=20\\ please say yes or no!")

        result = config.pio.hri.confirm_yesno()

        if result:
            break
        else:
            config.pio.say("I will wait for a second")
            time.sleep(2.0)
            continue

    config.pio.say("Thank you for your help")

    time.sleep(2.0)
    config.pio.say("then I will give the drink")

    delivery()

    return True


def delivery(timeout=60):
    config.pio.right_arm_motion("give")
    config.pio.say("Here")

    config.pio.say("please take this \\pau=20\\ when i open the hand")
    config.pio.right_arm_motion("open")

    tic = time.time()
    while time.time() - tic < timeout:

        config.pio.say("Are you finish? \\pau=10\\ please say yes or no!")
        result = config.pio.hri.confirm_yesno()

        if result:
            break
        else:
            config.pio.say("Okay \\pau=10\\ I will wait for you")
            continue

    config.pio.right_arm_motion("release")
    config.pio.arms_fix_while_walking(False, False)

    return True


def find_room_from_loc(loc):
    for r, l in location_dict.items():
        if loc in l:
            return r
    return None


"""
### EEGPSR functions
"""


def greet_person():
    config.pio.hri.greet_person()
    config.pio.hri.introduce()
    config.pio.say("Let's shake hands.", tag='Suggest')
    config.pio.right_arm_motion("handshake")
    time.sleep(5.0)
    config.pio.hri.thank_you()
    config.pio.right_arm_motion("release")


def describe_person(name):
    pid = config.pio.get_person_id_by_name(name)
    if pid is None:
        config.pio.hri.sorry_for("I don't know person named " + name)
        return False

    person = config.pio.get_person(pid)
    descriptions = person.get_sentence_descriptions()

    if len(descriptions) == 0:
        config.pio.say("Sorry, I cannot describe about {}".format(person.get_name()), tag="Sorry")
        return

    config.pio.say(descriptions[0], tag="Thinking")
    for d in descriptions:
        config.pio.say(d, tag="Suggest")
    config.pio.right_arm_motion("release")


# unused(maybe)
# def go_to_location_handling_crowds(waypoint):
#     config.pio.hri.moving_to_waypoint(waypoint)
#     while True:
#         result = config.pio.go_to_waypoint_2018(waypoint, pass_doors=None, check_person=True)
#         if result is True:
#             return True
#         elif result is -2:
#             print("go_to_waypoint_2018 TIMEOUT; one more go_to_waypoint_2018")
#             continue
#         elif result == -4 or result == -1 or result == -3:
#             config.pio.logger.warning("bad result: " + str(result), "go_to_location")
#             return False
#         else: # person detected
#             config.pio.say("Excuse me. Could you move out?")
def get_nearest_person():
    person_objs = config.pio.get_perception(['person'])
    valid_people = [p for p in person_objs.objects if p.valid_pose == 1]
    if not valid_people:
        return None
    return min(valid_people, key=lambda person: person.pose_wrt_robot.position.x)


def save_person(name):
    """Memorize the person."""
    person_id = config.pio.get_new_person_id(name)
    config.pio.enable_head_fix(vertical=-15)
    motion = "Gestures/ShowSky_7"

    config.pio.say("Let me remember you.", motion=motion)
    saved = False

    for i in range(3):
        config.pio.say("Please stand about two meters from me.")
        time.sleep(0.5)
        config.pio.say("Please keep turning around slowly for 5 seconds, starting from now.")

        config.pio.enable_head_fix(vertical=0)
        config.pio.right_arm_motion(motion="release")

        tic = time.time()
        while time.time() - tic < 5:
            person = get_nearest_person()
            if person:
                config.pio.add_person(person, person_id=person_id)
                time.sleep(0.15)
                saved = True

        if saved:
            break
        config.pio.say("Cannot find any person.")

    if saved:
        config.pio.hri.thank_you(politely=True)
        motion = "Emotions/Positive/Hysterical_1"
        config.pio.say("Let's go", motion=motion)
        return person_id
    else:
        config.pio.say("Failed to recognize person")
        return person_id


def guide_person_with_checking(waypoint, person_id, timeout=200.0):
    tic = time.time()
    track_period = 15.0

    while time.time() - tic < timeout:
        result = config.pio.go_to_waypoint_2018(waypoint, time_limit=track_period, verbose=False)

        if result is True:  # arrived
            return True
        else:
            if result == -1:  # goal invalid
                print("-1 goal invalid in guide_indoor func")
                return False
            elif result == -2:  # time out, need to check following well
                rotated_behind = False
                config.pio.look_behind(move_head=True, speed=0.8, look_front_again=False)
                time.sleep(0.5)
                tic2 = time.time()

                ask_flag = 0
                while time.time() - tic2 < timeout and ask_flag < 2:
                    ask_flag += 1
                    people = config.pio.get_perception([person_id]).objects
                    if len(people) == 0:
                        distance = 999
                    else:
                        distance = config.pio.get_distance(people[0].pose_wrt_robot.position.x,
                                                           people[0].pose_wrt_robot.position.y)

                    print(distance)
                    if distance < 3:
                        config.pio.say("Good. Keep following me.")
                        config.pio.look_behind(move_head=True, speed=0.8, look_front_again=True)
                        break
                    else:  # people is near
                        if not rotated_behind:
                            rotated_behind = True
                            head_angle = config.pio.get_head_angle()
                            config.pio.enable_head_fix()
                            config.pio.rotate_in_degree(-head_angle)

                        config.pio.say("I am here. please follow me.", tag="Raise_hand")
                else:
                    config.pio.say("Please follow me.", tag="Raise_hand")
                    time.sleep(0.5)
                    if rotated_behind:
                        config.pio.look_behind(move_head=False, speed=0.8, look_front_again=True)
                    else:
                        config.pio.look_behind(move_head=True, speed=0.8, look_front_again=True)

            elif result == -4:  # exception err
                print("-4 exception err in guide_indoor func")
                return False


condition_dict = {
    # main
    "child": lambda d: ('young' in d and d['young'] > 0.95),
    "male": lambda d: ('male' in d and d['male'] > 0.6),
    "female": lambda d: ('female' in d and d['female'] > 0.6),
    "both": lambda d: True,
    "young": lambda d: ('young' in d and d['young'] > 0.8),
    "old": lambda d: ('old' in d and d['old'] > 0.8),

    # color
    "blue shirts": lambda d: ('ucolor' in d and d['ucolor'] == "blue"),
    "yellow shirts": lambda d: ('ucolor' in d and d['ucolor'] == "yellow"),
    "black shirts": lambda d: ('ucolor' in d and d['ucolor'] == "black"),
    "white shirts": lambda d: ('ucolor' in d and d['ucolor'] == "white"),
    "red shirts": lambda d: ('ucolor' in d and d['ucolor'] == "red"),
    "gray shirts": lambda d: ('ucolor' in d and d['ucolor'] == "gray"),
    "orange shirts": lambda d: ('ucolor' in d and d['ucolor'] == "orange"),
    "blue pants": lambda d: ('lcolor' in d and d['lcolor'] == "blue"),
    "yellow pants": lambda d: ('lcolor' in d and d['lcolor'] == "yellow"),
    "black pants": lambda d: ('lcolor' in d and d['lcolor'] == "black"),
    "white pants": lambda d: ('lcolor' in d and d['lcolor'] == "white"),
    "red pants": lambda d: ('lcolor' in d and d['lcolor'] == "red"),
    "gray pants": lambda d: ('lcolor' in d and d['lcolor'] == "gray"),
    "orange pants": lambda d: ('lcolor' in d and d['lcolor'] == "orange"),

    # wearings
    "a hat": lambda d: ('wearing_hat' in d and d['wearing_hat'] > 0.3),
    "glasses": lambda d: ('eyeglasses' in d and d['eyeglasses'] > 0.3),
    "a necklace": lambda d: ('wearing_necklace' in d and d['wearing_necklace'] > 0.3),
    "a tie": lambda d: ('wearing_necktie' in d and d['wearing_necktie'] > 0.3),
    "earrings": lambda d: ('wearing_earrings' in d and d['wearing_earrings'] > 0.3),

    # pose
    "waving": lambda d: ('waving' in d and d['waving'] > 0.6),
    "raising their left arm": lambda d: ('lwaving' in d and d['lwaving'] > 0.6),
    "raising their right arm": lambda d: ('rwaving' in d and d['rwaving'] > 0.6),
    "pointing to the left": lambda d: ('lpointing' in d and d['lpointing'] > 0.6),
    "pointing to the right": lambda d: ('rpointing' in d and d['rpointing'] > 0.6),
    "lying down": lambda d: ('lying' in d and d['lying'] > 0.6),
    "sitting": lambda d: ('sitting' in d and d['sitting'] > 0.6),
    "standing": lambda d: ('sitting' in d and d['sitting'] < 0.4),
}

utmost_dict = {
    "tallest": lambda o: -o.x,
    "smallest": lambda o: o.x,
    "oldest": lambda d: (d['old'] if 'old' in d else 1 - d['young'] if 'young' in d else 0.5),
    "youngest": lambda d: (d['young'] if 'young' in d else 1 - d['old'] if 'old' in d else 0.5),
    "slimmest": lambda d: (d['skinny'] if 'skinny' in d else 1 - d['chubby'] if 'chubby' in d else 0.5),
    "fattest": lambda d: (d['chubby'] if 'chubby' in d else 1 - d['skinny'] if 'skinny' in d else 0.5),
}


def ee2find(person_objs, conditions=()):
    """"""
    """
    (child male female both young old)
    (male female both)
        (tallest smallest oldest youngest slimmest fattest)
        ("blue" | "yellow" | "black" | "white" | "red" | "gray" | "orange") , (u, l)
        ("a hat" | "glasses" | "a necklace" | "a tie" | "earrings")
    (male female both young old)
        ("standing" | "sitting" | "lying down")
        ( "shoes"| "pants" |"t-shirts" | "shirts" | "blouses" | "sweaters" | "coats" | "jackets")
        ("blue" | "yellow" | "black" | "white" | "red" | "gray" | "orange") and u, l
        ("waving" | "raising their " ("left" | "right") " arm" | "pointing to the " ("left" | "right"))
    'DESC'        # asked description
    'DESC'    name    # asked description + name
    """

    capt_result = []
    max_score = 0
    max_person = None

    for person_obj in person_objs:
        person = config.pio.get_person(person_obj.person_id)
        if person is None:
            capt_result.append(person)
        #TODO: enable_captioning
        description = person.get_descriptions(prob_threshold=0.3, face_num=10, banned_list=())
        for c in conditions:
            if c not in condition_dict or condition_dict[c](description):
                capt_result.append(person_obj)

    if conditions not in utmost_dict:
        return capt_result

    most = list(set(conditions) & set(utmost_dict.keys()))[0]

    for person_obj in capt_result:
        if most == "tallest" or most == "smallest":
            score = utmost_dict[most](person_obj)
            if score > max_score:
                max_person = person_obj
                max_score = score
        else:
            person = config.pio.get_person(person_obj.person_id)
            if person is None:
                continue
            description = person.get_descriptions(prob_threshold=0.3, face_num=10, banned_list=())

            score = utmost_dict[most](description)
            if score > max_score:
                max_person = person_obj
                max_score = score

    return max_person


def offer_foods(menu, find_again=False, conditions=()):
    targets = config.pio.search_all_people(head_trajectory=(-100.0, 100.0), speed=0.07, verbose=True)
    targets = ee2find(targets)

    if not targets:
        if find_again:
            config.pio.rotate_in_degree(60, speed=0.5)
            targets = config.pio.search_all_people(head_trajectory=(-100.0, 100.0), speed=0.07, verbose=True)
            if not targets:
                config.pio.rotate_in_degree(-60, speed=0.7)
                targets = config.pio.search_all_people(head_trajectory=(-100.0, 100.0), speed=0.07, verbose=True)
                if not targets:
                    config.pio.logger.warning("bad result: no target found.", "offer_foods")
                    return False
        else:
            config.pio.logger.warning("bad result: no target found.", "offer_foods")
            return False

    for t in targets:
        result = config.pio.go_to_target_2018(t, time_limit=40)
        if result is not True:
            config.pio.hri.sorry_for("I cannot approach to you. I will go to another guests")
            continue

        config.pio.start_tracking()
        config.pio.hri.greet_person()
        config.pio.say("Would you like something to eat or drink?", tag="Suggest")
        if config.pio.hri.confirm_yesno(3) == 1:
            config.pio.say("Great! I have", tag="Suggest")
            for m in menu:
                config.pio.say(m)
            config.pio.say("Which one do you prefer?")

            count = 3
            while count > 0:
                order = config.pio.simple_stt()
                if not order:
                    config.pio.hri.ask_again()
                    count -= 1
                else:
                    break
            else:
                config.pio.hri.got_it()

        else:
            config.pio.say("Okay. I will go to another guests", tag="Me")

    config.pio.say("Task finished!", tag="Raise_hand")
