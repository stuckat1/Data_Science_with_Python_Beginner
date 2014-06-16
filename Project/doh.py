
# cd d:\dev\classes\datascience\doh
# import imp
# import doh
# imp.reload(doh)
# doh.go()
#

# TODO:
# Remove anything from 1990
# Remove anything with boro = 0

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

    goforbroke = True

    if goforbroke == False :
        fname = r'\WebExtractTrunc2.txt'
    else :
        fname = r'\WebExtract.txt'

    # Read a truncated test file
    df = pd.read_csv( home_dir + fname, names = webextract_cnames, header=0, low_memory =False)

    return df.ix[ df['inspdate'] >= "2009-12-31 00:00:00"]

# ------------------------------------------------------------------------------
def stringToDate(s) :

    return datetime.strptime(s[0:10], '%Y-%m-%d')

# ------------------------------------------------------------------------------
def stringToYear(s) :

    return s[0:4]

def dropYears( df) :

    years = ['2007','2008','2009']

    for year in years :
        try :
            df.drop(year, axis=1, inplace=True)
        except:
            pass



# ------------------------------------------------------------------------------
def checkCAMIS( df) :

    #
    #  Find the number of unique CAMIS id.
    #
    print "********************************"
    print " Sanity checks on CAMIS ids"
    print "********************************"
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

    print "\n\n"

def statsRestaurantsLifeSpan(df) :

    print "********************************"
    print " Restaurant Life Spans"
    print "********************************"

    #
    # Report the number of inspections by boro and year
    #

    # Delete uninteresting columns
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')
    cnames.remove('boro')
    cnames.remove('inspdate')

    # Drop a bunch of uninteresting columns
    d_copy = df.drop(cnames,axis=1)

    # Add a year column for each row
    d_copy['year'] = d_copy['inspdate'].map(stringToYear)

    # Remove inspdate column
    d_copy.drop('inspdate', axis=1, inplace = True)

    # Drop duplicate inspections dates
    d_copy.drop_duplicates(inplace = True)

    cam13 = set( d_copy.ix[d_copy['year'] == '2013']['camis'].values)
    cam12 = set( d_copy.ix[d_copy['year'] == '2012']['camis'].values)
    cam11 = set( d_copy.ix[d_copy['year'] == '2011']['camis'].values)
    cam10 = set( d_copy.ix[d_copy['year'] == '2010']['camis'].values)

    print "Restaurants count:"
    print "2013:\t%i " % len(cam13)
    print "2012:\t%i " % len(cam12)
    print "2011:\t%i " % len(cam11)
    print "2010:\t%i " % len(cam10)

    total_by_union = len(cam13|cam12|cam11|cam10)
    print "\nTotal restaurants in existence over 4 years = %i" % total_by_union

    print "\n"
    print "New restaurants openings:"
    print "2013:\t%i " % len(cam13 - cam12)
    print "2012:\t%i " % len(cam12 - cam11)
    print "2011:\t%i " % len(cam11 - cam10)

    print "\n"
    print "Restaurants closings:"
    print "2013:\t%i " % len(cam12 - cam13)
    print "2012:\t%i " % len(cam11 - cam12)
    print "2011:\t%i " % len(cam10 - cam11)

    print "\n"
    print "Restaurants lifespans:"
    yr1 = len(cam13 - cam12) + \
          len((cam12 - cam13) & (cam12 - cam11)) + \
          len((cam11 - cam12) & (cam11 - cam10))


    yr2 = len(cam13 & cam12 - cam11) + \
          len(cam12 & cam11 - cam13 - cam10) + \
          len(cam11 & cam10 - cam12)

    yr3 = len(cam13 & cam12 & cam11 - cam10) + \
          len(cam12 & cam11 & cam10 - cam13)

    yr4 = len(cam13 & cam12 & cam11 & cam10)

    print "1 year: \t%i " % yr1
    print "2 years:\t%i " % yr2
    print "3 years:\t%i " % yr3
    print "4+ years:\t%i" % yr4

    total_by_span = yr1 + yr2 + yr3 + yr4
    print "check: sum of counts = %i " % total_by_span

    deficit = total_by_union - total_by_span
    print "missing inspections for %i restaurants. " % deficit

    print "\n\n"

def statsRestaurants(df) :

    #
    # Report the number of inspections by boro and year
    #
    print "********************************"
    print " Inspections Statistics"
    print "********************************"
    # Delete uninteresting columns
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')
    cnames.remove('boro')
    cnames.remove('inspdate')

    d_copy = df.drop(cnames,axis=1)

    # Add a year column for each row
    d_copy['year'] = d_copy['inspdate'].map(stringToYear)

    # Remove inspdate column and then remove even further duplicates
    d_copy.drop('inspdate', axis=1, inplace = True)

    # Drop duplicate inspections dates
    d_copy.drop_duplicates(inplace = True)

    #print d_copy

    pt = pd.pivot_table( d_copy, values='camis', rows=['boro'], cols=['year'],
                         fill_value = 0, aggfunc='count' )

    #dropYears(pt)

    print "Inspections by year and boro"
    print pt

    pt = pd.pivot_table( d_copy, values='camis', cols=['year'],
                         fill_value = 0, aggfunc='count' )

    #dropYears(pt)

    print "Inspections by year"
    print pt

    print "\n\n"

