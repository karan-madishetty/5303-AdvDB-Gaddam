#SHRAVANI GADDAM(M20228201)
#KARAN MADISHETTY(M20228991)
#http://104.236.194.242:5000
#http://104.236.194.242/5303-AdvDB-Madishetty/mongoDB-Project/


from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse
from flask import jsonify
from flask_cors import CORS, cross_origin

#from pymongo import MongoClient
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

import datetime

import json
import urllib



import timeit

app = FlaskAPI(__name__)
CORS(app)

client = pymongo.MongoClient('localhost', 27017)
db = client['shravani']
businessdb = db['yelp.business']
review = db['yelp.review']
userdb = db['yelp.user']
tip = db['yelp.tip']

parser = reqparse.RequestParser()

"""=================================================================================="""


@cross_origin() # allow all origins all methods.
@app.route("/", methods=['GET'])
def index():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list

	
"""=================================================================================="""
#1.Find all restaurants with zip code X or Y
# curl : curl -X GET http://104.236.194.242:5000/zip/zips=89117,89122:start=0:limit=20

@app.route("/zip/<args>", methods=['GET'])

def zip(args):
    args=myParseArgs(args)
     
    data = []
    zips=args['zips']
    firstzip,secondzip = zips.split(",")
    limit=int(args['limit'])
    
    result = businessdb.find({},{'full_address':1,'_id':0})
    	
    for r in result:
        parts = r['full_address'].split(' ')
        target = parts[-1]
        
        if target == firstzip or target == secondzip:
		    data.append(r['full_address'])
    if 'limit' in args.keys():
        return {"data":data[:limit]}
    else:
    	return {"data":data}



