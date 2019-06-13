from lot_analysis_2 import *


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

    return ent


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



def add_entropys(concepts, file):
    df = pd.read_csv(file)
    subj_group = df.groupby(["incr"])

    l = []
    ent_lst = []
    ents = {}
    c = 0
    halves = np.ones(16) * 0.5
    unc = -np.sum(np.log2(halves) * halves) * 2
    query = list(df["n_query"])
    z = 0

    for i, trial in subj_group:
        if c % 100 == 0:
            print c

        c += 1

        categories = [x[2:] for x in list(trial["categories"])][0]
        phase = np.array([x[0] for x in trial["trial_phase"]])
        selected = np.array(trial["selected"])
        cplx = np.array(trial["cplx"])
        correct = np.array(trial["correct_guess"])
        query_trial = np.array(trial["n_query"])

        selected_so_far = []
        categories_so_far = ["." for _ in range(len(categories))]
        


        stim = "".join(categories_so_far)


        if stim not in ents:
            #ents[stim] = get_entropy_over_concepts(stim, concepts)
            ents[stim] = get_entropy_over_data(stim, concepts)


        ent_lst.append(ents[stim])
        print

        print list(trial["worker_id"])[0]
        print query_trial

        print "1", query[z], ent_lst[z]
        z += 1
        k = 0

        #print stim, ents[stim]

        while (k < max(query_trial)-1):
            selected_so_far.append(selected[k])
            categories_so_far[selected[k]] = categories[selected[k]]
            stim = "".join(categories_so_far)
            if stim not in ents:
               # ents[stim] = get_entropy_over_concepts(stim, concepts)
                ents[stim] = get_entropy_over_data(stim, concepts)

            ent_lst.append(ents[stim])
            print "2", query[z], ent_lst[z]
            z += 1
            k += 1

           # print stim, ents[stim]

        #print

        for _ in range(len(query_trial) - k-1):
            if stim not in ents:
                #ents[stim] = get_entropy_over_concepts(stim, concepts)
                ents[stim] = get_entropy_over_data(stim, concepts)

            ent_lst.append(ents[stim])
            print "3", query[z], ent_lst[z]
            z += 1
        print



    print len(ent_lst)
    print len(df['trial_phase'])

    df["entropy"] = ent_lst
    df.to_csv(file)


if __name__ == "__main__":
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler

    from LOTlib.SampleStream import *
    from LOTlib.DataAndObjects import FunctionData
    from LOTlib.TopN import TopN
    import numpy as np


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
            concept_priors[c] += tup[0]


    keys = sorted(concept_priors.keys(), key=lambda x: concept_priors[x])
    for key in keys:
        print key, concept_priors[key]
    add_entropys(concept_priors,"data.csv")
