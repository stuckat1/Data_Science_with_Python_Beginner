
# cd d:\dev\classes\datascience\doh
# import imp
# import doh
# imp.reload(doh)
# doh.go()
#


#
#%matplotlib inline
home_dir = r'D:\dev\classes\datascience\dohmh_restaurant-inspections_002'

import pandas as pd
import numpy as np
import pylab as pl
import json
import copy

from pandas import DataFrame
from IPython.display import Image

from types import *
from datetime import datetime

# ------------------------------------------------------------------------------
webextract_cnames = ['camis', 'dba','boro','building','street','zip','phone',
                     'cuisine','inspdate', 'action', 'violcode','score','grade',
                     'gradedate','recorddate']

def readWebextract() :

    # Read a truncated test file
    return pd.read_csv( home_dir + r'\WebExtractTrunc2.txt',
                        names = webextract_cnames, header=0, low_memory = False)

    # Read the whole large file
    #return pd.read_csv( home_dir + r'\WebExtract.txt', names = webextract_cnames,
    #                    header=0, low_memory = False)


# ------------------------------------------------------------------------------
def stringToDate(s) :

    return datetime.strptime(s[0:10], '%Y-%m-%d')

# ------------------------------------------------------------------------------
def stringToYear(s) :

    return s[0:4]

# ------------------------------------------------------------------------------
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


def breakdownCAMIS(df) :


    # construct columns to delete
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')
    cnames.remove('inspdate')

    d_copy = df.drop(cnames,axis=1)

    # Drop duplicate inspections
    d_copy.drop_duplicates(inplace = True)

    # Add a year colukmn for each row
    d_copy['year'] = d_copy['inspdate'].map(stringToYear)

    # Remove inspdate column and then remove even further duplicates
    d_copy.drop('inspdate', axis=1, inplace = True)
    print d_copy



def transitions(df) :

    prior_k1 = ""
    prior_k2 = ""

    for (k1, k2), group in df.groupby(['camis','inspdate']) :
        print "=============================="
        print k1, k2

        rating_row = group[['dba','inspdate','action','score','grade']].drop_duplicates()

        if k1 != prior_k1 :
            print "First line!"
        else :
            delta = (stringToDate(k2) - stringToDate(prior_k2)).days / 365.0
            print("Compute %s to %s = %f" % (prior_k2, k2, delta))


        print rating_row
        #print group.drop_duplicates()
        #for k3, group2 in group.groupby('')

        prior_k1 = k1
        prior_k2 = k2



# ------------------------------------------------------------------------------
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

    # Read data file
    df = readWebextract()

    # Fixup actions so they are consistent
    updateActionColumn( df)

    # Check IDS so assumptions hold
    checkCAMIS(df)

    # CAMIS by borough by year
    breakdownCAMIS(df)

   # Do some work
   # transitions(df)