"""=================================================================================="""
# Find all restaurants in city X
# curl -X GET http://104.234.194.242:5000/city/city=Las Vegas:start=0:limit=20
#2.
@app.route("/city/<args>", methods=['GET'])
def city(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    city = args['city']
    data = []
    
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find({"city" : city},{"full_address":1,"name":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find({"city" : city},{"full_address":1,"name":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find({"city" : city},{"full_address":1,"name":1,"_id":0}).limit(args['limit'])
    else:
        result = businessdb.find({"city" :city},{"full_address":1,"name":1,"_id":0}).limit(10)  

    for r in result:
        data.append(r)


    return {"data":data}
	


"""==================================================================================""" 
# Find the restaurants within 5 miles of lat , lon
# curl -X GET http://104.234.194.242:5000/closest/lon=-80.839186:lat=35.226504:start=0:limit=20


#3.
@app.route("/closest/<args>", methods=['GET'])
def closest(args):

    args = myParseArgs(args)
	
       
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
		
    lon = float(args['lon'])
    lat = float(args['lat'])
    data = []
    data1 = [] 
    
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find({ "loc" : { "$geoWithin" : { "$centerSphere": [ [ lon, lat ], 5 / 3963.2 ] } } },{"business_id":1,"name":1,"_id":0}).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find({ "loc" : { "$geoWithin" : { "$centerSphere": [ [ lon, lat ], 5 / 3963.2 ] } } },{"business_id":1,"name":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find({ "loc" : { "$geoWithin" : { "$centerSphere": [ [ lon, lat ], 5 / 3963.2 ] } } },{"business_id":1,"name":1,"_id":0}).limit(args['limit'])
    else:
        result = businessdb.find({ "loc" : { "$geoWithin" : { "$centerSphere": [ [ lon, lat ], 5 / 3963.2 ] } } },{"business_id":1,"name":1,"_id":0}).limit(10)  

    for r in result:
        data.append(r)


    return {"data":data}
"""==================================================================================""" 
# Find all the reviews for restaurant X
# curl -X GET http://104.234.194.242:5000/reviews/id=hB3kH0NgM5LkEWMnMMDnHw:start=0:limit=20

#4.	
@app.route("/reviews/<args>", methods=['GET'])
def reviews(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
    if 'id' in args.keys():
        id = args['id']
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = review.find({'business_id' : id},{"id":1,"text":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = review.find({'business_id' : id},{"id":1,"text":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = review.find({'business_id' : id},{"id":1,"text":1,"_id":0}).limit(args['limit'])
    else:
        result = review.find({'business_id' : id},{"id":1,"text":1,"_id":0}).limit(10)  

    for row in result:
        data.append(row)


    return {"data":data}
    
	
"""=================================================================================="""


"""=================================================================================="""
# Find all the reviews for restaurant X that are 5 stars.
# curl -X GET http://104.234.194.242:5000/stars/id=hB3kH0NgM5LkEWMnMMDnHw:num_stars=5:start=0:limit=20


#5.
@app.route("/stars/<args>", methods=['GET'])
def stars(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
    #if 'id' in args.keys():	
    args['id'] = args['id']
    #if 'num_stars' in args.keys():
    args['num_stars'] = int(args['num_stars'])
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = review.find({'business_id' : args['id'], 'stars' : args['num_stars']},{"review_id" : 1, "text":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = review.find({'business_id' : args['id'], 'stars' : args['num_stars']},{"review_id" : 1, "text":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = review.find({'business_id' : args['id'], 'stars' : args['num_stars']},{"review_id" : 1, "text":1,"_id":0}).limit(args['limit'])
    else:
        result = review.find({'business_id' : args['id'], 'stars' : args['num_stars']},{"review_id" : 1, "text":1,"_id":0}).limit(10)  

    for r in result:
        data.append(r)


    return {"data":data}
	
"""=================================================================================="""
# Find all the users that have been 'yelping' for over 5 years.
# curl -X GET http://104.234.194.242:5000/yelping/min_years=5:start=0:limit=20

#6.
@app.route("/yelping/<args>", methods=['GET'])
def yelping(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
	
    years = int(args['min_years'])
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({ "yelping_since" : {"$lte":"2010-07"}}, {"_id":0,"name":1}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({ "yelping_since" : {"$lte":"2010-07"}}, {"_id":0,"name":1}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({ "yelping_since" : {"$lte":"2010-07"}}, {"_id":0,"name":1}).limit(args['limit'])
    else:
        result = userdb.find({ "yelping_since" : {"$lte":"20110-07"}}, {"_id":0,"name":1}).limit(10)  

    for r in result:
        data.append(r)


    return {"data":data}
"""=================================================================================="""
# Find the business that has the tip with the most likes.
# curl -X GET http://104.234.194.242:5000/most_likes/start=0:limit=20

#7.
@app.route("/most_likes/<args>", methods=['GET'])
def most_likes(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
	
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = tip.find({},{"business_id":1,"_id":0}).sort("likes", -1).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = tip.find({},{"business_id":1,"_id":0}).sort("likes", -1).skip(args['start'])
    elif 'limit' in args.keys():
        result = tip.find({},{"business_id":1,"_id":0}).sort("likes", -1).limit(args['limit'])
    else:
        result = tip.find({},{"business_id":1,"_id":0}).sort("likes", -1).limit(10)  

    for r in result:
        data.append(r)


    return {"data":data}
"""=================================================================================="""
# Find the average review_count for users.
# curl -X GET http://104.234.194.242:5000/review_count/

#8.
@app.route("/review_count/", methods=['GET'])
def review_count():
    
    data = []
    
    result = userdb.aggregate([{"$group":{"_id":"review_count","averageReviewCount":{"$avg":"$review_count"}}}])
    for r in result:
            data.append({"avg":r['averageReviewCount']})
    return {"data":data}
	
"""=================================================================================="""
# Find all the users that are considered elite.
# curl -X GET http://104.234.194.242:5000/elite/start=0:limit=20


#9.
@app.route("/elite/<args>", methods=['GET'])
def elite(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
	
    
    #.skip(1).limit(1)
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({"elite":{"$ne":[]}},{"user_id":1,"name":1,"elite":1,"_id":0}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({"elite":{"$ne":[]}},{"user_id":1,"name":1,"elite":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({"elite":{"$ne":[]}},{"user_id":1,"name":1,"elite":1,"_id":0}).limit(args['limit'])
    else:
        result = userdb.find({"elite":{"$ne":[]}},{"user_id":1,"name":1,"elite":1,"_id":0}).limit(10)  

    for r in result:
        data.append(r)


    return {"data":data}
	
"""=================================================================================="""
# Find the longest elite user.
# curl -X GET http://104.234.194.242:5000/elite/start=0:limit=1:sorted=reverse

#10.
@app.route("/longest_elite/<args>", methods=['GET'])
def longest_elite(args):

    args = myParseArgs(args)
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
    sort = args['sorted']
	
    result = userdb.aggregate([{"$group": { "_id" :0 , "max": {"$max": {"lengthofelite" :{ "$size" : "$elite"}}}}}])
    #.skip(1).limit(1)
   

    for r in result:
        data.append(r)


    return {"data":data}
	
"""=================================================================================="""
# Of elite users, whats the average number of years someone is elite.
# curl -X GET http://104.236.194.242:5000/avg_elite/

#11.
@app.route("/avg_elite/", methods=['GET'])
def avg_elite():
    
    data = []
    
    result = userdb.aggregate([{'$project': {'elitelength':{'$size':"$elite"}}},{'$group':{"_id":0, "avg":{'$avg':"$elitelength"}}}])
    for r in result:
            data.append(r)
    return {"data":data}
	
"""=================================================================================="""
@app.route("/business/<args>", methods=['GET'])
def business(args):

    args = myParseArgs(args)
    
    data = []
    
    result = businessdb.find({},{'_id':0}).limit(100)
    
    for row in result:
        data.append(row)
    

    return {"data":data}
	


	
"""=================================================================================="""

def snap_time(time,snap_val):
    time = int(time)
    m = time % snap_val
    if m < (snap_val // 2):
        time -= m
    else:
        time += (snap_val - m)
        
    if (time + 40) % 100 == 0:
        time += 40
        
    return int(time)

"""=================================================================================="""
def myParseArgs(pairs=None):
    """Parses a url for key value pairs. Not very RESTful.
    Splits on ":"'s first, then "=" signs.
    
    Args:
        pairs: string of key value pairs
        
    Example:
    
        curl -X GET http://cs.mwsu.edu:5000/images/
        
    Returns:
        json object with all images
    """
    
    if not pairs:
        return {}
    
    argsList = pairs.split(":")
    argsDict = {}

    for arg in argsList:
        key,val = arg.split("=")
        argsDict[key]=str(val)
        
    return argsDict
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
