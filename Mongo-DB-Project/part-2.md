###Mongo DB Project

###Part 2

###Typical Queries

db.yelp.business.find({$or: [{"full_address" : {$regex : ".89117."}},{"full_address" : {$regex : ".89122."}}]}).count()

db.yelp.business.find({"full_address": {$regex: ".Las Vegas."}}).count()

db.yelp.business.find({ "loc" : { $geoWithin : { $centerSphere: [ [ -80.839186, 35.226504 ], 5 / 3963.2 ] } } }).count()

db.yelp.review.find({"business_id" : "hB3kH0NgM5LkEWMnMMDnHw")}).count()

db.yelp.review.find({ $and : [{"business_id" : "P1fJb2WQ1mXoiudj8UE44w"}, {"stars" : 5}]}).count()

db.yelp.user.find({ "yelping_since" : {$lte:"2011-11"}}, {"_id":0,"name":1})

INCOMP db.yelp.user.find({"name":"Lynda"}, {_id:1})

db.yelp.user.aggregate([{$group:{_id:"review_count",averageReviewCount:{$avg:"$review_count"}}}])

db.yelp.user.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1})

db.yelp.user.find({"elite":{"$ne":[]}}).sort({"elite":-1}).limit(1)
