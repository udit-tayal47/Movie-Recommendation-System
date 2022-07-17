import pickle
import pandas as pd
import requests
import bz2
from flask import Flask ,render_template,request

TEMPLATE_DIR = r"/home/ubuntu/templates"
STATIC_DIR = r"/home/ubuntu/templates/static"


data = pickle.load(open('movie.pkl','rb'))
frame = pd.DataFrame(data)
movies = frame['title']
ifile = bz2.BZ2File("similarity.pkl",'rb')
similarity = pickle.load(ifile)
ifile.close()


trending = requests.get("https://api.themoviedb.org/3/trending/all/day?api_key=254afe6344db3d15ba4b1ed7143d63f3")
trending = trending.json()
trending_data = pd.DataFrame(trending)
trending_title = []
trending_poster_url = []
trending_imbd_url = []
for i in range(20):
    try:
        x = trending_data['results'][i]['title']
        trending_title.append(x)
        y = trending_data['results'][i]['poster_path']
        url = f"https://image.tmdb.org/t/p/w185/{y}"
        trending_poster_url.append(url)
        trending_movie_id = trending_data['results'][i]['id']
        response = requests.get(f"https://api.themoviedb.org/3/movie/{trending_movie_id}?api_key=254afe6344db3d15ba4b1ed7143d63f3")
        data = response.json()
        imdb_id = data["imdb_id"]
        z = f"https://www.imdb.com/title/{imdb_id}/"
        trending_imbd_url.append(z)

    except:
        i=i+1


app = Flask(__name__ ,template_folder=TEMPLATE_DIR,static_folder=STATIC_DIR)
app.config['PROPAGATE_EXCEPTIONS'] = True
@app.route('/',methods=['POST','GET'])
def hello_world():
    new = []
    recommended_title = []
    recommended_movie_poster = []
    imdb_url = []
    if request.method == "GET":
        recommended_movie_poster = trending_poster_url[6:12]
        recommended_title = trending_title[6:12]
        imdb_url = trending_imbd_url[6:12]
    if request.method == "POST":
        movie = request.form.get("search")    
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
            imdb_id = data["imdb_id"]
            fetch_poster_url = f"https://image.tmdb.org/t/p/w185/{poster}"
            fetch_imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
            recommended_movie_poster.append(fetch_poster_url)
            imdb_url.append(fetch_imdb_url)

    
    return render_template('index.html',item = movies ,title = recommended_title,poster=recommended_movie_poster,
    trending_poster_url = trending_poster_url ,trending_title=trending_title,imdb_url=imdb_url,trending_imbd_url=trending_imbd_url)




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
