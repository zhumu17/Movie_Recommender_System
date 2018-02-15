# Movie Recommender system
This is a web application of recommending movies on both computer and mobile devices web browsers

# Python version and dependencies
This app is developed in Python 2.7

Dependencies include:
Flask==0.12.0
Jinja2==2.9.6
numpy==1.12.1
scipy==0.19.1
pandas==0.20.3
scikit-learn==0.19.0
beautifulsoup4==4.6.0
gunicorn==19.7.1


# Data preprocessing downloaded from MovieLens (if /DATA directory not exist):
1. download https://grouplens.org/datasets/movielens/100k/
2. unzip to a directory that is in the same root directory of this project folder
    The file system layout should be like:
    /project - mk-100/
           \ RecommenderSystem/

3. Inside RecommenderSystem/, run the Preprocessing.ipynb in the jupyter notebook
4. copy mk-100/DATA to RecommenderSystem/
    now all the original data is saved in /DATA directory

