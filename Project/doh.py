#%matplotlib inline
home_dir = r'D:\dev\classes\datascience\dohmh_restaurant-inspections_002'

import pandas as pd
import numpy as np
import pylab as pl
import json
import copy

from pandas import DataFrame
from IPython.display import Image

webextract_cnames = ['camis', 'dba','boro','building','street','zip','phone','cuisine','inspdate',
                'action', 'violcode','score','grade', 'gradedate','recorddate']

def readWebextract() :

    # Read a truncated test file
    return pd.read_csv( home_dir + r'\WebExtractTrunc2.txt', names = webextract_cnames, header=0,
                        low_memory = False)

    # Read the whole large file
    #return pd.read_csv( home_dir + r'\WebExtract.txt', names = webextract_cnames, header=0,
    #                    low_memory = False)


def checkCAMIS( df) :

    #
    #  Find the number of unique CAMIS id.
    #

    # construct columns to delete
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')

    d_copy = df.drop(cnames,axis=1)
    d_copy.drop_duplicates(inplace = True)
    camis_len = len(d_copy)
    print "Found %i CAMIS ids" % camis_len


    #
    #  Find the number of unique CAMIS/boro/building/stsreet/zip groups
    #


    # construct columns to delete
    cnames.remove('dba')
    cnames.remove('boro')
    cnames.remove('building')
    cnames.remove('street')
    cnames.remove('zip')

    d_copy = df.drop(cnames,axis=1)
    d_copy.drop_duplicates(inplace = True)
    group_len = len(d_copy)
    print "Found %i CAMIS/boro/building/street/zip groups" % group_len

    if group_len == camis_len :
        print "Congrats, both sets match!"
    else :
        print "Sorry, both sets do not match!"

def foo(df) :

    for (k1, k2), group in df.groupby(['camis','inspdate']) :
        print "=============================="
        print k1, k2
        rating_row = group[['camis','dba','inspdate','action','score','grade']].drop_duplicates()

        print rating_row
        #print group.drop_duplicates()
        #for k3, group2 in group.groupby('')


def updateActionColumn( df) :

    #
    # Replace confusing action id given by the City that is time dependant
    # with one that has the consistent meaning across time.
    #

    # Ideally, all this would be table driven so it could be easily updated but this
    # a first attempt and non-production code. ;)

    # A - No violations were recorded at the time of this inspection.
    # B - Violations were cited in the following area(s).
    # C - Establishment Closed by DOHMH.  Violations were cited in the following area(s) and
    #     those requiring immediate action were addressed.
    # D - Establishment re-opened by DOHMH
    # E - Establishment padlocked by DOHMH
    # F - Establishment re-closed by DOHMH

    #print "Before:"
    #print df[['dba','inspdate','action']]

    # B -> A
    df.ix[ df.action == 'B', 'action'] = 'A'

    # C -> A or B
    # to be completed!!!
    df.ix[ np.logical_and(df.action == 'C', df.inspdate <= '2010/07/18 00:00:00'),'action'] = 'A'
    df.ix[ np.logical_and(df.action == 'C', df.inspdate  > '2010/07/18 00:00:00'),'action'] = 'B'

    #    D, E & F -> B
    df.ix[ df.action == 'D','action'] = 'B'
    df.ix[ df.action == 'E','action'] = 'B'
    df.ix[ df.action == 'F','action'] = 'B'

    # G -> C
    df.ix[ df.action == 'G','action'] = 'C'

    # O -> D
    df.ix[ df.action == 'O','action'] = 'D'

    # P -> E or F
    # to be completed!!!
    df.ix[ np.logical_and(df.action == 'P', df.inspdate <= '2010/07/18 00:00:00'),'action'] = 'E'
    df.ix[ np.logical_and(df.action == 'P', df.inspdate  > '2010/07/18 00:00:00'),'action'] = 'B'

    #    S, T & U -> F
    df.ix[ df.action == 'S','action'] = 'B'
    df.ix[ df.action == 'T','action'] = 'B'
    df.ix[ df.action == 'U','action'] = 'B'

    # W -> F
    df.ix[ df.action == 'W','action'] = 'F'

    #print "After:"
    #print df[['dba','inspdate','action']]

def go() :


    df = readWebextract()

    updateActionColumn( df)

    checkCAMIS(df)

    foo(df)

