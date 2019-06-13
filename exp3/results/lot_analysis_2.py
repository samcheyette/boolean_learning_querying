from LOTlib.Grammar import Grammar
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Miscellaneous import Infinity, beta, attrmem
from LOTlib.Primitives import primitive
from math import log, exp
from helpers import *
import pandas as pd
import numpy as np


grammar = Grammar(start='BOOL')

@primitive
def and__(x,y):
	return int(x) * int(y)

@primitive
def nand__(x,y):
    return 1 - int(x) * int(y)

@primitive
def or__(x,y):
	return min(int(x) + int(y), 1)


@primitive
def xor__(x,y):
    return (int(x) + int(y)) % 2


@primitive
def eq__(x,y):
	return int(int(x) == int(y))

@primitive
def not__(x):
	return abs(int(x) - 1)

@primitive
def x_(f):
    return int(f)
maxLen = 4





for i in xrange(maxLen):
    grammar.add_rule('BOOL', 'x_(%s[%s])', ['C', str(i)], 1.)
    grammar.add_rule('BOOL', 'not__(x_(%s[%s]))', ['C', str(i)], 1.)

	#grammar.add_rule('BOOL', 'eq__(%s[%s], 0)', ['C', str(i)], 1.0)
	#grammar.add_rule('BOOL', 'eq__(%s[%s], 1)', ['C', str(i)], 1.0)

grammar.add_rule('BOOL', 'and__', ['BOOL', 'BOOL'], 0.5)
grammar.add_rule('BOOL', 'or__', ['BOOL','BOOL'], 0.5)
grammar.add_rule('BOOL', '0', None, 0.5)
grammar.add_rule('BOOL', '1', None, 0.5)
#grammar.add_rule('BOOL', 'xor__', ['BOOL','BOOL'], 0.5)
#grammar.add_rule('BOOL', 'nand__', ['BOOL','BOOL'], 0.5)

#grammar.add_rule('BOOL', 'not__', ['BOOL'], 1.0)





class MyHypothesis(LOTHypothesis):
    def __init__(self, **kwargs):


        LOTHypothesis.__init__(self, grammar=grammar,  maxnodes=400,
                                   display="lambda C: %s", **kwargs)

        if 'sp' in kwargs:

            self.use_size_principle = kwargs['sp']
        else:
            self.use_size_principle = False


    def __call__(self, stimuli_list):
    	out = ""
    	for stim in stimuli_list:
        	out += str(self.fvalue(stim))
        return out   	



    def compute_single_likelihood(self, datum):
    	out = self.__call__(datum.input)
    	length = len(out)
    	assert(len(datum.input) == len(datum.output))
    	assert(length == len(datum.output))

    	sim = 0.0
    	for i in xrange(len(out)):
            if datum.output[i] != ".":
        		if datum.output[i] == out[i]:
        			sim += log(datum.alpha)
        		else:
        			sim += log(1.0 - datum.alpha)

        if self.use_size_principle:
            #assumes positive examples only!
            assert(0 not in datum.output)
            stim = get_all_stimuli(maxLen)
            out_stim = self.__call__(stim)
            card_h = sum(out_stim)

            if card_h != 0:
                n_ex = len(datum.output)
                sim -= n_ex * log(card_h)


        return sim


def get_rule(grammar, which, data):

	rules_iter = grammar.enumerate(log(which + 2))

	for i in xrange(which):
		rules_iter.next()

	true_rule = rules_iter.next()
	h = MyHypothesis()

	h.set_value(true_rule)

	return h.value, h(data)


"""
def get_data(file):
    df = pd.read_csv(file)

    categories = [x[2:] for x in list(df["categories"])]
    phase = list(df["trial_phase"])
    selected = list(df["selected"])
    cplx = list(df["cplx"])

    obj_shape = list(df["obj_shape"])
    obj_size = list(df["obj_size"])
    obj_color = list(df["obj_color"])
    obj_texture = list(df["obj_texture"])


    data = {'categories':categories, 'phase': phase, 
            'selected':selected, 'cplx':cplx}


    return data

"""

