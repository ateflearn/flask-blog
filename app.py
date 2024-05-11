from flask import Flask, render_template, url_for, flash, redirect, request
from forms import BlogPostForm
from models import BlogPost
from database import init_db, db
import os
import re

app = Flask(__name__)

app.config['POSTGRES_USER'] = os.getenv("POSTGRES_USER")
app.config['POSTGRES_PASSWORD'] = os.getenv("POSTGRES_PASSWORD")
app.config['POSTGRES_DB'] = os.getenv("POSTGRES_DB")
app.config['POSTGRES_HOST'] = 'postgres'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


init_db(app)

@app.route('/')
def home():
    return 'Hello, World! This is Atef!'

@app.route('/post/new', methods=['GET', 'POST'])
def new_post_form():
    form = BlogPostForm()  # Create form instance
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        slug = slugify(title)  # Generate slug from the title
        try:
            new_post = BlogPost(title=title, slug=slug, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('blog'))  # redirect to the blog page
        except Exception as e:
            print("Failed to add post:", e)
            flash(f'Failed to add post: {e}', 'danger')
            return redirect(url_for('new_post_form'))
    return render_template('create_post.html', form=form)


@app.route('/blog')
def blog():
    posts = BlogPost.query.all()
    return render_template('blog_main.html', posts=posts)

def slugify(title):
    words = title.split()[:10]
    slug = '-'.join(words)
    slug = re.sub(r'\W+', '-', slug).lower()
    return slug

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)