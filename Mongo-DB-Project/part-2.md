#SHRAVANI GADDAM 

##Mongo DB Project

###Part 2

###Typical Queries

1.db.yelp.business.find({$or: [{"full_address" : {$regex : ".89117."}},{"full_address" : {$regex : ".89122."}}]}).count()

2.db.yelp.business.find({"full_address": {$regex: ".Las Vegas."}}).count()

3.db.yelp.business.find({ "loc" : { $geoWithin : { $centerSphere: [ [ -80.839186, 35.226504 ], 5 / 3963.2 ] } } }).count()

4.db.yelp.review.find({"business_id" : "hB3kH0NgM5LkEWMnMMDnHw")}).count()

5.db.yelp.review.find({ $and : [{"business_id" : "P1fJb2WQ1mXoiudj8UE44w"}, {"stars" : 5}]}).count()

6.db.yelp.user.find({ "yelping_since" : {$lte:"2011-11"}}, {"_id":0,"name":1})

7.db.yelp.tip.find({},{business_id:1,likes:1}).sort({likes:-1}).limit(1)

8.db.yelp.user.aggregate([{$group:{_id:"review_count",averageReviewCount:{$avg:"$review_count"}}}])

9.db.yelp.user.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1})

10.db.yelp.user.find({"elite":{"$ne":[]}}).sort({"elite":-1}).limit(1)

11.db.yelp.user.aggregate([{$group:{_id :"name",average:{$avg:{$size:"$elite"}}}}])
