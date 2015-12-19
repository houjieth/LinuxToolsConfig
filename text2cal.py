#!/usr/bin/python

import sys
import re

def main():

    # read and parse ics file
    content = sys.stdin.readlines()
    print content
    keyPattern = re.compile("(\w+);(.*$)")
    keyPatternFollow = re.compile("\s(.*$)")
    d = dict()
    for line in content:
        result = keyPattern.match(line)
        if result is not None:
            key = result.group(1)
            lastKey = key
            value = result.group(2)
            d[key] = value
        else:
            result = keyPatternFollow.match(line)
            if result is not None and lastKey is not None:
                #print result.group(1)
                d[lastKey] = d[lastKey] + result.group(1) 
            else:
                lastKey = None

    organizer = d['ORGANIZER']
    attendee = d['ATTENDEE']
    summary = d['SUMMARY']
    location = d['LOCATION']
    dtstart = d['DTSTART']
    dtend = d['DTEND']

    print attendee

    # need to beautify the start time and end time, generate date and timeRange
    dtpattern = re.compile(".*:(\d+)T(\d+)")
    dtresult = dtpattern.match(dtstart)
    date = dtresult.group(1)
    time = dtresult.group(2)
    stime = time[:2]+':'+time[2:4]+':'+time[4:6]

    dtresult = dtpattern.match(dtend)
    time = dtresult.group(2)
    etime = time[:2]+':'+time[2:4]+':'+time[4:6]

    timeRange = stime+'~'+etime

    #print date
    #print timeRange

    # append to .pal file
    fpal = open('/home/likewise-open/ANT/jiehou/.pal/meetings.pal', 'a')
    fpal.write(date+' ')
    fpal.write('SUMMARY: '+summary+' ')
    fpal.write('TIME: '+timeRange+' ')
    fpal.write('LOCATION: '+location+' ')
    fpal.write('ORGANIZER: '+organizer+' ')
    fpal.write('ATTENDEE: '+attendee+' ')
    fpal.write('\n')
		
main()
