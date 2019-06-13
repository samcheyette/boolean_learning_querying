from lot_analysis_exp4 import *
all_C = get_states(N_CPLX)

def compute_prior(mod, n_seen,a, loc, scale, noise):

    if len(mod[0]) > 0:
        out = np.zeros(2**N_CPLX)
        norm = 0.

        
        priors = st.gamma.pdf(mod[0],a,loc,scale)

        m2 = np.ones_like(mod[2])
        priors = priors * ((noise*m2)**mod[2])
        priors = priors * (((1-noise)*m2)**(n_seen-mod[2]))
        #priors = 1./(2**mod[0])
        priors = priors/(np.sum(priors)+1e-15)
        outs = priors.dot(mod[1])
        return outs

    else:
        return np.ones(2**N_CPLX) * 0.5

def get_dist(stim,conc):
    dist = 0
    for i in xrange(len(stim)):
        if stim[i] == '0' and conc[i] == '1':
            dist += 1
        elif  stim[i] == '1' and conc[i] == '0':
            dist += 1

    return dist
   


def get_compatible_concepts(stim, concepts, max_hd=3):
    all_possible = []
    all_exts = []
    all_dist = []
    """
    n_total = 0
    dct = {}
    for c in concepts:
        hd = get_dist(stim, c)
        

        if hd < 4:

            exts = [int(x) for x in c]
            lst = sorted(concepts[c], key = lambda x: sum(x[4][:6]))
            mdls = lst[:10]
            for mdl in mdls:
                all_possible.append(sum(mdl[4][:6]))
                all_exts.append(exts)
                all_dist.append(hd)
    """
    for c in concepts:
        hd = get_dist(stim, c)
        if hd <= max_hd:

            exts = [int(x) for x in c]
            for x in  concepts[c]:
                cnc = sum(x[4][:6]) + 1



                all_exts.append(exts)
                all_possible.append(cnc)
                all_dist.append(hd)
    

    return np.array(all_possible), np.array(all_exts),np.array(all_dist)


def get_cplx(stim, concepts, memoized):

    if stim in memoized:
        mdl = memoized[stim]
    else:
        compatible = get_compatible_concepts(stim, concepts, 0)
        if len(compatible[0]) == 0:
            mdl = 10
        else:
            mdl = min([i for i in compatible[0]])
        memoized[stim] = mdl

    return mdl, memoized



def get_best_hyp(stim):

    data = [FunctionData(alpha=1.-1e-9,  input=all_C, 
                        output=stim)]
    h0 = MyHypothesis()

    for h in MHSampler(h0, data, 
                    steps=STEPS, acceptance_temperature=2.): 

        out = h(all_C)
        str_h = str(h)

def get_data(file, concepts):
    df = pd.read_csv(file)
    t = time.time()

    count = 0
    incr_prev = -1
    dct_compatible = {}
    dct_exact ={}
    hum_data = {}
    av_cplx_prev = {}
    av_cplx = 0.
    tot_av_cplx = []

    categories_so_far = ["." for _ in range(2**N_CPLX)]
    for i, trial in df.iterrows():
        incr = trial["incr"]
        subj = trial["uniqueid"]
        selected = trial["selected"]
        correct = np.array(trial["correct_guess"])
        query_trial = np.array(trial["n_query"])
        phase =  trial["trial_phase"]
        objs_remain = trial["objs_remain"]
        obj_category = trial["obj_category"]

        stim = "".join(categories_so_far)

        if count % 100 == 0:
            nt = time.time() - t

            print count, nt, count/(nt)

        if incr != incr_prev:
            if count > 5000:
                break
            if count > 0:

                cplx_category, dct_exact = get_cplx(stim, concepts, dct_exact)

                if subj not in av_cplx_prev:
                    av_cplx_prev[subj] = [6.]
                

                av_cplx = np.mean(av_cplx_prev[subj])

                av_cplx_prev[subj].append(cplx_category)
                tot_av_cplx.append(cplx_category)

            incr_prev = incr

            categories = trial["categories"][2:]
            cplx = np.array(trial["cplx"])
            categories_so_far = ["." for _ in range(len(categories))]
            stim = "".join(categories_so_far)




        if stim not in dct_compatible:
            n_seen = len(stim) - stim.count(".")
            pc = get_compatible_concepts(stim, concepts)
           # prior = compute_prior(pc,n_seen,1,0,1,0.1, np.zeros(len(pc[0])), np.zeros(len(pc[0])))

           # print stim, [round(x,2) for x in prior]
            #if count == 5:
               # assert(False)

            dct_compatible[stim] = pc

        if (stim, selected) not in hum_data:
            hum_data[(stim,selected)] = [[],[]]


        if correct:
            guess = obj_category
        else:
            guess = 1-obj_category

        hum_data[(stim,selected)][0].append(guess)
        hum_data[(stim,selected)][1].append(av_cplx)
        categories_so_far[selected] = str(obj_category) #categories[selected]

        count += 1

    sd_av_cplx = np.std(tot_av_cplx)
    tot_av_cplx = np.mean(tot_av_cplx)
    for h in hum_data:
        hum_data[h][1] = (np.array(hum_data[h][1]) - tot_av_cplx)/ sd_av_cplx

    return hum_data, dct_compatible

