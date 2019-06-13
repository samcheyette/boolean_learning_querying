import copy
import os.path
import time
import random
import itertools as it
import pickle
from LOTlib.Grammar import Grammar
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Miscellaneous import Infinity, beta, attrmem
from LOTlib.Primitives import primitive
from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.FunctionNode import FunctionNode

from LOTlib.SampleStream import *
from LOTlib.DataAndObjects import FunctionData
from LOTlib.TopN import TopN
import scipy.stats as st
from math import log, exp
from collections import defaultdict




def hamming_distance(a, b):
	assert(len(a) == len(b))
	hd = 0
	for i in xrange(len(a)):
		if a[i] != b[i]:
			hd += 1

	return hd


def get_all_stimuli(length):
	if length == 0:
		return [""]

	else:
		new_lst = []
		for x in copy.deepcopy(get_all_stimuli(length - 1)):
			y1 = x + "0"
			y2 = x + "1"
			new_lst.append(y1)
			new_lst.append(y2)
		return new_lst


def complexity_penalty(constant, hyp):
	cplx = hyp.value.count_subnodes()
	return const / float(2**cplx)


def invert(x):
    inv = ""
    for i in x:
        if i == "0":
            inv += "1"
        elif i == "1":
            inv += "0"
        else:
            assert(False)
    return inv


def output(file, model, data, app=False):

	if (not app) or (not os.path.isfile(file)):
		s = ("subj, blicket, resp, hyp, hyp_pred, prob, hamming,")
		s += "complexity, verbal, verbal_pred, alpha, time, RT_mean, RT_median\n"
		app_use = "w+"
	else:
		s = ""
		app_use = "a+"

	subs = 0
	tm = str(time.time())
	for m in model:

		blicket = "".join(["ab"[int(i)] for i in m[0]])
		resp = "".join(["ab"[i] for i in m[1]])
		verbal_resp = m[3]
		verbal_resp_pred = "".join(["ab"[i] for i in m[4]])
		alph = str(m[5])
		RT_mean = str(m[6])
		RT_med = str(m[7])

		for pred in m[2]:
			hyp = str(pred[0]).replace(",", "")
			hyp_pred = str("".join(["ab"[i] for i in pred[0](data)]))
			hd = str(hamming_distance(pred[0](data), m[1]))
			prob = str(round(pred[1],4))
			cplx = str(pred[2])

			print subs, blicket, resp, hyp, hyp_pred, prob, hd, cplx

			s += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (subs, blicket, resp, hyp,
															 hyp_pred, prob, hd, cplx,verbal_resp,
															 	 verbal_resp_pred, alph, tm,
															 	  RT_mean, RT_med)

		subs += 1
		print

	f = open(file, app_use)
	f.write(s)
	f.close()


def output_learning(file, model, app=False):

	if (not app) or (not os.path.isfile(file)):
		s = ("subj, blicket, alpha, hyp, cplx, prob, time, part_resp\n")
		app_use = "w+"
	else:
		s = ""
		app_use = "a+"

	tm = str(time.time())
	for m in model:
		print m
		blicket_bn = m[0]
		blicket = ""
		for i in blicket_bn:
			blicket += "ab"[int(i)]
		mod_res = m[1]
		alpha = m[2]
		subj = m[3]
		resp = m[4]

		for hpc in mod_res:
			hyp = str(hpc[0]).replace(",", "")
			cplx = str(max(1, hyp.count("C[")))

			prob = str(hpc[1])
			s += ("%s, %s, %s, %s, %s, %s, %s, %s\n" %
				 (str(subj), blicket, alpha, hyp, cplx, prob, tm, resp))

	f = open(file, app_use)
	f.write(s)
	f.close()



    

def get_states(n, states = [""]):
    if n == 0:
        return states
    else:
        add_states = []
        for state in states:
            add_states.append(state + "0")
            add_states.append(state + "1")
        return get_states(n-1, add_states)

