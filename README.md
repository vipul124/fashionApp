# fashionApp

## Setup
- Create a `.env` file in the root of this folder with the following variables:
```
DATABASE_URL=your_postgres_database_url
```
- Install dependencies using - `pip3 install -r requirements.txt`
- Run the server
```
cd fashionApp

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

## APIs
1. For retrieving all the videos in JSON format
   - **GET** `/api/getAllVideos/`
   - Sample Response - [sample.txt](/sample.txt)

2. For uploading data to the database
   - **POST** `/api/user/` - _just dummy ones for testing purposes for now, can implement authentication and better endpoints later_
   - **POST** `/api/store/`
   - **POST** `/api/product/` - _for mentioning store you need to only pass the id of store as it is an independent thing. but for variants you need to pass a whole json object (kept this as vareints are different for different product)_
   - **POST** `/api/music/` - _was thinking to integrate with the video thing itself as done with variants but if you want to create something kindoff INSTAGRAM REELS for FASHION thing, a seperate API must be a better idea_
   - **POST** `/api/music/` - _for user and music you just need to pass the id of them and for products you can pass a list of product ids_


## Design Ideas
1. Models and Model Relationships -
   - Used **6** different models for `User`, `Store`, `Variant`, `Product`, `Music` and `Video` because each of them had there own seperate unique identifier (id) so it was a wise choice to keep them as seperate models [ [models.py](/fashionApp/home/models.py) ]
   - Created 2 different serialization logics - one for creating the database object which can handle other object's referenced ids and store it as a relation ship [ [here](https://github.com/vipul124/fashionApp/blob/648905cceca5dafde6caefb1a3354d68fb8dea6c/fashionApp/home/serializers.py#L5C1-L60C27) ] - and another one for viewing the data in expanded form instead of just their ids, done only for models which actually had some referencing to other models, like `Product` and `Video` [ [here](https://github.com/vipul124/fashionApp/blob/648905cceca5dafde6caefb1a3354d68fb8dea6c/fashionApp/home/serializers.py#L63C1-L81C27) ]
  
2. Optimizations and Pagination -
    -  Implemented PageNumberPagination as per the mentioned format in the task [ [here](https://github.com/vipul124/fashionApp/blob/648905cceca5dafde6caefb1a3354d68fb8dea6c/fashionApp/home/views.py#L15C1-L34C11) ] - prevents performance bottlenecks caused by very high requests from the users (also max capped the pagination limit to 100)
    -  Added a caching for 5 minutes [ [here](https://github.com/vipul124/fashionApp/blob/648905cceca5dafde6caefb1a3354d68fb8dea6c/fashionApp/home/views.py#L45C4-L48C49) ] - minimizes the database hits and API's latency which can help to improve the scalability
    -  Database Optimization - One is having better model-model relationships which is already explained above and the 2nd thing is adding django's db optimization methods (_I don't have much idea about this thing but googled and found out that this is one of the ways to optimize the database queries_) [ [here](https://github.com/vipul124/fashionApp/blob/648905cceca5dafde6caefb1a3354d68fb8dea6c/fashionApp/home/views.py#L39) ]
