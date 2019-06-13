from lot_analysis_exp4 import *


def get_entropy_over_data(stim, concepts):
    """
 
    probs = prob_categories(stim, concepts)
    probs = probs + (0.5 - probs) * 1e-5

    entropy = -np.sum(probs * np.log2(probs))
    entropy += -np.sum((1.-probs) * np.log2(1.-probs))
    return entropy
    """
    all_possible = []
    exts = []
    for c in concepts:
        if compatible(stim, c):
            all_possible = np.append(all_possible, concepts[c])
            exts.append([int(x) for x in c])

    exts=np.array(exts)


    if len(all_possible) == 0:
        unc = stim.count(".")
        probs = []
        for s in stim:
            if s == ".":
                probs.append(0.5)
            else:
                probs.append(int(s))



        ent = -unc * (0.5 * np.log2(0.5))
       # ent = -1

    else:
        norm = np.sum(all_possible)
        all_possible = all_possible/norm

        #print all_possible
        probs = all_possible.dot(exts)
        probs = probs + (0.5 - probs) * 1e-6
        ent = -np.sum(probs * np.log2(probs))
        ent += -np.sum((1.-probs) * np.log2(1.-probs))

    return np.array(probs), ent


def get_entropy_over_concepts(stim, concepts):
    all_possible = []
    for c in concepts:
        if compatible(stim, c):
            all_possible = np.append(all_possible, concepts[c])


    if len(all_possible) == 0:
        unc = stim.count(".")
        ent = -unc * (0.5 * np.log2(0.5))

    else:
        all_possible += 1e-15
        norm = np.sum(all_possible)
        all_possible = all_possible/norm

        log_p = np.log2(all_possible)
        ent = -np.sum(all_possible * log_p)



    return ent



def convert_probs_to_score(probs, objs_remain):


    if objs_remain == 0:
        return 0




    p_correct = 0.5 +np.abs(0.5-probs)
   # p_correct =  np.sum(p_correct) 

    objs_already_categorized = (len(probs) - objs_remain)

    n_correct =  np.sum(p_correct)  - objs_already_categorized
    n_incorrect = objs_remain - n_correct

    score = n_correct - n_incorrect

    """
    print objs_remain
    print [round(x,1) for x in probs]
    print n_correct, n_incorrect
    print score

    print
    """
    return score




def get_entropy_after_query(categories_so_far, probs, concepts):
    entropys = []
    prob_ents = []
    scores = []
    objs_remain = categories_so_far.count(".")
    tot_ent = 0.
    tot_unc= 0.
    for i in range(len(categories_so_far)):
        is_unknown = categories_so_far[i] == "."
        if is_unknown:
            entropy = 0.
            score = 0.
            for flip in [0,1]:
                s = copy.copy(categories_so_far)
                s[i] = str(flip)
                stim = "".join(s)


                ent_probs, ent = get_entropy_over_data(stim, concepts)

                if flip == 0:
                    p =  (1.-probs[i])
                else:
                    p = probs[i]

                entropy += ent * p
                score += convert_probs_to_score(ent_probs, objs_remain-1) * p


           # print stim
            #print score
            #print
            entropys.append(entropy)
            scores.append(score)



    stim = "".join(categories_so_far)

    expected_entropy = np.mean(np.array(entropys))
    expected_score = np.mean(np.array(scores))
   # print "ES: ", expected_score
    #print "EE: ", expected_entropy
    #print "*" * 20
    #print
    return expected_score, expected_entropy




def get_info_gain(concepts, file):
    df = pd.read_csv(file)
    incr_prev, incr = -1, -1
    ents, expected_ents, expected_scores,scores, all_probs = [],[],[],[],[]
    dct_exp_ents = {}
    dct_ents = {}
    dct_exp_scores = {}
    dct_scores = {}
    dct_probs = {}
    expected_ent,entropy,count = 0,0,0
    t = time.time()
    for i, trial in df.iterrows():
        incr = trial["incr"]
        subj = trial["uniqueid"]
        if count % 200 == 0:
            nt = time.time() - t

            print count, nt, count/(nt)

        count += 1
        if incr != incr_prev:

            incr_prev = incr

            categories = trial["categories"][2:]
            cplx = np.array(trial["cplx"])
            categories_so_far = ["." for _ in range(len(categories))]
            stim = "".join(categories_so_far)

            print


        selected = np.array(trial["selected"])
        correct = np.array(trial["correct_guess"])
        query_trial = np.array(trial["n_query"])
        phase =  trial["trial_phase"]
        objs_remain = trial["objs_remain"]
        if phase == "querying":
            stim = "".join(categories_so_far)
            if stim in dct_ents:
                entropy = dct_ents[stim]
                expected_ent = dct_exp_ents[stim]
                score = dct_scores[stim]
                expected_score = dct_exp_scores[stim]
                probs = dct_probs[stim]
                prob = probs[selected]



            else:
                probs, entropy = get_entropy_over_data(stim, concepts)
                score = convert_probs_to_score(probs, categories_so_far.count("."))


                expected_score, expected_ent = get_entropy_after_query(categories_so_far, probs, concepts)
                dct_ents[stim] = entropy
                dct_exp_ents[stim] = expected_ent
                dct_scores[stim] = score
                dct_exp_scores[stim] = expected_score
                dct_probs[stim] = copy.copy(probs)
                prob = probs[selected]
                print "".join(categories_so_far), selected, trial["obj_category"], round(prob,1)

            categories_so_far[selected] = str(trial["obj_category"]) #categories[selected]

            #if (count + 500) % 1000 < 25:

              #  print stim, round(entropy,2),round(expected_ent,2), round(entropy,2) - round(expected_ent,2)
              #  print "".join([str(max(min(0.9,round(i,1)),0.1))[2] for i in probs])
               # print

        ents.append(entropy)
        expected_ents.append(expected_ent)
        scores.append(score)
        expected_scores.append(expected_score)
        all_probs.append(prob)

       # if objs_remain == 0:
          #  print "*-"*20
           # print

    df["entropy"] = ents
    df["expected_ent"] = expected_ents
    df["score"] = scores
    df["expected_score"] = expected_scores
    df["model_pred"] = all_probs

    df.to_csv(file, index=False)



if __name__ == "__main__":
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler

    from LOTlib.SampleStream import *
    from LOTlib.DataAndObjects import FunctionData
    from LOTlib.TopN import TopN
    import numpy as np
    import time

    #make_all_objs([["rect","circle"],
           # ["red","blue"], ["big","small"],
                #["solid","unfilled"]], "all_objs.txt")


    STEPS = 100
    N_CPLX= 4

    concepts = {}
    seen = set()

    cncpts = load_concepts('pkl_files/conc_2.pkl')



    concept_priors = {}
    for c in cncpts:
        concept_priors[c] = 0.
        for tup in cncpts[c]:
            print tup[0], np.exp(-(1+3*tup[1]))
            concept_priors[c] += tup[0]

    assert(False)
    keys = sorted(concept_priors.keys(), key=lambda x: concept_priors[x])
    #for key in keys:
      #  print key, concept_priors[key]
    info_gain = get_info_gain(concept_priors, "data.csv")
