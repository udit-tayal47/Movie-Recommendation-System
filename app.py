import pickle
import pandas as pd
import requests
from flask import Flask ,render_template,request

TEMPLATE_DIR = r"C:\Users\dhc\Desktop\VS CODE\PYTHON\DATA SCIENCE\MACHINE LEARNING\MOVIE RECOMMENDATION\templates"
STATIC_DIR = r"C:\Users\dhc\Desktop\VS CODE\PYTHON\DATA SCIENCE\MACHINE LEARNING\MOVIE RECOMMENDATION\templates\static"


data = pickle.load(open('movie.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
frame = pd.DataFrame(data)
movies = frame['title']


trending = requests.get("https://api.themoviedb.org/3/trending/all/day?api_key=254afe6344db3d15ba4b1ed7143d63f3")
trending = trending.json()
trending_data = pd.DataFrame(trending)
trending_title = []
trending_poster_url = []
for i in range(15):
    try:
        x = trending_data['results'][i]['title']
        trending_title.append(x)
        y = trending_data['results'][i]['poster_path']
        url = f"https://image.tmdb.org/t/p/w185/{y}"
        trending_poster_url.append(url)
    except:
        i=i+1


app = Flask(__name__ ,template_folder=TEMPLATE_DIR,static_folder=STATIC_DIR)

@app.route('/',methods=['GET','POST'])
def hello_world():
    new = []
    recommended_title = []
    recommended_movie_poster = []
    if request.method == "POST":
        movie = request.form.get("search")
        print(movie)
        index = frame[frame['title'] == movie].index[0]
        new = enumerate(similarity[index].tolist())
        new = sorted(new ,reverse=True ,key=lambda x:x[1])[1:7]
        print(new)
        id = []
        for i,j in new:
            id.append(frame['id'][i])
        for i,j in new:
            x = frame['title'][i]
            recommended_title.append(x)
        for i in id:
            response = requests.get(f"https://api.themoviedb.org/3/movie/{i}?api_key=254afe6344db3d15ba4b1ed7143d63f3")
            data = response.json()
            poster = data["poster_path"]
            fetch_poster_url = f"https://image.tmdb.org/t/p/w185/{poster}"
            recommended_movie_poster.append(fetch_poster_url)

    
    return render_template('index.html',item = movies ,title = recommended_title,poster=recommended_movie_poster,
    trending_poster_url = trending_poster_url ,trending_title=trending_title)




if __name__ == '__main__':
    app.run(port=3000,debug=True)

