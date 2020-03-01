#!/usr/bin/python2.7
import os
import sys

import xml.etree.ElementTree


sys.path.append("../../")
import pepper_config


# shared variables
params = None
pio = None


def get_pio_params():
    # TODO: customized config
    pio_params = pepper_config.load_config()
    pio_params["person_names"] = ["alex", "morgan", "michael", "taylor",
                                  "tracy", "jordan", "hayden", "peyton",
                                  "robin"]
    pio_params["nonstop_stt"] = False # True
    pio_params["hmc"] = True
    pio_params['show_integrated_perception'] = False

    return pio_params


class Params(object):

    debugging = False
    use_streaming = True

    time_limit = 600  # in seconds

    # TODO: pio params
    volume = 1.0
    voice_speed = 100
    # data_recording = True  # TODO: for real test
    data_recording = False

    # file_waypoint = 'robocup2018.txt'  # TODO: for real test
    file_waypoint = 'new_gpsr.txt'
    wp_operator = 'operator'
    wp_start = 'start'

    base_dir = os.path.dirname(__file__)
    xml_dir = os.path.join(base_dir, "cmd_gen")
    xml_gestures = "Gestures.xml"
    xml_locations = "Locations.xml"
    xml_names = "Names.xml"
    xml_objects = "Objects.xml"
    xml_questions = "Questions.xml"

    caption_filter = ['man', 'woman', 'person', 'shirt', 'jean', 'jacket', 'hair']

    gestures = []
    rooms = []
    locations = []
    names = []
    categories = []
    objects = []
    questions = []
    verbs = []
    command_words = []
    command_rep_list = []

    positives = ["yes", "yup", "yeah", "yeh", "yep", "yeap", "ya",
                 "that's it", "okay", "right", "correct"]
    negatives = ["no", "nah", "nope", "not",
                 "don't", "never", "wrong", "incorrect"]
    yes_or_no = positives + negatives

    def __init__(self, debugging=False):
        if debugging:
            self.debugging = True
            self.data_recording = False
            # self.file_waypoint = 'room409_fixed.txt'
        self.load_gestures()
        self.load_locations()
        self.load_names()
        self.load_objects()
        self.load_questions()

        # TODO: command_words
        # TODO: verbs

    def load_gestures(self):
        file_path = os.path.join(self.xml_dir, self.xml_gestures)
        root = xml.etree.ElementTree.parse(file_path)
        for gesture in root.findall('gesture'):
            gesture_name = gesture.get('name')
            gesture_difficulty = gesture.get('difficulty')
            self.gestures.append({
                'name': gesture_name,
                'difficulty': gesture_difficulty,
            })

    def load_locations(self):
        file_path = os.path.join(self.xml_dir, self.xml_locations)
        root = xml.etree.ElementTree.parse(file_path)
        for room in root.findall('room'):
            room_name = room.get('name')
            locs_in_room = []
            for loc in room.findall('location'):
                loc_name = loc.get('name')
                loc_is_beacon = loc.get('isBeacon') == 'true'
                loc_is_placement = loc.get('isPlacement') == 'true'
                self.locations.append({
                    'name': loc_name,
                    'room': room_name,
                    'is_beacon': loc_is_beacon,
                    'is_placement': loc_is_placement,
                })
                locs_in_room.append(loc_name)
            self.rooms.append({
                'name': room_name,
                'locations': locs_in_room,
            })

    def load_names(self):
        file_path = os.path.join(self.xml_dir, self.xml_names)
        root = xml.etree.ElementTree.parse(file_path)
        for name in root.findall('name'):
            # TODO
            self.names.append({
                'name': name.text,
                'gender': 'male',
            })

    def load_objects(self):
        file_path = os.path.join(self.xml_dir, self.xml_objects)
        root = xml.etree.ElementTree.parse(file_path)
        for cat in root.findall('category'):
            cat_name = cat.get('name')
            cat_default_location = cat.get('defaultLocation')
            cat_room = cat.get('room')
            objs_in_cat = []
            for obj in cat.findall('object'):
                obj_name = obj.get('name')
                obj_difficulty = obj.get('difficulty')
                obj_type = obj.get('type')
                obj_fruit = obj.get('fruit') == 'true'
                obj_alcoholic = obj.get('alcoholic') == 'true'
                obj_can_pour = obj.get('canPour') == 'true'
                obj_can_pour_in = obj.get('canPourIn') == 'true'
                obj_can_place_on = obj.get('canPlaceOn') == 'true'
                obj_can_place_in = obj.get('canPlaceIn') == 'true'
                obj_two_hands = obj.get('twoHands') == 'true'
                self.objects.append({
                    'name': obj_name,
                    'cat': cat_name,
                    'difficulty': obj_difficulty,
                    'type': obj_type,
                    'fruit': obj_fruit,
                    'alcoholic': obj_alcoholic,
                    'can_pour': obj_can_pour,
                    'can_pour_in': obj_can_pour_in,
                    'can_place_on': obj_can_place_on,
                    'can_place_in': obj_can_place_in,
                    'two_hands': obj_two_hands,
                })
                objs_in_cat.append(obj_name)
            self.categories.append({
                'name': cat_name,
                'default_location': cat_default_location,
                'room': cat_room,
                'objects': objs_in_cat,
            })

    def load_questions(self):
        file_path = os.path.join(self.xml_dir, self.xml_questions)
        root = xml.etree.ElementTree.parse(file_path)
        for question in root.findall('question'):
            q = question.find('q')
            if q is not None:
                q = q.text
            a = question.find('a')
            if a is not None:
                a = a.text
            self.questions.append({
                'q': q,
                'a': a,
            })


def main():
    p = Params()
    print("========= gestures ===========")
    print(p.gestures)
    print("========= rooms ===========")
    print(p.rooms)
    print("========= locations ===========")
    print(p.locations)
    print("========= names ===========")
    print(p.names)
    print("========= cats ===========")
    print(p.categories)
    print("========= objects ===========")
    print(p.objects)
    print("========= questions ===========")
    print(p.questions)


if __name__ == "__main__":
    main()