def get_data(file):
    df = pd.read_csv(file)
    subj_group = df.groupby(["uniqueid", "trial_id"])

    l = []

    for i, trial in subj_group:

        #print i
        categories = [x[2:] for x in list(trial["categories"])][0]
        phase = np.array([x[0] for x in trial["trial_phase"]])
        selected = np.array(trial["selected"])
        cplx = np.array(trial["cplx"])
        correct = np.array(trial["correct_guess"])

        if len(selected) == len(categories):
            observed_categories = [0 for _ in range(len(cplx))]
            for j in range(len(phase)):
                cat =int(categories[int(selected[j])])
                if phase[j] == 'g':
                    if correct[j]:
                        observed_categories[selected[j]] = cat
                    else:
                        observed_categories[selected[j]] = 1-cat

                else:
                    observed_categories[selected[j]] = cat

            observed_categories = [str(k) for k in observed_categories]
            observed_categories = "".join(observed_categories)




            l.append({'categories':categories, 'phase': phase, 
                'selected':selected, 'cplx':cplx,
                 'observed_cats':observed_categories})

    return l




def compatible(stim,conc):
    accept = True
    i = 0
    while accept and i < len(conc):
        if stim[i] == '0' and conc[i] == '1':
            accept = False
        elif  stim[i] == '1' and conc[i] == '0':
            accept = False

        i += 1
    return accept



def prob_categories(stim, concepts):
    all_possible = []
    sum_prior = 0.
    for c in concepts:
        if compatible(stim, c):
            for cnc in concepts[c]:
                all_possible.append(cnc)
                sum_prior += cnc[0]

    all_possible = sorted(all_possible, key = lambda tup: -tup[0])

    if len(all_possible) == 0:
        probs = []
        for i in range(len(stim)):
            if stim[i] == ".":
                probs.append(random.random())
            else:
                probs.append(int(stim[i]))
    else:

        probs = np.zeros(len(stim))
        for poss in all_possible:
            prob = poss[0]/sum_prior
            for i in range(len(probs)):
                probs[i] += prob * (poss[2][i] == '1')

                #probs[i] = round(probs[i], 3)




    return np.array([round(x,1) for x in probs])


def n_compatible(stim, concepts):
    n_comp=0
    for c in concepts:
        if compatible(stim, c):
            n_comp += len(concepts[c])

    return n_comp

def load_concepts(file):
    f = open(file, "r")
    pkl_file = pickle.load(f)
    f.close()
    return pkl_file



