
# coding: utf-8

import nltk
import pattern.en
import pepper_io
import numpy as np
import time
import pepper_config
import gpsr_examples
import datetime
import os

#entry_wp = 'entrance_outside'

global_timeout = 4*60
global_tic = time.time()

entry_wp = 'bedroom'
start_wp = 'bedroom'

#entry_wp = 'desk2'
#start_wp = 'desk2'


debug_mode = False
waypoint_file = 'final.txt'
data_recording = True

volume = 1.0
find_dist = 2.2 #3.3#2.2

last_talked_person = 'no one'
last_executed_command = 'nothing'
last_moved_obj = 'nothing'

# Name of object which is being frequently used
#obj_words_singular = ['cracker', 'juice', 'coke', 'cereal', 'milk', 'snack', 'chip', 'apple','drink','bottle','beverage','object','chair','mug','cup','table','beer','deodrant']
incomplete_obj_words = ['chewing', 'soup', 'fork', 'hair', 'cold', 'cup']

obj_words_singular = ['curry', 'plate', 'cleaner', 'shampoo', 'green tea', 'chewing gum', 'chopsticks', 'soup container', 'aquarius', 'fries', 'bowl', 'milk', 'candy', 'asience', 'fork Spoon', 'hair Spray', 'radish', 'apple', 'cold brew ', 'onion', 'corn', 'jelly', 'bread','cup star','orange','moisturizer','coke']
obj_words_plural = [pattern.en.pluralize(word) for word in obj_words_singular]
obj_words = obj_words_singular + obj_words_plural

#male_names = ['john', 'patrick', 'paul', 'joe', 'james']
#female_names = ['ana', 'mary']
male_names = ['noah', 'liam', 'mason', 'jacob', 'william', 'ethan', 'james', 'alexander', 'michael', 'benjamin']
female_names = ['emma', 'olivia', 'sophia', 'ava', 'isabella', 'mia', 'abigail', 'emily', 'charlotte', 'harper']
unknown_people = ['operator','girls', 'boys', 'people','them','girl', 'boy', 'man', 'woman', 'person']
people_words = male_names + female_names + unknown_people

thing_pronouns = ['it','them']
male_pronouns = ['he', 'him']
female_pronouns = ['she', 'her']
people_pronouns = male_pronouns+female_pronouns

question_dict = {
	'which' : 0,
	'team' : 1,
	'name': 1,
	'teams' : 2,
	'year':2,
	'participate' : 2,
	'vote' : 3,
	'popular' : 3,
	'u.s' : 3,
	'election':3,
	'highest':4,
	'mountain':4,
	'japan':4,
	'standard':5,
	'platforms':5,
	'two':5,
	'stand':6,
	'alphabet':7,
	'boston':7,
	'dynamic':7,
	'dynamics':7,
	'boston':7,
	'nagoya':8,
	'largest':8,
	'train':8,
	'station':8,
	'world':8,
	'large':8,
	'home':9,
	'star':10,
	'wars':10,
	'pineapple':11,
	'under':11,
	'sea':11,
	'grace':12,
	'hopper':12,
	'invent':12
}
answers = ['nagoya','au pair','31','hillary clinton','mount fuji','pepper and hsr', 'D S P L is domestic standard platform league, while S S P L is social standard platform league','softbank','over 410000 square metres','seoul','george lucas','sponge bob squarepants','the first compiler']


# Start words
start_words = ['tell', 'put', 'bring', 'count', 'follow','what',
				 'pour', 'go', 'meet', 'navigate', 'find','answer',
				 'look','search','identify','place', 'guide',
				 'describe', 'ask', 'take', 'locate', 'where',
				 'offer', 'hand', 'turn','name','give','say',
				 'greet','welcome','report','move','grasp','leave',
				 'introduce', 'escort', 'accompany','deliver','lead','pick','get','how','come','who','join']

