
from helpers import *
import pandas as pd
import numpy as np


glob_cats = [[0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0],[0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0],[1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],[1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0],[0,1,0,1,1,1,1,0,0,1,0,1,0,0,1,0],[1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0],[1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1],[1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1],[0,1,0,0,0,1,0,0,1,1,0,0,1,1,0,0],[0,1,0,0,1,1,1,0,0,1,0,1,1,0,1,0],[0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0],
[0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0],[0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0],[0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],[0,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1],[0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
[0,0,1,1,1,1,1,1,0,0,1,1,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,1,0,0,1,1,1,0,0,1,0,1,0,0,0,0],[1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1],[1,0,1,1,0,0,0,1,1,0,1,0,0,1,0,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],[0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],[0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0],[1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1],[0,1,0,0,1,1,1,0,0,1,0,0,0,0,1,0],[1,0,1,1,0,0,0,1,1,0,1,0,1,1,1,1],[0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
[0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1],[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0],[0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0],[1,0,1,1,1,0,1,1,0,0,1,1,0,0,1,1],
[1,1,1,1,0,0,0,0,1,1,1,1,0,1,0,1],[1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],[1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0],[0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0]]


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
    #grammar.add_rule('BOOL', 'not__(x_(%s[%s]))', ['C', str(i)], 1.)

	#grammar.add_rule('BOOL', 'eq__(%s[%s], 0)', ['C', str(i)], 1.0)
	#grammar.add_rule('BOOL', 'eq__(%s[%s], 1)', ['C', str(i)], 1.0)

grammar.add_rule('BOOL', 'and__', ['BOOL', 'BOOL'], 0.5)
grammar.add_rule('BOOL', 'or__', ['BOOL','BOOL'], 0.5)
grammar.add_rule('BOOL', 'not__', ['BOOL'], 1.0)

grammar.add_rule('BOOL', '0', None, 0.5)
grammar.add_rule('BOOL', '1', None, 0.5)
#grammar.add_rule('BOOL', 'xor__', ['BOOL','BOOL'], 0.5)
#grammar.add_rule('BOOL', 'nand__', ['BOOL','BOOL'], 0.5)






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
    subj_group = df.groupby(["uniqueid", "trial_id"])

    l = []

    for i, trial in subj_group:

        #print i
        categories = [x[2:] for x in list(trial["categories"])][0]
        #phase = np.array([x[0] for x in trial["trial_phase"]])
        selected = np.array(trial["selected"])
        cplx = np.array(trial["cplx"])
        correct = np.array(trial["correct_guess"])

        if len(selected) == len(categories):
            observed_categories = [0 for _ in range(len(cplx))]
            for j in range(len(categories)):
                cat =int(categories[int(selected[j])])
                if correct[j]:
                    observed_categories[selected[j]] = cat
                else:
                    observed_categories[selected[j]] = 1-cat


            observed_categories = [str(k) for k in observed_categories]
            observed_categories = "".join(observed_categories)




            l.append({'categories':categories, 
                'selected':selected, 'cplx':cplx,
                 'observed_cats':observed_categories})

    return l

"""

def get_data(file):
    df = pd.read_csv(file)
    subj_group = df.groupby(["incr"])

    l = []

    for i, trial in subj_group:

        #print i
        categories = [x[2:] for x in list(trial["categories"])][0]
        #phase = np.array([x[0] for x in trial["trial_phase"]])
        selected = np.array(trial["selected"])
        cplx = np.array(trial["cplx"])
        correct = np.array(trial["correct_guess"])

        if len(categories) == len(selected):

            categories_so_far = ["." for _ in range(len(categories))]
            resps_so_far = ["." for _ in range(len(categories))]

            all_resp = ["." for _ in range(len(selected))]

            for k in range(len(selected)):
                if correct[k]:
                    resp = categories[k]
                else:
                    resp = str(1-int(categories[k]))

                all_resp[k] = resp




            for k in range(len(selected)):
                #categories_so_far[selected[k]] = categories[selected[k]]
                if k > 0:

                    categories_so_far[selected[k-1]] = categories[selected[k-1]]

                if correct[k]:
                    resp = categories[selected[k]]
                else:
                    resp = str(1-int(categories[selected[k]]))

                resps_so_far[selected[k]] = resp

                l.append({"n_query":k, 'categories':categories, 
                        'category':categories[selected[k]],
                          'cats_so_far': "".join(categories_so_far),
                            'resp':resp,
                    'resps': all_resp,
                'all_selected':selected, 'selected':selected[k],
                 'cplx':cplx,

                    'correct': correct[k], 'all_correct':correct,
                 'resps_so_far':"".join(resps_so_far)})


    return l




def compatible(stim,conc):
    accept = True
    i = 0
    while accept and i < len(stim):
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



def get_rule_counts(grammar, t, add_counts ={}):
    """
            A list of vectors of counts of how often each nonterminal is expanded each way

            TODO: This is probably not super fast since we use a hash over rule ids, but
                    it is simple!
    """

    counts = defaultdict(int) # a count for each hash type

    for x in t:
        if type(x) != FunctionNode:
            raise NotImplementedError("Rational rules not implemented for bound variables")
        
        counts[x.get_rule_signature()] += 1 


    for k in add_counts:
        counts[k] += add_counts[k]

    # and convert into a list of vectors (with the right zero counts)
    out = []
    for nt in grammar.rules.keys():
        v = np.array([ counts.get(r.get_rule_signature(),0) for r in grammar.rules[nt] ])
        out.append(v)
    return out

if __name__ == "__main__":


    #make_all_objs([["rect","circle"],
           # ["red","blue"], ["big","small"],
                #["solid","unfilled"]], "all_objs.txt")
    STEPS = 10000
    CHAINS = 1
    N_CPLX= 4
    TOP_N = 500

    all_C = get_states(N_CPLX)
    concepts = {}
    concept_cplxs = {}
    concept_ps = {}
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

    mod_probs_dct = {}
    """

    categories=[]

    for hd in human_data:
        categories.append(hd["categories"])

    categories = list(set(categories))

    for c in categories:
        print c

    """
    resps = {}
    trues = {}
    categories=[]

    for hd in human_data:
        tmp = ""
        category = hd["category"]
        selected = hd["selected"]
        cats_so_far = hd["cats_so_far"]
        resp = hd["resp"]
        resps_so_far = hd["resps_so_far"]
        correct = hd["correct"]
        if (cats_so_far, selected) not in resps:
            resps[(cats_so_far, selected)] = []
            trues[(cats_so_far, selected)] = []

        resps[(cats_so_far, selected)].append(int(resp))
        trues[(cats_so_far, selected)].append(int(category))

        categories.append((cats_so_far, selected))

    for r in sorted(resps.keys(), key=lambda x: np.mean(resps[x])):
        cat_true =  round(np.mean(trues[r]), 1)
        resp = round(np.mean(resps[r]),1)
       # if not "0" in r[0]:
       # print r, resp, cat_true, resp-cat_true



    #assert(False)
    #categories += glob_cats
    categories = sorted(list(set(categories)), key=lambda x: -x[0].count("."))
    #categories = list(set(categories))
    c_seen = []

    
    rule_keys = []

    for z in grammar: 
        #print z.get_rule_signature()
        rs_orig = z.get_rule_signature()
        name = rs_orig[1].replace("'", "")
        print name
        name = name.replace("(", "")
        name = name.replace(")", "")
        name = name.replace(",","")
        name = name.replace("%s", "S")
        name = name.replace(" ", "")

        rs = (rs_orig[0], name)

        rule_keys.append(rs)


    for cs in categories:
        category = cs[0]
        c_seen.append(cs)
        data = [FunctionData(alpha=1.-1e-9,  input=all_C, 
                            output=category)]
                          # output="".join(categories))]

                            #output=stim)]

        h0 = MyHypothesis()

        MAP = None
        best_post = -float("inf")
        best_out = ""


        n_comp = n_compatible(category, concepts)
        #print concepts
        cnt = 0
        #print category, n_comp




        while n_compatible(category, concepts) < 10:
            print category, n_comp, cnt

            cnt += 1

            for _ in range(CHAINS):
                for h in MHSampler(h0, data, 
                    steps=STEPS, acceptance_temperature=2.): 

                    out = h(all_C)
                    str_h = str(h)

                    if out not in concepts:
                        concepts[out] = []
                        concept_ps[out] = 0.

                    if str_h not in seen:
                        concept_ps[out] += np.exp(h.prior)
                        if len(concepts[out]) < TOP_N or np.exp(h.prior) > min([x[0] for x in concepts[out]]):
                            

                            rc = get_rule_counts(grammar, h.value)
                            concepts[out].append((np.exp(h.prior), len(h.value),out, count, rc[0], rule_keys))
                            concepts[out] = sorted(concepts[out], key=lambda tup: -tup[0])
                            

                            if len(concepts[out]) > TOP_N:

                                concepts[out] = concepts[out][:TOP_N]
                        seen.add(str_h)


                        if h.posterior_score > best_post:
                            MAP = str(h)
                            best_post = h.posterior_score
                            best_out = out
                                #print h, out
                            #print category, n_compatible(category, concepts)
                            #print best_out
                           # print best_post
                           # print concept_ps
                           # print


       # keys = sorted(concept_ps.keys(), key=lambda x: concept_ps[x])
        if len(c_seen) % 10 == 5:
            print "*" * 10
            mod_fit,true_fit,rand_fit = 0.,0.,0.
            rps,tps,mps = [],[],[]
            for r in c_seen:
                r_check = r[0][:r[1]] + "x"  
                if r[1]+1 < len(r[0]):
                    r_check += r[0][r[1]+1:]
                #if len(r) > 0:
                if r[0] not in mod_probs_dct or random.random() < 0.2:
                    mod_probs = prob_categories(r[0], concepts)
                    mod_probs_dct[r[0]] = mod_probs
                mod_probs = mod_probs_dct[r[0]]

                resp_probs = resps[r]

                resp_prob = round(np.mean(resps[r]),1)
                #true_prob = round(np.mean(trues[r]),1)

                true_prob = np.mean(trues[r]) + (0.5-np.mean(trues[r])) * 0.6
                mod_prob = mod_probs[r[1]] + (0.5-mod_probs[r[1]])*0.8

                #mod_fit +=  len(resp_probs) * (mod_prob - resp_prob)**2.
                #true_fit +=  len(resp_probs) * (true_prob - resp_prob)**2.
                #rand_fit = len(resp_probs) * (0.5-resp_prob) **2.
                mf = np.sum(st.bernoulli.logpmf(resp_probs,mod_prob))
                tf = np.sum(st.bernoulli.logpmf(resp_probs,true_prob))
                rf = np.sum(st.bernoulli.logpmf(resp_probs,0.5))

                mod_fit += mf
                true_fit += tf
                rand_fit += rf

                rps.append(resp_prob)
                tps.append(true_prob)
                mps.append(mod_prob)
                if len(c_seen) % 50 == 5:
                    print r_check, resp_prob,round(true_prob,1), mod_prob

                #print r[0], 0.5,round(true_prob,1),round(mod_prob,1)
                #print r[0], rf,tf,mf
                #print
            print "x"*5
            print rand_fit,true_fit, mod_fit
            print "x"
            print st.spearmanr(rps, tps)

            print st.spearmanr(rps, mps)
            print "x"
            print st.pearsonr(rps, tps)

            print st.pearsonr(rps, mps)
            print "x"*5

            print "*" * 10

            f = open("pkl_files/conc_count_2.pkl", "w")
            pickle.dump(concepts, f)
            f.close()

            f = open("pkl_files/hyps_count_2.pkl", "w")
            pickle.dump(seen, f)
            f.close()