if __name__ == "__main__":
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler

    from LOTlib.SampleStream import *
    from LOTlib.DataAndObjects import FunctionData
    from LOTlib.TopN import TopN


    #make_all_objs([["rect","circle"],
           # ["red","blue"], ["big","small"],
                #["solid","unfilled"]], "all_objs.txt")
    STEPS = 10000
    N_CPLX= 4

    all_C = get_states(N_CPLX)
    concepts = {}
    seen = set()


   # concepts = load_concepts('pkl_files/conc_1.pkl')
   # seen = load_concepts('pkl_files/hyps_1.pkl')

    #print concepts
    human_data = get_data("data.csv")
    random.shuffle(human_data)

    print len(human_data)

    print all_C
    all_stim = []
    all_cats = []
    all_obs = []
    tot_guess = 0

    hamming_true = 0
    hamming_model = 0

    count = 0

    for hd in human_data:
        phase = hd["phase"]
        observed_cats = hd["observed_cats"]
        categories = hd["categories"]
        selected = hd["selected"]

        selected_so_far = []
        categories_so_far = ["." for _ in range(len(categories))]

        i=0
        while (i < len(categories)) and (phase[i] != 'g'):
            selected_so_far.append(selected[i])
            categories_so_far[selected[i]] = categories[selected[i]]
            i += 1

        if ((i < len(categories)) and (i > 0)):

            stim = "".join(categories_so_far)
            all_stim.append(stim)
            all_cats.append(categories)
            all_obs.append(observed_cats)
            tot_guess += len(categories) - i
            #print selected_so_far
           # print stim
           # print
            data = [FunctionData(alpha=1.-1e-7,  input=all_C, 
                                output=stim)]
                              # output="".join(categories))]

                                #output=stim)]

            h0 = MyHypothesis()

            MAP = None
            best_post = -float("inf")
            best_out = ""

            n_comp = n_compatible(stim, concepts)
            print stim, n_comp

            while n_compatible(stim, concepts) < 2:

                for h in MHSampler(h0, data, 
                    steps=STEPS, acceptance_temperature=2.): 

                    out = h(all_C)
                    str_h = str(h)

                    if out not in concepts:
                        concepts[out] = []

                    if str_h not in seen:
                        if len(concepts[out]) < 200 or np.exp(h.prior) > min([x[0] for x in concepts[out]]):
                           # if len(concepts[out]) > 0:
                               # print len(concepts[out]), np.exp(h.prior), min([x[0] for x in concepts[out]])

                            concepts[out].append((np.exp(h.prior), len(h.value),out, count))
                            concepts[out] = sorted(concepts[out], key=lambda tup: -tup[0])
                            if len(concepts[out]) > 200:
                               # print len(concepts[out]), np.exp(h.prior), min([x[0] for x in concepts[out]])

                                concepts[out] = concepts[out][:200]
                               # print len(concepts[out]), np.exp(h.prior), min([x[0] for x in concepts[out]])
                               # print
                        seen.add(str_h)



                    #print h, out, h.posterior_score
                    if h.posterior_score > best_post:
                        MAP = str(h)
                        best_post = h.posterior_score
                        best_out = out
                        #print h, out
                print stim, n_compatible(stim, concepts)
                print best_out
                print best_post
                print


            tot_hd_true = 0
            tot_hd_model =0
            for l in range(len(all_stim)):
                p_cat = prob_categories(all_stim[l], concepts)
                rounded = "".join([str(int(round(z))) for z in p_cat])
                hd_true =  hamming_distance(all_cats[l], all_obs[l])
                hd_model =  hamming_distance(rounded, all_obs[l])
                tot_hd_true +=  hd_true

                tot_hd_model += hd_model
                if count % 25 == 0:
                    print
                    print "STIMULUS:", all_stim[l]
                    print "CATEGORY: %s (%d)" % (all_cats[l], hd_true)

                    print "MODEL   : %s (%d)" % (rounded,hd_model)
                    print "P(Objs):", p_cat

                    print

            print tot_hd_true, tot_hd_model
            print round(tot_hd_true/float(tot_guess),2), round(tot_hd_model/float(tot_guess),2)
            print len(seen), len(concepts.keys())

            f = open("pkl_files/conc_3.pkl", "w")
            pickle.dump(concepts, f)
            f.close()

            f = open("pkl_files/hyps_3.pkl", "w")
            pickle.dump(seen, f)
            f.close()

            print "*" * 100
            count += 1



    """

            hamming_model += hamming_distance(observed_cats, best_out)
            hamming_true += hamming_distance(categories, best_out)
            print "BEST"
            print stim
            print categories, hamming_distance(categories, best_out)
            print best_out, hamming_distance(observed_cats, best_out)
            print observed_cats

            print hamming_true, hamming_model
            print



            #i+=1

        print "*." * 20 + "*"



       # if count == 5:
          #  assert(False)


       # print categories
       # print observed_cats
        #print hamming_distance(categories, observed_cats)
        #print


    categories = human_data["categories"]
    phases = human_data["phase"]
    selected = human_data["selected"]

    for c in range(len(categories)):
        full_category = categories[c]
        phase = phases[c]
        select = all_C[selected[c]]
        obj_cat = full_category[selected[c]]
        print full_category, phase, select, obj_cat


    all_stim = get_all_stimuli(2**N_CPLX)

    random.shuffle(all_stim)


    for stim in all_stim:
        concepts[stim] = 2**(N_CPLX+1)


    count = 0

    for stim in all_stim:
        data = [FunctionData(alpha=1.-1e-10,
                 input=all_C, output=stim)]

        h0 = MyHypothesis()



        for h in MHSampler(h0, data, 
                steps=STEPS): 

            out = h(all_C)
            n_subnodes = h.value.count_subnodes()
            if out not in concepts:
                print "why"

            if n_subnodes < concepts[out]:
                concepts[out] = n_subnodes
                concepts[invert(out)] = n_subnodes


        count += 1

        print
        n_below_max_cplx = 0
        for c in sorted(concepts.keys(), key=lambda x: -concepts[x]):
            if concepts[c] < 2**(N_CPLX + 1):
                print c, concepts[c]
                n_below_max_cplx += 1
        print count, len(concepts), n_below_max_cplx






   # output_to_data(concepts, "data.csv","out.csv")
    """