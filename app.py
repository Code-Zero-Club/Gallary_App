from flask import Flask, render_template, request, redirect, url_for
import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

# 이미지 모델
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Image {self.filename}>'

# 메인 페이지
@app.route('/')
def index():
    with app.app_context():
        images = Image.query.all()
    return render_template('index.html', images=images)

# 업로드 페이지
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # 데이터베이스에 이미지 정보 저장
            new_image = Image(filename=filename)
            db.session.add(new_image)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')

# 좋아요 기능
@app.route('/like/<int:image_id>', methods=['POST'])
def like_image(image_id):
    image = Image.query.get(image_id)
    image.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)