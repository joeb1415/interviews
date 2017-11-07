# 8/8 3pm 

"""
USGS Earthquake Catalog API Client Library
------------------------------------------
We’re hoping to ease adoption of the USGS Earthquake Catalog API (https://earthquake.usgs.gov/fdsnws/event/1/#parameters), a service that tracks and exposes data on earthquakes in the United States.

Write a client library for this API in your favorite language.

For the sake of time, let’s narrow the scope of the library. Here’s a subset of the API’s documentation that the library should work for:

URL
===
https://earthquake.usgs.gov/fdsnws/event/1/[METHOD[?PARAMETERS]]

METHOD
=======
*version* - https://earthquake.usgs.gov/fdsnws/event/1/version
Returns the full semantic version of the service as a string.
(PARAMETERS don’t apply to this endpoint)

*query* - https://earthquake.usgs.gov/fdsnws/event/1/query
Retrieves earthquake event data.

PARAMETERS
==========
*format*
Default: quakeml
Type: string
Description: Allowed values: quakeml, geojson, text, csv

*starttime*
Default: null
Type: string
Description: Limit to events on or after the specified start time. NOTE: All times use ISO8601 Date/Time format. Unless a timezone is specified, UTC is assumed.

*endtime*
Default: null
Type: string
Description: Limit to events on or before the specified end time. NOTE: All times use ISO8601 Date/Time format. Unless a timezone is specified, UTC is assumed.

*limit*
Default: null
Type: integer
Limit the results to the specified number of events. NOTE: The service limits queries to 20000, and any that exceed this limit will generate a HTTP response code “400 Bad Request”.

*offset*
Default: 1
Type: integer
Return results starting at the event count specified, starting at 1.

*orderby*
Default: null
Type: string
Order the results. The allowed values are:
- orderby=time
  order by origin descending time
- orderby=time-asc
  order by origin ascending time
- orderby=magnitude
  order by descending magnitude
- orderby=magnitude-asc
  order by ascending magnitude

The interface to this library is up to you.

Feel free to google/stack-overflow/etc. anything you need.

"""

import requests
import json
from pprint import pprint
from datetime import datetime


class EarthquakeAPI:
    def __init__(self):
        self.base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/'

    @property
    def version(self):

        r = requests.get(self.base_url + 'version')

        return r.text

    def query(self, params):
        '''
        {
         request_time: 123,
         earthquakes:
         [
          {
           time:
           coord: []
           mag:
          },
          {

          }
         ]
        }
        '''
        # format = geojson
        # starttime = input
        # endtime = input
        # limit = input default 1
        # orderby = input default time

        if 'format' not in params:
            params['format'] = 'geojson'
        if 'limit' not in params:
            params['limit'] = 1
        # TODO: warning if no starttime or endtime
        if 'orderby' not in params:
            params['orderby'] = 'time'

        url = self.base_url + 'query'
        r = requests.get(url, params)

        # TODO: handle limit > 1
        # TODO: error handling if bad request
        response_text = json.loads(r.text)['features'][0]

        quake_list = []

        coordinates = response_text['geometry']['coordinates']
        mag = response_text['properties']['mag']
        time = datetime.fromtimestamp(response_text['properties']['time'] / 1000)

        quake = {
            'time': time,  # specify time formatting?
            'mag': mag,
            'coordinates': coordinates
        }

        quake_list.append(quake)

        response = {
            'request_time': datetime.now(),
            'earthquakes': quake_list
        }

        return response


earthquake_api = EarthquakeAPI()
print(earthquake_api.version)
pprint(earthquake_api.query({'starttime': '2017-08-07'}))




############
# Fri 8/11 10am

# rob started 3 years ago from 30 people to 300 today
# python rest API, postgres, mongo db
# external api for plugins, internal for apps
# download sample product

# user builds form in editor
#
# TBL_FORM
# Form_ID
# Form Title
# Form sub title
# Owner_id --> FK User ID
#

# TBL_Question
# Question_ID
# Form_ID --> FK Form ID
# Question Title
# Is_Required
# Question_Desc
# Question_Type_ID
# Order_ID (within the form)


# TBL_SubQuestion
# Sub_QuestionID
# QuestionID
# OptionID --> muliptle choice fields


# TBL_Question_Type
# Question_type_id
# Question_type_name (multiple choice, radio, text)

# TBL_Form_access
#


# TBL_Answer
# Answer_ID
# Question_ID
# Answering_user_id
# answer_text

# answer_choice
# Answer_ID
# Question_ID
# Answering_user_id
# sub_question_id
# is_chosen

x = 0