'''
	if start_word in ['tell','ask','say','report']: func = tell
	elif start_word == 'count' or (start_word == 'how' and words[1] == 'many'): func = count
	elif start_word == 'follow': func = follow
	elif start_word == 'go' and words[1] == 'after': func = follow
	elif start_word == 'come' and words[1] == 'after': func = follow
	elif start_word in ['go', 'meet', 'move','come','navigate']: func = move
	elif start_word in ['find','look','search'] : func = find
	elif start_word in ['who','where'] : func=where
	elif start_word in ['guide', 'escort', 'accompany','lead']:func = guide
	elif start_word == 'describe':func = describe
	elif start_word in ['name','identify']:func = name_of_person
	elif start_word in ['greet','welcome']:func = greet
	elif start_word in ['grasp', 'offer', 'give', 'pour', 'put', 'place', 'hand', 'turn' ,'locate','deliver','pick','get']:func = manipulate
	elif start_word in ['take'] : func = take
	elif start_word == 'bring':func = bring
	elif start_word == 'leave':func = leave
	elif start_word == 'introduce':func = introduce
	elif start_word == 'answer' :func =  general_qa
	elif start_word in ['how', 'what']:
'''

actions = ['waving', 'standing' , 'sitting']
colors = ['red', 'green', 'blue', 'yellow', 'white', 'black']

# used for count function
special_countables = ['girls', 'boys', 'people']
sepical_findables = ['girl', 'boy', 'man', 'woman', 'person']

#incomplete_location_names = ['living', 'dining', 'bed', 'bath']
#complete_location_names = ['livingroom','diningroom','bedroom','bathroom','kitchen', 'door', 'enterance', 'gpsr_start_point']
#location_names = incomplete_location_names + complete_location_names

incomplete_location_names = ['little',
'entrance',
'coffee',
'bistro',
'left',
'right',
'balcony',
'kitchen','living']

'''
complete_location_names = ['bench',
'hallway table',
'bar',
'sidetable',
'kitchen table',
'kitchen counter',
'stove',
'bed',
'dresser',
'sideboard',
'bookshelf',
'pantry',
'cabinet',
'dinner table',
'couch table']
'''

location_names = ['desk',
'left rack',
'right rack',
'sideboard',
'kitchen table',
'little desk',
'teepee',
'bed',
'entrance shelf',
'kitchen shelf',
'bookcase',
'sofa',
'coffee table',
'tv',
'bistro table',
'left planks',
'left plank',
'right planks',
'right plank',
'balcony shelf',
'kitchen counter',
'fridge',
'kitchen rack','kitchen','living room','bedroom','balcony','entrance_outdoor','corridor'		 ]

search_loc = ['kitchen','living room','bedroom','balcony','corridor']

#location_names = incomplete_location_names + complete_location_names

prepositions = ['in', 'on', 'at','from','to']

interogatives = ['what','who','how','where','name']

all_words = obj_words + people_words + people_pronouns + start_words + actions + colors + special_countables + sepical_findables + location_names + prepositions + interogatives + question_dict.keys()

all_words = list(set(all_words))

