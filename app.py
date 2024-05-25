from flask import Flask, render_template, request
import pickle
import numpy as np
popular_df = pickle.load(open('E:/ANISHA/projects/major_project/popular.pkl', 'rb'))
pt = pickle.load(open('E:/ANISHA/projects/major_project/pt.pkl', 'rb'))
books = pickle.load(open('E:/ANISHA/projects/major_project/books.pkl', 'rb'))
similarity_scores = pickle.load(open('E:/ANISHA/projects/major_project/similarity_scores.pkl', 'rb'))
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['book_title'].values),
                           author = list(popular_df['book_author'].values),
                           image = list(popular_df['image_url_m'].values),
                           votes = list(popular_df['num_ratings'].values),
                           ratings = list(popular_df['avg_ratings'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books', methods = ['POST'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input not in pt.index:
        print("Book not found in the index.")
        return "Book not found in the index."
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['book_title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('book_title')['book_title'].values))
        item.extend(list(temp_df.drop_duplicates('book_title')['book_author'].values))
        item.extend(list(temp_df.drop_duplicates('book_title')['image_url_m'].values))
        data.append(item)
    print(data)
    return render_template('recommend.html', data = data)
if __name__ == '__main__':
    app.run(debug = True)