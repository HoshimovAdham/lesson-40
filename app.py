from flask import Flask, render_template, request, redirect
import mysql.connector
import settings  

app = Flask(__name__)

db = mysql.connector.connect(
    host=settings.HOST,
    user=settings.USER,
    password=settings.PASSWORD,
    database=settings.DB_NAME
)

def create_database():
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library")
    cursor.execute("USE library")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            pages INT,
            published_year INT
        )
    """)
    db.commit()

create_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        published_year = request.form['published_year']

        cursor = db.cursor()
        sql = "INSERT INTO books (title, author, pages, published_year) VALUES (%s, %s, %s, %s)"
        val = (title, author, pages, published_year)
        cursor.execute(sql, val)
        db.commit()
        return redirect('/books')
    return render_template('add_book.html')

@app.route('/books')
def books():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True, port=8500)