def statsRestaurantsByCuisine(df) :

    #
    # Report the number of inspections by cuisine and year
    #
    print "********************************"
    print " Cuisine Statistics"
    print "********************************"
    # Delete uninteresting columns
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')
    cnames.remove('cuisine')
    cnames.remove('inspdate')

    d_copy = df.drop(cnames,axis=1)

    # Drop duplicate inspections dates
    d_copy.drop_duplicates(inplace = True)

    # Add a year column for each row
    d_copy['year'] = d_copy['inspdate'].map(stringToYear)

    # Remove inspdate column and then remove even further duplicates
    d_copy.drop('inspdate', axis=1, inplace = True)

    # Drop duplicate inspections dates
    d_copy.drop_duplicates(inplace = True)

    #print d_copy

    pt = pd.pivot_table( d_copy, values='camis', rows=['cuisine'], cols=['year'],
                         fill_value = 0, aggfunc='count' )

    #dropYears(pt)

    print "Inspections by year and cuisine"
    print pt

    print "\n\n"

def statsRestaurantsClosures(df) :

    #
    # Report the number of inspections by cuisine and year
    #
    print "********************************"
    print " Closure Statistics"
    print "********************************"
    # Delete uninteresting columns
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')
    cnames.remove('action')
    cnames.remove('boro')
    cnames.remove('cuisine')
    cnames.remove('inspdate')

    d_copy = df.drop(cnames,axis=1)

    # Drop duplicate inspections dates
    #d_copy.drop_duplicates(inplace = True)

    # Add a year column
    d_copy['year'] = d_copy['inspdate'].map(stringToYear)

    # Remove inspdate column
    d_copy.drop('inspdate', axis=1, inplace = True)

    # Pick out only actions that resulted in closure
    d_copy = d_copy.ix[ np.logical_or(d_copy['action'] == 'C',d_copy['action'] == 'F')]

    # Drop duplicates if any
    d_copy.drop_duplicates(inplace = True)

    pt = pd.pivot_table( d_copy, values='camis', cols=['year'],
                         fill_value = 0, aggfunc='count' )
    #dropYears(pt)
    print "Closures by year"
    print pt

    pt = pd.pivot_table( d_copy, values='camis', rows=['boro'], cols=['year'],
                         fill_value = 0, aggfunc='count' )

    print "\n\n"
    #dropYears(pt)
    print "Closures by year and boro"
    print pt

    pt = pd.pivot_table( d_copy, values='camis', rows=['cuisine'], cols=['year'],
                         fill_value = 0, aggfunc='count' )

    print "\n\n"
    #dropYears(pt)
    print "Closures by year and cuisine"
    print pt

    print "\n\n"

def statsCleanestCuisines(df) :

    #
    # Report the number of inspections by cuisine and year
    #
    print "********************************"
    print " Cleanliness Statistics"
    print "********************************"
    # Delete uninteresting columns
    cnames = copy.deepcopy(webextract_cnames)
    cnames.remove('camis')
    cnames.remove('boro')
    cnames.remove('cuisine')
    cnames.remove('score')
    cnames.remove('inspdate')

    d_copy = df.drop(cnames,axis=1)

    #d_copy = df

    # Add a year column
    d_copy['year'] = d_copy['inspdate'].map(stringToYear)

    # Remove inspdate column
    #d_copy.drop('inspdate', axis=1, inplace = True)

    # Remove any rows with missing data.  Since we only
    # have four columns, only missing scores should be excluded.
    #d_copy.dropna(inplace = True)

    d_copy.drop_duplicates(inplace = True)


    pt = pd.pivot_table( d_copy, values='score', cols=['boro'],
                         fill_value = 0, aggfunc=np.average )
    #dropYears(pt)
    print "Scores by year"
    print pt


    pt = pd.pivot_table( d_copy, values='score', rows=['boro'],cols=['year'],
                         fill_value = 0, aggfunc=np.average )
    #dropYears(pt)
    print "Scores by year and boro"
    print pt

    print "\n\n"


def test(df) :

    for k1, group in df.groupby(['camis']) :
        print "==== ", group['dba'], "====="

        group = group[['dba','inspdate','grade']].drop_duplicates()

        for k2, group2 in group.groupby(['inspdate']) :
            print group2['grade']

def transitions(df) :

    prior_k1 = ""
    prior_k2 = ""
    prior_company = ""

    for (k1, k2), group in df.groupby(['camis','inspdate']) :
        print "=============================="
        #print k1, k2

        rating_row = group[['dba','inspdate','action','score','grade']].drop_duplicates()


        if k1 != prior_k1 :
            print "First line!"
            pass
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

    # Inspections by borough by year
    statsRestaurants(df)
    statsRestaurantsLifeSpan(df)

    # Inspections by cuisine by year
    statsRestaurantsByCuisine(df)

    # Closures
    statsRestaurantsClosures(df)

    # Cleaniless
    statsCleanestCuisines(df)


    # Do some work
    #test(df)
    #transitions(df)

