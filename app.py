from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory
from forms import BlogPostForm
from models import BlogPost
from database import init_db, db
from werkzeug.utils import secure_filename
import os
import re
import random


app = Flask(__name__)

app.config['POSTGRES_USER'] = os.getenv("POSTGRES_USER")
app.config['POSTGRES_PASSWORD'] = os.getenv("POSTGRES_PASSWORD")
app.config['POSTGRES_DB'] = os.getenv("POSTGRES_DB")
app.config['POSTGRES_HOST'] = 'postgres'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join('uploads')


init_db(app)

@app.route('/')
def home():
    return 'Hello, World! This is Atef!'

@app.route('/blog')
def blog():
    posts = BlogPost.query.all()
    return render_template('blog_main.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post_form():
    form = BlogPostForm()  # Create form instance
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        slug = unique_slug(title)
        image_file = request.files.get('image')  

        if image_file and image_file.filename:  
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)
            image_url = url_for('uploaded_file', filename=filename)
        else:
            random_number = random.randint(1, 10)
            filename = f"bloggenricbg{random_number}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_url = url_for('uploaded_file', filename=filename)

        try:
            new_post = BlogPost(title=title, slug=slug, content=content, image_url=image_url)
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('blog'))  # redirect to the blog page
        except Exception as e:
            print("Failed to add post:", e)
            flash(f'Failed to add post: {e}', 'danger')
            return redirect(url_for('new_post_form'))
    return render_template('create_post.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/post/<slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)


# Helper functions
# ----------------

def slugify(title):
    words = title.split()[:10]
    slug = '-'.join(words)
    slug = re.sub(r'\W+', '-', slug).lower()
    return slug

def unique_slug(title):
    base_slug = slugify(title)
    unique_slug = base_slug
    counter = 1
    while BlogPost.query.filter_by(slug=unique_slug).first():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    return unique_slug

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)