def get_ll(human, model, a, loc, scale, intcpt, noise, beta_cplxs):
    lls = 0.
    h_resps = np.array([0])
    m_resps = np.array([0])
    for h in human:
        hum_resps = human[h][0]
        av_cplxs = human[h][1]
        n_seen = len(h[0]) - h[0].count(".")
        for i in xrange(len(hum_resps)):
            a_cplx = a + beta_cplxs * av_cplxs[i]
            mod_preds = compute_prior(model[h[0]],n_seen, a_cplx,loc,scale,noise)
            mod_pred = mod_preds[h[1]]
            mod_pred = mod_pred  + (intcpt-mod_pred) * noise
            ll =st.bernoulli.logpmf(hum_resps[i], mod_pred)

            h_resps = np.append(h_resps, hum_resps[i])
            m_resps = np.append(m_resps, mod_pred)
            lls += np.sum(ll)

    r = st.spearmanr(h_resps, m_resps)
    return lls, r



#def get_prior


def show_gamma(a,b,c,low=0,high=6):
    ys= []
    for i in range(low,high):
        ys.append(st.gamma.pdf(i,a,b,c))

    ys = np.array(ys)/sum(ys)
    ys = [round(i,3) for i in list(ys)]



    return ys



def infer_prior(human, model, STEPS):

    a_curr,loc_curr,scale_curr = 5, 0,1.5
    int_curr, noise_curr = 0.5, 0.3
    beta_cplxs_curr = 0.



    ll_curr, r_curr = get_ll(human, model, a_curr, loc_curr, scale_curr, 
                int_curr, noise_curr,beta_cplxs_curr)
   #prior_curr = get_prior(a_curr,loc_cur,scale_curr,noise_curr)

    for step in range(STEPS):
        a_prop = np.exp(np.log(a_curr) + np.random.normal(0,.3))
        loc_prop = loc_curr + np.random.normal(0,0.3)
        #loc_prop = 0
        beta_cplxs_prop = beta_cplxs_curr + np.random.normal(0,0.1)
        #loc_prop = loc_curr
        scale_prop = np.exp(np.log(scale_curr) + np.random.normal(0,.3))
       
        int_prop = max(min(int_curr + np.random.normal(0,0.05), 0.75),0.25)
        noise_prop = max(min(np.exp(np.log(noise_curr + np.random.normal(0,0.05))), 0.75),0.05)
        #int_prop = np.random.beta(1+int_curr*20., 1+(1.-int_curr)*20.) 
        #noise_prop = np.random.beta(1+noise_curr*20., 1+(1.-noise_curr)*20.) 

        #noise_prop = np.exp(np.log(noise_curr) + np.random.normal(0,.1))

        ll_prop,r_prop = get_ll(human, model, a_prop, loc_prop, scale_prop,int_prop, noise_prop,
                                             beta_cplxs_prop)
        if ll_prop > ll_curr or (np.exp(ll_prop - ll_curr) > random.random()):
            a_curr,loc_curr,scale_curr,int_curr,noise_curr =  a_prop, loc_prop, scale_prop, int_prop,noise_prop
            beta_cplxs_curr = beta_cplxs_prop
            ll_curr = ll_prop
            print "~" * 50
            print a_curr,loc_curr,scale_curr,int_curr,noise_curr, beta_cplxs_curr
            print ll_curr
            print r_prop
            print show_gamma(a_curr,loc_curr,scale_curr)
            print "~" * 50

            print

        elif step % 25 == 0:
            print "*"*50

            print "STEP: ", step
            print a_curr,loc_curr,scale_curr,int_curr,noise_curr,beta_cplxs_curr
            print ll_curr
            print r_curr
            print show_gamma(a_curr,loc_curr,scale_curr)

            print
            print a_prop,loc_prop,scale_prop,int_prop,noise_prop,beta_cplxs_prop
            print ll_prop
            print r_prop
            print show_gamma(a_prop,loc_prop,scale_prop,)

            print "*"*50
            print


if __name__ == "__main__":

    import time


    STEPS = 10000
    N_CPLX= 4

    concepts = {}
    seen = set()

    cncpts = load_concepts('pkl_files/conc_count_2.pkl')



    concept_priors = {}
    for c in cncpts:
        concept_priors[c] = 0.
        for tup in cncpts[c]:
            concept_priors[c] += tup[0]


    hum_data, mod_data = get_data("data.csv", cncpts)


    keys = sorted(hum_data.keys(), key= lambda x : abs(0.5-np.mean(hum_data[x])))
    

    infer_prior(hum_data, mod_data, STEPS)



   # analyze_posterior_shapes = 