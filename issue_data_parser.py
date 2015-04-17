#!/usr/bin/python

import os
import psycopg2
import sys
import simplejson
from pprint import pprint

connection = None
# get the project name that is also the nane of the json file as a parameters passed to the script
project_name  = sys.argv[1]

try:
    
    #connect to the database to retrieve the file name linked with the commit
    connection = psycopg2.connect(host='cranberry', port='5432', database='re', user='re', password='re')
    cursor = connection.cursor()
    
    # drop table to store commit data if it does not exists
    # cursor.execute("drop table if exists issues")
    #create table
    # cursor.execute("create table issues (project_name text, bug_id numeric, bug_number numeric, title text, pull_request text,  user_id numeric, user_login text, state text, locked boolean, assignee_id numeric, assignee_login text, comment_count numeric, created_at timestamp without time zone, updated_at timestamp without time zone, closed_at timestamp without time zone, body text, labels text)")
    

    # concat path to the commit file
    path = "/Users/evermal/Documents/soen691E/course_project/issues/"

    for root, dirs, files in os.walk(path):
        for f in files:

            # catch all files of this project
            if project_name in f :
                print f    

                # read as a json object
                with open(root+f) as data_file:
                    data = simplejson.load(data_file)
                
                # extract wanted data and insert into the database
                for x in xrange(0,len(data)):
                    
                    bug_id  = 0
                    bug_number = 0
                    title = "no_title"
                    user_id = 0
                    user_login ="no_user_login"
                    state ="no state"
                    locked = False
                    assignee_id = 0
                    assignee_login ="no_assignee"
                    comment_count = 0
                    updated_at = "2999-09-09T00:00:00Z"
                    closed_at  = "2999-09-09T00:00:00Z"
                    body = "no_body"
                    pull_request = "no_pull_request"

                    bug_id = data[x]['id']                    
                    bug_number = data[x]['number']
                    title = data[x]['title'].replace('\'', '"')
                    if data[x]['user'] is not None:
                        user_id = data[x]['user']['id'] 
                        if data[x]['user']['login'] is not None:                        
                            user_login = data[x]['user']['login'].replace('\'', '"')
                    state = data[x]['state'].replace('\'', '"')
                    locked = data[x]['locked']
                    if data[x]['assignee'] is not None:
                        assignee_id = data[x]['assignee']['id']
                        if data[x]['assignee']['login'] is not None:    
                            assignee_login = data[x]['assignee']['login'].replace('\'', '"')
                    comment_count = data[x]['comments']
                    created_at = data[x]['created_at']
                    updated_at = data[x]['updated_at']
                    closed_at = data[x]['closed_at']
                    if data[x]['body'] is not None:
                        body = data[x]['body'].replace('\'', '"')
                    if data[x]['labels'] is not None:
                        labels = str(data[x]['labels']).replace('\'', '"')

                    if 'pull_request' in str(data[x]):
                        pull_request = "is_pull_request"

                    if created_at is None:
                        created_at = "2999-09-09T00:00:00Z"
                    if updated_at is None:
                        updated_at = "2999-09-09T00:00:00Z"
                    if closed_at is None:            
                        closed_at = "2999-09-09T00:00:00Z"
                    if str(labels) == "[]":
                        labels = "no_labels"
                
                                                                                                                                                                                                                                                        
                    cursor.execute("insert into issues(project_name, bug_id, bug_number, title, pull_request, user_id, user_login , state , locked , assignee_id , assignee_login , comment_count , created_at , updated_at , closed_at , body , labels ) values ('"+project_name+"','"+str(bug_id)+"','"+str(bug_number)+"','"+title+"','"+pull_request+"','"+str(user_id)+"','"+user_login+"','"+state+"','"+str(locked)+"','"+str(assignee_id)+"','"+assignee_login+"','"+str(comment_count)+"',to_timestamp('"+created_at+"','YYYY-MM-DD HH24:MI:SS'),to_timestamp('"+updated_at+"','YYYY-MM-DD HH24:MI:SS'),to_timestamp('"+closed_at+"','YYYY-MM-DD HH24:MI:SS'),'"+body+"','"+labels+"')") 
        
except Exception, e:
    print  e
    connection.rollback()

finally:
    connection.commit()