from lot_analysis_exp4 import *

def compute_prior(mod, a, loc, scale):

    if len(mod[0]) > 0:
        out = np.zeros(2**N_CPLX)
        norm = 0.
        priors = st.gamma.pdf(mod[0],a,loc,scale)

        #priors = 1./(2**mod[0])
        priors = priors/(np.sum(priors)+1e-10)
        outs = priors.dot(mod[1])
        return outs
    else:
        return np.ones(2**N_CPLX) * 0.5

def compatible_ish(stim,conc,differ):
    accept = True
    dist = 0
    i = 0
    while accept and i < len(stim):
        if stim[i] == '0' and conc[i] == '1':
            dist += 1
            if dist >= differ:
                accept = False
        elif  stim[i] == '1' and conc[i] == '0':
            dist += 1
            if dist >= differ:
                accept = False
        i += 1
    return accept


def get_compatible_concepts(stim, concepts):
    all_possible = []
    all_exts = []
    for c in concepts:

        if compatible(stim, c):
            exts = [int(x) for x in c]
            for x in  concepts[c]:
                cnc = sum(x[4]) - 1
               

                all_exts.append(exts)
                all_possible.append(cnc)

    return np.array(all_possible), np.array(all_exts)


def get_data(file, concepts):
    df = pd.read_csv(file)
    t = time.time()

    count = 0
    incr_prev = -1
    dct_compatible = {}
    hum_data = {}
    for i, trial in df.iterrows():
        incr = trial["incr"]
        subj = trial["uniqueid"]
        count += 1
        if count % 200 == 0:
            nt = time.time() - t

            print count, nt, count/(nt)

        if incr != incr_prev:

            incr_prev = incr

            categories = trial["categories"][2:]
            cplx = np.array(trial["cplx"])
            categories_so_far = ["." for _ in range(len(categories))]
            stim = "".join(categories_so_far)

        selected = trial["selected"]
        correct = np.array(trial["correct_guess"])
        query_trial = np.array(trial["n_query"])
        phase =  trial["trial_phase"]
        objs_remain = trial["objs_remain"]
        obj_category = trial["obj_category"]

        stim = "".join(categories_so_far)
        if stim not in dct_compatible:
            pc = get_compatible_concepts(stim, concepts)
            #print stim, [round(x,1) for x in compute_prior(pc,1,0,1)]

        

            dct_compatible[stim] = pc

        if (stim, selected) not in hum_data:
            hum_data[(stim,selected)] = []


        if correct:
            guess = obj_category
        else:
            guess = 1-obj_category

        hum_data[(stim,selected)].append(guess)
        categories_so_far[selected] = str(obj_category) #categories[selected]


    return hum_data, dct_compatible

def get_ll(human, model, a, loc, scale, intcpt, noise):
    lls = 0.
    for h in human:
        hum_resps = human[h]
        mod_preds = compute_prior(model[h[0]], a,loc,scale)
        mod_pred = mod_preds[h[1]]
        mod_pred = mod_pred  + (intcpt-mod_pred) * noise
        ll =st.bernoulli.logpmf(hum_resps, mod_pred)
        lls += np.sum(ll)
    return lls



#def get_prior


def infer_prior(human, model, STEPS):

    a_curr,loc_curr,scale_curr = 15,0,5
    int_curr, noise_curr = 0.5, 0.5

    ll_curr = get_ll(human, model, a_curr, loc_curr, scale_curr, int_curr, noise_curr)
   #prior_curr = get_prior(a_curr,loc_cur,scale_curr,noise_curr)

    for step in range(STEPS):
        a_prop = np.exp(np.log(a_curr) + np.random.normal(0,.2))
        loc_prop = loc_curr + np.random.normal(0,0.1)
        #loc_prop = loc_curr
        scale_prop = np.exp(np.log(scale_curr) + np.random.normal(0,.2))
       
        int_prop = max(min(int_curr + np.random.normal(0,0.1), 0.75),0.25)
        noise_prop = min(noise_curr + np.random.normal(0,0.1), 0.75)
        #int_prop = np.random.beta(1+int_curr*20., 1+(1.-int_curr)*20.) 
        #noise_prop = np.random.beta(1+noise_curr*20., 1+(1.-noise_curr)*20.) 

        #noise_prop = np.exp(np.log(noise_curr) + np.random.normal(0,.1))

        ll_prop = get_ll(human, model, a_prop, loc_prop, scale_prop,int_prop, noise_prop)
        if ll_prop > ll_curr or (np.exp(ll_prop - ll_curr) > random.random()):
            a_curr,loc_curr,scale_curr,int_curr,noise_curr =  a_prop, loc_prop, scale_prop, int_prop,noise_prop
            ll_curr = ll_prop
            print "~" * 50
            print a_curr,loc_curr,scale_curr,int_curr,noise_curr
            print ll_curr
            print "~" * 50

            print

        elif step % 25 == 0:
            print "*"*50

            print "STEP: ", step
            print a_curr,loc_curr,scale_curr,int_curr,noise_curr
            print ll_curr
            print
            print a_prop,loc_prop,scale_prop,int_prop,noise_prop
            print ll_prop
            print "*"*50
            print


if __name__ == "__main__":

    import time


    STEPS = 10000
    N_CPLX= 4

    concepts = {}
    seen = set()

    cncpts = load_concepts('pkl_files/conc_count_1.pkl')



    concept_priors = {}
    for c in cncpts:
        concept_priors[c] = 0.
        for tup in cncpts[c]:
            concept_priors[c] += tup[0]


    hum_data, mod_data = get_data("data.csv", cncpts)


    keys = sorted(hum_data.keys(), key= lambda x : abs(0.5-np.mean(hum_data[x])))
    

    infer_prior(hum_data, mod_data, STEPS)



   # analyze_posterior_shapes = 