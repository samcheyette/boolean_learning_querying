from lot_analysis_exp4 import *
STEPS = 5000
N_CPLX= 4
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
   


def compatible_concs(stim, concepts):
    compatible = []

    for c in concepts:
        hd = get_dist(stim, c)
        if hd  == 0:
            compatible.append(c)

    

    return compatible


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


def get_best_hyps(stim, concepts, seen, MIN_N):

    data = [FunctionData(alpha=1.-1e-9,  input=all_C, 
                        output=stim)]
    h0 = MyHypothesis()


    for h in MHSampler(h0, data, 
                    steps=STEPS, acceptance_temperature=2.): 

        out = h(all_C)
        str_h = str(h)
        if out not in seen:
            seen[out] = set()
            concepts[out] = []

        if str_h not in seen[out]:
            seen[out].add(str_h)
            concepts[out].append(np.sum(get_rule_counts(grammar, h.value)))



    return concepts,seen


def get_data(file, MIN_N):
    df = pd.read_csv(file)
    t = time.time()

    count = 0
    incr_prev = -1
    concepts = {}
    dct_exact ={}
    hum_data = {}
    av_cplx_prev = {}
    seen = {}
    av_cplx = 0.
    tot_av_cplx = []

    init = time.time()
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

        if incr != incr_prev:
            incr_prev = incr

            categories_so_far = ["." for _ in range(2**N_CPLX)]

        stim = "".join(categories_so_far)


        compatible = compatible_concs(stim, concepts)
        count_unk = stim.count(".")

        while len(compatible) < count_unk:
            concepts, seen= get_best_hyps(stim, concepts, seen, MIN_N)
            compatible = compatible_concs(stim, concepts)


        compatible = compatible_concs(stim, concepts)

        if len(compatible) > 0:
            mdl = min([min(concepts[c]) for c in compatible])
            print count, stim, len(compatible), mdl
            #print
            #posteriors = assign_posterior_scores(stim,concepts)
            #for p in posteriors[:5]:
              #  print stim, p[0],round(p[1]*1000,5), min(concepts[p[0]])
            #print "*" * 20
        else:
            print stim, "NONE :("
        categories_so_far[selected] = str(obj_category)
        count += 1

        if count % 20 == 0:
            t = time.time() - init
            print
            print count, t, count/t, t/count
            print
            #break

    print "*X*X*X*X*X*X"

    return df, concepts



def assign_posterior_scores(stim, concepts,n_prim=8,noise=0.01):
    rem = stim.count(".")
    posts = []

    for c in concepts:
        hd = get_dist(c, stim)
        lklhd = ((1.-noise)**(rem-hd)) * (noise**hd)
        prior = (1./n_prim)**min(concepts[c])

        posterior = lklhd * prior
        posts.append((c,posterior))

    posts = sorted(posts, key=lambda x: - x[1])



    return posts




def output_for_pymc(file,data,concepts, MIN_N):
    categories_so_far = ["." for _ in range(2**N_CPLX)]
    memo_post = {}
    incr_prev = -1
    output = "incr,subj,stim,n_query,selected,obj_category,"
    output += "guess,correct,concept,cplx,dist,mod_pred\n"

    for i, trial in data.iterrows():
        incr = trial["incr"]
        subj = trial["uniqueid"]
        selected = trial["selected"]
        correct = trial["correct_guess"]
        query_trial = trial["n_query"]
        phase =  trial["trial_phase"]
        objs_remain = trial["objs_remain"]
        obj_category = trial["obj_category"]

        if incr != incr_prev:
            incr_prev = incr

            categories_so_far = ["." for _ in range(2**N_CPLX)]

        stim = "".join(categories_so_far)

        if stim not in memo_post:
            memo_post[stim] = assign_posterior_scores(stim,concepts)

        posteriors = memo_post[stim]


        if correct:
            guess = obj_category
        else:
            guess = 1-obj_category


        for p in posteriors[:MIN_N]:
            conc = p[0]
            bool_cplx = str(min(concepts[conc]))
            mod_pred = str(conc[selected])

            dist = str(get_dist(p[0],stim))

            print stim, conc,bool_cplx, dist
            print mod_pred,guess
            #print [(x,type(x)) for x in guess,correct,conc,bool_cplx,dist,mod_pred]
            output += "%d,%s,%s,%d,%d,%d," % (incr,subj,stim,query_trial,selected,obj_category)
            output += "%d,%d,%s,%s,%s,%s\n" % (guess,correct,"x_"+conc,bool_cplx,dist,mod_pred)
        print


        categories_so_far[selected] = str(obj_category)


    f= open(file,"w")
    f.write(output)
    f.close()


if __name__ == "__main__":

    import time
    MIN_N = 20



    concepts = {}
    seen = set()




    data, concepts = get_data("data.csv",MIN_N)
    output_for_pymc("pymc_analysis/mc_data_small.csv", data, concepts,10)
    output_for_pymc("pymc_analysis/mc_data.csv", data, concepts,20)

    output_for_pymc("pymc_analysis/mc_data_big.csv", data, concepts,50)

