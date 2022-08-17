# Movie-Recommendation-System
THE PROJECT IS CURRENT DEPLOYED ON AWS.
http://ec2-52-66-238-69.ap-south-1.compute.amazonaws.com:5000/

CURRENTLY I HAVE USED A WEBSITE MAKER NAMED NICEPAGE TO MAKE THE LAYOUT OF WEBSITE
I HAVE USED FLASK APP TO MAKE THE MOVIE RECOMMENDATION SYSTEM. DYNAMIC VARIABLES IN HTML IS USED USING JINJA

#PROCESS FOLLOWED
1. Collected the data from Kaggle.
2. Preprocessed the data.
3. Converted the desired features into a tag.
4. Applying Count Vectorizer using sklearn library.
5. Calculated the similarity index and sorted in descending order.
6. Using requests library to fetch the poster of movies
7. Fetching trending movies from movie_db api.
8. Creating Flask app to deploy it on server.
9. Created EC2 instance through Amazon Web Services and deployed the code.