def manipulate(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "manipulate()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	pio.say('i am sorry. i cannot manipulate objects')
	return True
	'''
	if len(obj) == 0 : return True

	#if target_object is None :
	#	result = find(obj=obj,location=location)
	#	if not result : return False

	pio.say('i cannot manipulate objects.')
	pio.say('is there anybody? please help me')
	result = find(person=['person'],location=location)
	if not result: return False

	pio.say('please')
	q = ''
	for w in query : q+=w ; q+=' '
	pio.say(q)
	return True
	'''
def move(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "move()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object

	if len(person)>0 or len(obj)>0 :
		print 'move : find instead move'
		result = find(person, obj, action, properties, location, query)
		if not result : return False
		#if target_found is not None and target_found.valid_pose == 1 :
		#	result = pio.approach( [target_found.pose_wrt_map.position.x, target_found.pose_wrt_map.position.y], 1.0 , True,True,30)
		return True
	if len(location) == 0 :
		print 'move : no target location'
		return True
	if current_location == location[0] :
		print 'move : already there'
		return True

	pio.say("moving to " + location[0])

	result = pio.go_to_waypoint(location[0],wait=True,clear_costmap=True,wait_timeout = 30)
	#result = pio.approach(pio.waypoints[location[0]][0:2],dist=0.3,wait=True,clear_costmap=True,timeout = 20,dist_inc=0.05)
	#if result : result = 0
	#else : result = None

	if result != 0 :
		print 'move : fail'
		return False
	
	current_location = location[0] ;
	print '[Move] current location = ' + current_location;
	pio.say('moved to ' + location[0] ) ;
	return True


def count(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "count()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object

	if len(location) > 0 :
		result = move(location=location)
		if not result : return False

	fil = person + obj + action + properties

	pio.say('start counting')

	num = 0
	for i in range(10):
		per = pio.get_perception()
		temp = 0
		for o in per.objects :
			if o.valid_pose == 0 or o.pose_wrt_robot.position.x > 2.3 : continue
			for f in fil :
				if f in o.tags : temp+=1
		if num < temp : num=temp
		time.sleep(0.3)

	pio.say('the count is ' + str(num))
	print 'count : anwser is ' + str(num)
	tell_content = 'the answer is ' + str(num)
	return True

def follow(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "follow()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object

	if target_found is None :
		result = find(person, obj, action, properties, location, query)
		if not result : return False

	target = target_found
	pio.say('i will follow you')
	pio.say('the time limit is 90 seconds.')
	pio.say('if you want me to stop, please say pepper, and say stop after beep')
	result = pio.follow_person(target,timeout=90,stop_criterion='speech',use_reid=True)
	pio.say('stop following')
	return result

def guide(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "guide()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object

	if target_found is None :
		result = find(person=[person[0]], action=action, properties=properties)
		if not result : return False

	if len(person) > 1 :
		if current_location is None : return False
		if person[-1] == 'operator' :
			location = ['gpsr_start_point']
		elif person[-1] in pio.waypoints.keys() :
			location = [person[-1]]



	location_ = location[:]
	if len(location_) == 1 :
		if current_location is None : return False
		location_.append(current_location)
		location_ = location_[::-1]

	print 'guide : ' , location_


	target = target_found

	pio.say('i will guide you to ' + location_[-1])
	pio.say('please follow me')
	tic = time.time()
	last_ask = time.time()
	ask_flag = 0 #no checking in gpsr guiding
	mci = 0
	while time.time()-tic < 40 :
		if mci % 4 == 0 : pio.map_clear_srv()
		mci+=1
		result = pio.go_to_waypoint(location_[-1],clear_costmap=True,wait_timeout=3.0)
		if result == 0 : pio.say('finish guiding') ; return True
		if time.time()-last_ask > 25 and ask_flag == 0 :
			pio.stop()
			pio.rotate_in_radian(np.pi)
			time.sleep(1)
			tic2 = time.time()
			ok_flag = False
			while time.time() - tic2 < 30 :
				people = pio.get_perception(['person']).objects
				min_dis = 9999999
				for p in people :
					if p.valid_pose == 1	: min_dis = p.pose_wrt_robot.position.x
				if min_dis < 2 : pio.say('good. keep following me.') ; ok_flag = True ; break
				pio.say('i am here. follow me. let me see you in my sight. closer than 2 meters')
				time.sleep(1)
			if not ok_flag :
				return False
			pio.rotate_in_radian(-np.pi)
			last_ask = time.time()
			ask_flag = 1
	return False


def find(person=[],obj=[],action=[],properties=[],location=[],query=[]): #TODO gender, objects? , add tags to find_target
	print "find()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True

	global tell_content
	global current_location
	global target_found ; global target_object
	global people_words
	global find_dist
	global search_loc
	global male_names,female_names,last_talked_person,last_moved_obj

	if len(person) > 0 and person[0]=='operator' : return move(location=['gpsr_start_point'])

	fil = []
	talk_target, talk_action = 'person',''
	talk_ = ''
	if len(person)>0 :
		fil = fil + person
		talk_target = person[0]
		if person[0] in male_names + female_names :
			fil=['waving']
			talk_ = person[0] + ', where are you? please come in front of me about 2 meters away and wave your hand!'
		else :
			talk_ = 'finding ' + person[0]
	if len(properties) > 0 : #convert color to color_cloth
		fil = properties
		talk_ = 'finding ' + properties[0]
	if len(obj) > 0 : fil = obj ; talk_ = 'finding ' + obj[0]
	if len(action)>0 : fil = action ; talk_ =  'finding ' + action[0]
	print '[find] ' , fil
		
	if 'male' in query : fil = ['man']	
	if 'man' in query : fil = ['man']	
	if 'female' in query : fil = ['woman']	
	if 'woman' in query : fil = ['woman']			
	if 'girls' in query : fil = ['woman']	
	if 'boys' in query : fil = ['man']	
	if 'boy' in query : fil = ['man']	
	if 'girl' in query : fil = ['woman']			
		
	print 'find : ' , talk_

	if len(location) == 0 and current_location != 'gpsr_start_point' : location = [current_location]
	
	if len(location) == 0 :
		pio.say('location is not given.')
		pio.say('find tartget in all rooms')
		if len(fil)>0 and fil[0] in pio.waypoints.keys() : _location = [  fil[0]  ]
		else :
			_location = []
			for wp in pio.waypoints.keys():
				if wp in people_words or wp not in search_loc : continue
				flag = True
				for wwpp in location :
					if (wp[0]-wwpp[0])**2 + (wp[1]-wwpp[1])**2 < 1.0 : flag = False
				if flag : _location.append(wp)
	else : _location = [location[0]]

	print 'find : ' , _location

	dists = np.zeros(len(_location))
	for l in range(  len( _location) ) :
		dists[l] = (pio.waypoints[_location[l]][0]-pio.position[0])**2 \
		+(pio.waypoints[_location[l]][1]-pio.position[1])**2

	ranked = np.argsort(dists)
	print 'find : ' , ranked

	for i in ranked :
		loc = _location[i]
		result = move(location=[loc])
		if not result : return False
		#result = pio.find_target(fil,talk=talk_,timeout=30,speed=0.2,direction_change=False,direction_change_interval=5,dist_limit = find_dist)
		result = pio.find_target(fil,talk=talk_,timeout=30,speed=0.1,direction_change=True,direction_change_interval=2,dist_limit =find_dist,waypoint_ignore=['spectators','commitee_table'],wp_ignore_dist=2.6,waypoint_only=[loc],only_dist=2,allow_unknown = False)

		if result is not None :
			if result.class_string == 'person' :
				target_found = result ;
				target_found.person_name = 'person'
				if len(fil)>0 and target_found.class_string == 'person' :
					if len(person)>0 :
						if person[0] in male_names+female_names :
							target_found.person_name = person[0]
						else :
							name_of_person()
						pio.add_reid_target(200, target_found.person_name, img=None, person_obj=target_found )
							
					if fil[0] != 'operator' :
						pio.add_waypoint(target_found.person_name)
				last_talked_person = target_found.person_name				

			else :
				target_object = result
				last_moved_obj = result.class_string

			#pio.approach( [ result.pose_wrt_map.position.x , result.pose_wrt_map.position.y ] , 1.0 , wait=True, clear_costmap=True, timeout = 15)
			return True
	return False


def describe(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "describe()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	global male_names
	global female_names
	global obj_words
	global actions
	global colors

	target = None
	if len(location) > 0 : move(location=location)

	if target_found is not None : target = target_found
	elif len(person)>0 and len(obj)>0:
		result = find(person, obj, action, properties, location, query)
		if not result : return False
		target = target_found

	if target is None :
		tell_content = ''
		cap = pio.get_captions()
		limit = min(5,len(cap))
		for i in range(limit) :
			pio.say(cap[i])
			tell_content += cap[i] + ' '
	else :
		captions = target.captions
		for w in captions :
			pio.say(w)

	if len(person) > 1 :
		if person[-1] == 'operator' :
			result = move(location=['gpsr_start_point'])
			if not result : return False
			pio.say(tell_content)
		else :
			result = find(person=[person[-1]])
			if not result : return False
			pio.say(tell_content)

	return True


def person_action(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "person_action()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global target_found ; global target_object
	global actions
	global tell_content
	global all_words

	result = find(person, obj, action, properties, location, query)
	if not result : return False

	tic1 = time.time()
	while time.time()-tic1 < 60 :
		pio.say('what are you doing?')
		pio.say('please tell me after beep')
		pio.speech_hints = all_words
		answer = pio.start_recording(reset=True, base_duration=3.0)
		pio.say(answer)
		pio.say('am i correct? please say yes or no, after beep')
		pio.speech_hints = ['yes','no']
		answer2 = pio.start_recording(reset=True, base_duration=3.0)
		if pio.find_word('yes',answer2) :
			pio.say('okay')
			tell_content = answer
			return True
		else :
			pio.say('please tell again')
	return False

def name_of_person(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "name_of_person()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	if target_found is None : 
		result = find(person, obj, action, properties, location, query)
		if not result : return False

	tic1 = time.time()
	while time.time()-tic1 < 60 :
		pio.say('what is your name?')
		pio.say('please come and tell me one second after beep')
		time.sleep(3)
		pio.speech_hints = male_names + female_names
		answer = pio.start_recording(reset=True, base_duration=3.0)
		for n in (male_names + female_names):
			if pio.find_word(n,answer) : 
				pio.say('okay') ; 
				tell_content = 'the name is ' + n ; 
				if target_found is not None : 
					target_found.person_name = n
				return True
		pio.say('please tell me again')
	return False


def tell(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "tell()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object

	target = None

	if len(person)>0 :
		if person[0] == 'operator' :
			result = move(location=['gpsr_start_point'])
			if not result : return False
		else :
			if target_found is not None and target_found.person_name == person[0] :
				print 'target already found'
			else :
				result = find(person, obj, action, properties, location, query)
				if not result : return False

	if tell_content == 'nothing to tell' :
		if 'time' in query  :
			now = datetime.datetime.now()
			nowstr = now.strftime("%H %M %B %d %Y")
			pio.say(nowstr)
			return True	
		elif 'joke' in query:
			pio.say('the best place to hide a body is the second page of a google search')
			return True
		elif 'yourself' in query:
			pio.say('Hello! I am Aupair.')
			pio.say('I came from Seoul National University')
			pio.say('Nice to meet you')
			return True	
		elif 'affiliation' in query:
			pio.say('I came from Seoul National University')
			return True
		elif 'week' in query  :
			now = datetime.datetime.now()
			nowstr = now.strftime("%A")
			pio.say(nowstr)
			return True
		elif 'month' in query  :
			now = datetime.datetime.now()
			nowstr = now.strftime("%d")
			pio.say(nowstr)
			return True
		elif 'tomorrow' in query  :
			now = datetime.date.today() + datetime.timedelta(days=1)
			nowstr = now.strftime("%B %d %Y")
			pio.say(nowstr)
			return True
		print query
		q = ''
		for w in query : q+=w ; q+=' '
		pio.say(q)
	else :
		if 'time' in tell_content  :
			now = datetime.datetime.now()
			nowstr = now.strftime("%H %M %B %d %Y")
			pio.say(nowstr)
			return True	
		elif 'joke' in tell_content:
			pio.say('the best place to hide a body is the second page of a google search')
			return True
		elif 'yourself' in tell_content:
			pio.say('Hello! I am Aupair.')
			pio.say('I came from Seoul National University')
			pio.say('Nice to meet you')
			return True	
		elif 'affiliation' in tell_content:
			pio.say('I came from Seoul National University')
			return True
		elif 'week' in tell_content  :
			now = datetime.datetime.now()
			nowstr = now.strftime("%A")
			pio.say(nowstr)
			return True
		elif 'month' in tell_content  :
			now = datetime.datetime.now()
			nowstr = now.strftime("%d")
			pio.say(nowstr)
			return True
		elif 'tomorrow' in tell_content  :
			now = datetime.date.today() + datetime.timedelta(days=1)
			nowstr = now.strftime("%B %d %Y")
			pio.say(nowstr)
			return True
		print tell_content
		pio.say(tell_content)
	return True

def bring(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "Bring()"
	print person, obj, action, properties, location, query

	if len(person) > 1 : print 'bring : reroute to guide' ; return guide(person, obj, action, properties, location, query)

	if len(obj)>0 : print 'bring : reroute to manipulate' ; return manipulate(person, obj, action, properties, location, query)

	return True

def general_qa(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "general_qa()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object ; global question_dict ; global answers
	global last_talked_person
	global last_executed_command 
	global last_moved_obj 	
	if 'time' in query :
		now = datetime.datetime.now()
		nowstr = now.strftime("%H %M %B %d %Y")
		query[ query.index('time') ] = nowstr
		q = ''
		for w in query : q+=w ; q+=' '
		pio.say(q)
		return True
	
	else :
		timeout = 60
		pio.say('say pepper,')
		pio.say('and give me the question after the beep')
		tic = time.time()
		pio.speech_memory = ''
		ques = ''
		pio.speech_hints = question_dict.keys() + ['command','object','person']
		while time.time()-tic < timeout :
			ques = ''
			pio.speech_memory = ''
			while ques == '' :
				ques = pio.speech_memory
				
			if 'command' in ques.split(' ') : pio.say(last_executed_command) ; return True
			if 'object' in ques.split(' ') : pio.say(last_moved_obj) ; return True
			if 'person' in ques.split(' ') : pio.say(last_talked_person) ; return True
				
			for w in ques.split(' ') :				
				if w in question_dict.keys() :
					pio.say(answers[question_dict[w]])
					pio.say('done')
					return True
			pio.say('please ask again')
	return None


def where(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "where()"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	result = find(person, obj, action, properties, location, query)
	if not result : return False
	tell_content = current_location
	return True

def greet(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "greet"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	if target_found is None :
		result = find(person, obj, action, properties, location, query)
		if not result : return False
	pio.say('Hi! welcome to my home')
	return True

def take(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "greet"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	if len(person) > 0 : 
		print '[take] reroute to guide'
		return guide(person, obj, action, properties, location, query)
	else : 
		print '[take] reroute to mani'
		return manipulate(person, obj, action, properties, location, query)
		

def leave(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "leave"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	return move(location=['exit'])

def introduce(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "introduce"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object

	if len(person) > 0 :
		if target_found is None:
			result = find(person, obj, action, properties, location, query)
			if not result : return False

	pio.say('Hello! I am Aupair.')
	pio.say('I came from Seoul National University')
	pio.say('Nice to meet you')
	return True

def dark_side(person=[],obj=[],action=[],properties=[],location=[],query=[]):
	print "dark_side"
	print person, obj, action, properties, location, query
	global debug_mode
	if debug_mode : return True
	global tell_content
	global current_location
	global target_found ; global target_object
	
	pio.say('i am your father')
	return True
	


def to_str(words):
	return reduce(lambda x, y: x +' '+ y, words)

def convert(words):
	global tell_content
	
	start_word = words[0]
	op_or = lambda x, y: x or y

	words_ = words[:]
	i = 0
	person = []
	obj = []
	properties = []
	location = []
	action = []
	while i < len(words) :
		if words[i] in prepositions : del words[i] ; continue
		if words[i] in people_words : person.append( words[i] )
		if words[i] in obj_words : 
			obj.append(words[i])			
			last_moved_obj = words[i]
						
		if words[i] in incomplete_obj_words:
			if i + 1 < len(words):
				word_with_blank = words[i] + ' ' + words[i+1]
				word_without_blank = words[i] + words[i+1]
				if word_with_blank in obj_words : 
					obj.append(word_without_blank)
					#i += 1
					i += 2
					continue
			
		'''
		if words[i] in location_names :
			if words[i] in incomplete_location_names : location.append( words[i] + ' room')
			else : location.append( words[i])
		'''
		'''
		if words[i] in location_names :
			if words[i] in incomplete_location_names :
				location.append( words[i] + ' table')
			else :
				location.append( words[i])
		'''
		'''
		if words[i] in location_names : location.append(words[i])

		if words[i] in incomplete_location_names:
			if i + 1 < len(words):
				word_with_blank = words[i] + ' ' + words[i+1]
				if word_with_blank in location_names:
					location.append(word_with_blank)
					i += 1
					
		for i1 in range(  len(words)  ) :
			for i2 in range( len(location_names) ):
				ln_sp = location_names.split(' ')
				if i1 + len(ln_sp) - 1 < len(words) :
					for i3 in range( len(ln_sp) ) :
		'''
		loc_flag = True
		if words[i] in incomplete_location_names:
			if i + 1 < len(words):
				word_with_blank = words[i] + ' ' + words[i+1]
				if word_with_blank in location_names:
					location.append(word_with_blank)
					loc_flag = False
					i += 2
					continue
					
		if words[i] in location_names and loc_flag: location.append(words[i])
					
		if words[i] in colors : properties.append(words[i])
		if words[i] in actions : action.append(words[i])
		i+=1

	# get query
	query = words[1:]

	# get function
	func = None
	if start_word in ['tell','ask','say','report']: func = tell
	elif start_word == 'count' or (start_word == 'how' and words[1] == 'many'): func = count
	elif start_word == 'follow': func = follow
	elif start_word == 'go' and words[1] == 'after': func = follow
	elif start_word == 'come' and words[1] == 'after': func = follow
	elif start_word in ['go', 'meet', 'move','come','stand','navigate']: func = move
	elif start_word in ['find','look','search','locate'] : func = find
	elif start_word in ['who','where'] : func=where
	elif start_word in ['guide', 'escort', 'accompany','lead']:func = guide
	elif start_word == 'describe':func = describe
	elif start_word in ['name','identify']:func = name_of_person
	elif start_word in ['greet','welcome']:func = greet
	elif start_word in ['grasp', 'offer', 'give', 'pour', 'put', 'place', 'hand', 'turn' ,'deliver','pick','get']:func = manipulate
	elif start_word in ['take'] : func = take
	elif start_word == 'bring':func = bring
	elif start_word == 'leave':func = leave
	elif start_word == 'introduce':func = introduce
	elif start_word == 'answer' :func =  general_qa
	elif start_word == 'join' :func =  dark_side
	elif start_word in ['how', 'what']:
		if words[-1] == 'doing':
			func = person_action
		else:
			func = general_qa
	else: func = general_qa

	if func is not None :
		return func(person,obj,action,properties,location,query)
	else : return False



def parse(words):
	global interogatives
	global people_words
	global start_words
	global tell_content
	global global_tic , global_timeout
	tell_content = 'nothing to tell'
	print 'parsing : ' , words

	start_word_locations = []
	commands = []
	i = 0
	while i < len(words):
		if words[i] == 'and' or words[i] == 'then' :
			del words[i] ; continue
		if words[i] in start_words :
			start_word_locations.append(i)
		i+=1

	start_word_locations.append(len(words))

	for i in range( len(start_word_locations) -1 ) :
		commands.append(words[ start_word_locations[i] : start_word_locations[i+1] ])

	i = 0
	while i < len(commands):
		if commands[i][0] == 'tell' or commands[i][0] == 'ask' or commands[i][0] == 'say' :
			if i != len(commands)-1 and commands[i+1][0] in interogatives :
				temp = commands[i+1]
				commands[i+1] = commands[i]
				commands[i] = temp
			elif len(commands[i]) == 2 or ( len(commands[i])==3 and commands[i][1] in people_words and commands[i][2]=='to') :
				if i != len(commands)-1 :
					tell_content = ''
					for ww in commands[i+1]:
						tell_content += ww + ' '
					del commands[i+1]
		i+=1

	for c in commands : print c
	print tell_content


	for c in commands:
		trial = 0
		while trial < 5 and time.time() - global_tic < global_timeout :
			result = convert(c)
			if result : break
			trial += 1
			
		if time.time() - global_tic >= global_timeout : 
			print '[EEGPSR] timeout -> return to start point'

	return None



def infer_it(words):
	for obj_word in obj_words:
		if obj_word in words:
			return obj_word
	return None

def infer_him(words):
	for male_name in male_names:
		if male_name in words:
			return male_name
	return None

def infer_her(words):
	for female_name in female_names:
		if female_name in words:
			return female_name
	return None


def process_command(command, erroneous=False):
	global obj_words_plural
	global location_names
	global people_pronouns
	words = nltk.word_tokenize(command)
	words_new = []
	for w in words :
		ww = w
		if w == 'tp' : ww = 'teepee'
		if w == 'plank' : ww = 'planks'
		words_new.append(ww)
	words = words_new
	
	words = [word for word in words if word != 'a' and word != 'the']
	or_op = lambda x, y: x or y

	if reduce(or_op, [pronoun in words for pronoun in thing_pronouns]):
		inferred_obj = infer_it(words)
		if inferred_obj is not None:
			for pronoun in thing_pronouns:
				while pronoun in words:
					words[words.index(pronoun)] = inferred_obj

	if reduce(or_op, [pronoun in words for pronoun in male_pronouns]):
		inferred_his_name = infer_him(words)
		if inferred_his_name is not None:
			for pronoun in male_pronouns:
				while pronoun in words:
					words[words.index(pronoun)] = inferred_his_name

	if reduce(or_op, [pronoun in words for pronoun in female_pronouns]):
		inferred_her_name = infer_her(words)
		if inferred_her_name is not None:
			for pronoun in female_pronouns:
				while pronoun in words:
					words[words.index(pronoun)] = inferred_her_name

	for i in range(len(words)) :
		if words[i] in obj_words_plural : words[i] = pattern.en.singularize(words[i])
		if words[i] == 'there' :
			for w in words :
				if w in location_names : words[i] = w ; break
		if words[i] == 'me' : words[i] = 'operator'
		if words[i] == 'here' : words[i] = 'gpsr_start_point'
		if words[i] == 'you' : words[i] = 'this robot'
		if words[i] in people_pronouns and 'person' in words : words[i] = 'person'
		if words[i] in people_pronouns and 'people' in words : words[i] = 'people'

		#TODO comma?
	parse(words)

def test(commands):
	for command in commands:
		print '-' * 50
		print command
		process_command(command)


# In[4]:
tell_content = 'nothing to tell'
current_location = None
target_found = None
target_object = None
count_result = 0
'''
print '##################################'
print '##########    G P S R ############'
print '##################################'
examples = gpsr_examples.load_examples()
for cmd in examples :
	print '### cmd : ' , cmd
	process_command(cmd)

raise ValueError
'''

pio = pepper_io.pepper_io(pepper_config.load_config())
pio.set_volume(volume)
pio.tts.setParameter("defaultVoiceSpeed", 100)

##
# keyboard control for debugging
pio.load_waypoints(waypoint_file)
pio.activate_keyboard_control()
pio.init_speech_recognition(0.6)
if data_recording : pio.start_data_recording()
'''
pio.say("i am ready. please open the door.")
time.sleep(5)
'''
pio.set_static_map(True)
pio.set_initial_pose_wp(entry_wp,0.006,-0.006)
pio.map_clear_srv()

'''
result = 1
while result != 0 :
	#result = pio.approach(pio.waypoints[start_wp][0:2],dist=0.3,wait=True,clear_costmap=True,timeout = 10,dist_inc=0.05)
	result = pio.go_to_waypoint(start_wp,wait=True,clear_costmap=True,wait_timeout = 10)
pio.map_clear_srv()
'''
global_tic = time.time()


'''
#Test
while  True :
	last_talked_person = open('last_person.txt','r').readlines()[0]
	last_executed_command = open('last_cmd.txt','r').readlines()[0]
	last_moved_obj = open('last_obj.txt','r').readlines()[0]
	pio.clear_reid_targets()
	pio.load_waypoints(waypoint_file,say=False)
	pio.add_waypoint('gpsr_start_point')
	location_names += pio.waypoints.keys()
	romm_names = list(set(location_names))
	tell_content = 'nothing to tell'
	current_location = 'gpsr_start_point'
	target_found = None
	target_object = None
	cmd = raw_input('cmd : ' )
	lastcmd_f = open('last_cmd.txt','w')
	lastcmd_f.write(cmd)
	lastcmd_f.flush()
	lastcmd_f.close()
	if cmd =='exit' : raise ValueError
	result = process_command(cmd.encode('ascii','ignore'))
raise ValueError
'''

cmd_cnt = 0

while cmd_cnt < 100 :
	#if cmd_cnt != 0 : pio.say('erasing previous command')
	pio.clear_reid_targets()
	pio.load_waypoints(waypoint_file,say=False)
	pio.add_waypoint('gpsr_start_point')
	location_names += pio.waypoints.keys()
	romm_names = list(set(location_names))
	tell_content = 'nothing to tell'
	current_location = 'gpsr_start_point'
	target_found = None
	target_object = None

	go_flag = 0
	all_words = obj_words + people_words + people_pronouns + start_words + actions + colors + special_countables + sepical_findables + incomplete_location_names  + location_names + prepositions + interogatives
	pio.speech_hints = all_words
	pio.say('say pepper. And give a command one second after beep')
	pio.speech_memory = ''
	cmd = ''
	got_cmd_flag = False
	while not got_cmd_flag : 
		pio.speech_memory = ''
		cmd = ''
		tic = time.time()
		while time.time() - tic < 30 and cmd == '' :
			cmd = pio.speech_memory
		if cmd != '' : got_cmd_flag = True


	pio.say('the exact command is')
	pio.say(cmd)
	pio.say('am i correct? please say pepper and say yes or no, one second after beep')
	pio.speech_hints = ['yes','no']
	
	pio.speech_memory = ''
	answer = ''
	
	got_yn_flag = False
	while not got_yn_flag : 
		pio.speech_memory = ''
		answer = ''
		tic = time.time()
		while time.time() - tic < 30 and answer == '' :
			answer = pio.speech_memory
		if pio.find_word('yes',answer) : 
			pio.say('okay') ; go_flag = 1
			got_yn_flag = True	
		elif pio.find_word('no',answer) :
			pio.say('sorry') ; go_flag = 0
			got_yn_flag = True
		else : 
			pio.say('please say yes or no again')

	if go_flag == 0 : continue
	print 'cmd : ' , cmd.encode('ascii','ignore')
	
	
	global_tic = time.time()
	
	result = process_command(cmd.encode('ascii','ignore'))
	last_executed_command = cmd
	
	if result : pio.say('done')

	while True :
		if move(location=['gpsr_start_point']) : break

	cmd_cnt += 1

pio.say('done')
