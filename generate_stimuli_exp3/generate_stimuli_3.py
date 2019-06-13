from LOTlib.Grammar import Grammar
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Miscellaneous import Infinity, beta, attrmem
from LOTlib.Primitives import primitive
from math import log, exp
from helpers_3 import *
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
    grammar.add_rule('BOOL', 'x_(%s[%s])', ['C', str(i)], 1.0)
    grammar.add_rule('BOOL', 'not__(x_(%s[%s]))', ['C', str(i)], 1.0)

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
    """
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
    """

    return objs


def make_all_objs(features, file):
    all_objs = it.product(*features)

    txt = "["
    for i in all_objs:
        tmp = [j+","for j in i]
        tmp[len(tmp)-1] = tmp[len(tmp)-1][:-1]
        txt += str(tmp) + ","
    txt += txt[:-1] + "]"
    f = open(file, "w+")
    f.write(txt)
    f.close()






def output_to_txt_file(conc, file, which):
    txt = "["

    i = 0
    for c in conc:
        if i % 5 == 4:
            txt += "\n"
        if which == 0:
            tmp = "["
            for j in str(c[which]):
                tmp += j + ","
            tmp = tmp[:-1]
            tmp= tmp+"],"

            txt += tmp

        else:
            txt += str(c[which]) + ","

        i += 1

    txt = txt[:-1]
    txt += "]"

    f = open(file, "w+")
    f.write(txt)
    f.close()

def get_concepts(concepts, max_cplx):
    conc_lst = []
    for c in concepts:
        conc_lst.append((c, concepts[c]))

    conc_lst = sorted(conc_lst, key=lambda tup: tup[1])


    n_below_max_cplx = 0
    for i in conc_lst:
        if i[1] < max_cplx:
            n_below_max_cplx += 1
            print i


    sample = random.sample(conc_lst[:n_below_max_cplx], 45)



    output_to_txt_file(sample,"sample.txt", 0)

    output_to_txt_file(sample,"sample_cplx.txt", 1)

def output_to_data(cplxs, data_file, output_file):
    df = pd.read_csv(data_file)
    new_col = []

    for i in df[" condition"]:
        cond = "".join([str(x) for x in exp1_conditions[i]])
        new_col.append(cplxs[cond])

    df["cplx"] = new_col

    df.to_csv(output_file)
    #for row in df:
      #  print row


def swap(l, i,j):
    l = copy.copy(l)
    max_ij = max([i,j])
    min_ij = min([i,j])
    l2 = l[:min_ij] 
    l2.append(l[max_ij])
    l2 += l[min_ij+1:max_ij] 
    l2.append(l[min_ij])
    l2 += l[max_ij+1:]
    return(l2)


def make_orders(cplx, n_items, n_orders, file):
    orders = []
    out = ""
    for j in xrange(n_items):
        numbers = list([i for i in xrange(2**cplx)])
        random.shuffle(numbers)
        item_order = [numbers]


        for i in xrange(n_orders-1):
            new_order = copy.copy(numbers)
            for _ in range(4):
                swp1 = random.randint(0,len(new_order)/2)
                swp2 = random.randint(swp1+1,len(new_order)-1)
                new_order = swap(new_order, swp1,swp2)

            item_order.append(new_order)

        orders.append(item_order)
        #order1 = numbers
       # order2 = swap(numbers, 0,len(numbers)-1)
        #orders.append([order1,order2])
       # order3 = swap(numbers,4,len(numbers)-1)
       #order4 = swap(numbers,8,len(numbers)-1)
       # order5 = swap(numbers,12,len(numbers)-1)
        #orders.append([order1,order2,order3,order4,order5])


    for o in xrange(len(orders)):
        order = orders[o]
        out += str(order) 
        if o < len(orders) -1:
           out  += ",\n"

    f= open(file,"w")
    f.write(out)
    f.close()

 





def make_orders_2(cplx, n_items, n_orders, file):
    orders = []
    out = "["
    numbers = list([i for i in xrange(2**cplx)])

    for j in xrange(n_items):
        random.shuffle(numbers)
        out += str(numbers) 
        if j < n_items-1:
            out += ",\n"
        else:
            out += "]"

    f = open(file,"w")
    f.write(out)
    f.close()
 



 


def run_mcmc(stim,concept,STEPS,all_C):
    data = [FunctionData(alpha=1.-1e-10,
                 input=all_C, output=stim)]

    h0 = MyHypothesis()



    for h in MHSampler(h0, data, 
            steps=STEPS): 

        out = h(all_C)
        n_subnodes = h.value.count_subnodes()
        #if out not in concepts:
          #  print "why"


        if n_subnodes < concepts[out]:
            concepts[out] = n_subnodes
            concepts[invert(out)] = n_subnodes
    return concepts




if __name__ == "__main__":
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler

    from LOTlib.SampleStream import *
    from LOTlib.DataAndObjects import FunctionData
    from LOTlib.TopN import TopN



    #orders = make_orders_2(4,5,4, "orders.txt")

    #for order in orders:
       # print order
        #print [len(o) for o in order]


    make_all_objs([["rect","circle"],
            ["red","blue"], ["big","small"],
                ["solid","unfilled"]], "all_objs.txt")



    STEPS = 10000
    N_CPLX= 4

    all_C = get_states(N_CPLX)
    concepts = {}
    concepts_use = {}

    all_stim = get_all_stimuli(2**N_CPLX)

    random.shuffle(all_stim)


    for stim in all_stim:
        concepts[stim] = 2**(N_CPLX+1)


    count = 0

    for stim in all_stim:
        concepts = run_mcmc(stim,concepts,STEPS,all_C)


        count += 1

        print
        n_below_max_cplx = 0
        for c in sorted(concepts.keys(), key=lambda x: -concepts[x]):
            if concepts[c] < 2**(N_CPLX + 1):
                print c, concepts[c]
                concepts_use[c] = concepts[c]
                n_below_max_cplx += 1
        print count, len(concepts), n_below_max_cplx


        if n_below_max_cplx > 50:
            break


    orig_stim = copy.deepcopy(concepts_use.keys())
    c = 0
    for stim in orig_stim:
        concepts_use = run_mcmc(stim,concepts_use,STEPS/5,all_C)
        print c, stim
        c += 1
    dct = {}
    for c in orig_stim:
        dct[c] = concepts_use[c]



    get_concepts(dct, 2**(N_CPLX+1))




   # output_to_data(concepts, "data.csv","out.csv")
