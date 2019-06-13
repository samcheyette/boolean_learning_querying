
import sqlite3
import ast
from psiturk.amt_services import MTurkServices, init_db, db_session

#from amt_services_wrapper import MTurkServicesWrapper


connection = sqlite3.connect('participants.db')
cursor = connection.cursor()
cursor.execute("SELECT * FROM turkdemo") #turkdemo
results = cursor.fetchall()
map_str = lambda x: ','.join(map(str, x))

null=None
true=True
false=False

#output = []



bonus = {}


incr = 0
t_num = 0
for r in results:
    try:
        dic= eval(r[len(r)-1].encode('ascii', 'ignore'))
    #except:
    #  pass
        if 'data' in dic:
            trial = dic['data']


            for t in trial:
                header = [x for x in t]
                tt = t['trialdata']


                if tt['phase']=='TEST' and 'debug' not in dic['workerId']:
                    if tt['objs_remain'] == 15:
                      incr += 1

                    w,a = dic['workerId'], dic['assignmentId']
                    if (w,a) not in bonus:
                        bonus[(w,a)] = []

                    bonus[(w,a)].append(tt['total_money'])

                # if 'debug' not in dic['workerId'] and "A19S8APZYIU1AC" not in dic["workerId"]:
                  #  print tt



    except:
        print "FAIL"




for k in bonus:
    print k, max(bonus[k])