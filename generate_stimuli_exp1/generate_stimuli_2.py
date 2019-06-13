import random
import numpy as np

def get_states(n, states = [""]):
    if n == 0:
        return states
    else:
        add_states = []
        for state in states:
            add_states.append(state + "0")
            add_states.append(state + "1")
        return get_states(n-1, add_states)

def map_to_objs(all_c): 
    objs = []
    for C in all_C:
        obj = ""

        if (int(C[0])):
            obj += "red"
        else:
            obj += "green"

        if int(C[1]):
            obj += "_square"

        else:
            obj += "_triangle"

        if int(C[2]):
            obj += ".jpg"
        else:
            obj += "_small.jpg"
        objs.append(obj)


    return objs

all_C = get_states(3)

objs = map_to_objs(all_C)

half_states = get_states(7)
all_states = []
for state in half_states:
	full_state = state + "0"
	l_state = []
	for i in full_state:
		l_state.append(int(i))
	all_states.append(l_state)

print all_states
for i in range(len(all_states)):
	state = all_states[i]
	#print(state)
	#for j in range(len(state)):
		#obj = objs[j]

#print random.sample(all_states, 256)