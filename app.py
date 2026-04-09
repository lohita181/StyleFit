from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import pickle
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from config import Config
from models import db, User, WardrobeItem
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
    
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables if they don't exist
# with app.app_context():
#     db.create_all()

# ── Create upload dirs on startup ──────────────────────────────────────────────
# os.makedirs(app.config['TOP_UPLOAD_FOLDER'],    exist_ok=True)
# os.makedirs(app.config['BOTTOM_UPLOAD_FOLDER'], exist_ok=True)

# ── Load models safely ─────────────────────────────────────────────────────────
def load_models():
    try:
        top_model    = tf.keras.models.load_model(app.config['TOP_MODEL_PATH'])
        bottom_model = tf.keras.models.load_model(app.config['BOTTOM_MODEL_PATH'])

        with open(app.config['TOP_LABELS_PATH'], 'rb') as f:
            top_labels = pickle.load(f)
        with open(app.config['BOTTOM_LABELS_PATH'], 'rb') as f:
            bottom_labels = pickle.load(f)

        print("✅ Models and labels loaded successfully")
        return top_model, bottom_model, top_labels, bottom_labels

    except Exception as e:
        print(f"❌ Failed to load models: {e}")
        raise SystemExit(1)   # stop the app cleanly instead of a cryptic crash

top_model, bottom_model, top_labels, bottom_labels = load_models()

# ── Helpers ────────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    )

def predict_occasion(img_path, model, labels):
    img  = image.load_img(img_path, target_size=(224, 224))
    arr  = image.img_to_array(img)
    arr  = np.expand_dims(arr, axis=0)
    arr  = preprocess_input(arr)
    preds = model.predict(arr)[0]
    return labels[np.argmax(preds)]

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/topupload', methods=['GET', 'POST'])
@login_required
def upload_top():
    message = None
    if request.method == 'POST':
        files = request.files.getlist('top-upload')
        saved = []
        for file in files:
            if file and allowed_file(file.filename):
                folder = Config.user_upload_dir(current_user.id, 'tops')
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, file.filename)
                file.save(save_path)

                # run inference immediately
                occasion = predict_occasion(save_path, top_model, top_labels)

                # web-relative path for <img src>
                web_path = save_path.replace("\\", "/")
                web_path = web_path[web_path.index("static/"):]

                # save to DB
                item = WardrobeItem(
                    user_id  = current_user.id,
                    filename = file.filename,
                    filepath = web_path,
                    type     = 'top',
                    occasion = occasion
                )
                db.session.add(item)
                saved.append(file.filename)

        db.session.commit()
        message = f"✅ Uploaded: {', '.join(saved)}" if saved else "⚠️ No valid files uploaded."
    return render_template('topupload.html', message=message)


@app.route('/bottomupload', methods=['GET', 'POST'])
@login_required
def upload_bottom():
    message = None
    if request.method == 'POST':
        files = request.files.getlist('bottom-upload')
        saved = []
        for file in files:
            if file and allowed_file(file.filename):
                folder = Config.user_upload_dir(current_user.id, 'bottoms')
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, file.filename)
                file.save(save_path)

                occasion = predict_occasion(save_path, bottom_model, bottom_labels)

                web_path = save_path.replace("\\", "/")
                web_path = web_path[web_path.index("static/"):]

                item = WardrobeItem(
                    user_id  = current_user.id,
                    filename = file.filename,
                    filepath = web_path,
                    type     = 'bottom',
                    occasion = occasion
                )
                db.session.add(item)
                saved.append(file.filename)

        db.session.commit()
        message = f"✅ Uploaded: {', '.join(saved)}" if saved else "⚠️ No valid files uploaded."
    return render_template('bottomupload.html', message=message)

@app.route('/occasion')
@login_required
def occasion():
    return render_template('occasion.html')

@app.route('/result', methods=['POST'])
@login_required
def result():
    selected_occasion = request.form.get('selected_occasion')
    mapped_occasion   = app.config['OCCASION_MAPPING'].get(selected_occasion)

    tops = WardrobeItem.query.filter_by(
        user_id  = current_user.id,
        type     = 'top',
        occasion = mapped_occasion
    ).all()

    bottoms = WardrobeItem.query.filter_by(
        user_id  = current_user.id,
        type     = 'bottom',
        occasion = mapped_occasion
    ).all()

    matched_outfits = [
        (top.filepath, bottom.filepath)
        for top in tops
        for bottom in bottoms
    ]

    return render_template('result.html', occasion=selected_occasion, matched_outfits=matched_outfits)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email    = request.form.get('email').strip().lower()
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already registered.')

        hashed = generate_password_hash(password)
        user   = User(email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('about'))

    return render_template('register.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email').strip().lower()
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return render_template('login.html', error='Invalid email or password.')

        login_user(user)
        return redirect(url_for('about'))

    return render_template('login.html', error=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/wardrobe')
@login_required
def wardrobe():
    tops = WardrobeItem.query.filter_by(
        user_id = current_user.id,
        type    = 'top'
    ).order_by(WardrobeItem.created_at.desc()).all()

    bottoms = WardrobeItem.query.filter_by(
        user_id = current_user.id,
        type    = 'bottom'
    ).order_by(WardrobeItem.created_at.desc()).all()

    return render_template('wardrobe.html', tops=tops, bottoms=bottoms)


@app.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = WardrobeItem.query.get_or_404(item_id)

    # make sure users can only delete their own items
    if item.user_id != current_user.id:
        return 'Unauthorized', 403

    # delete file from disk
    full_path = os.path.join(BASE_DIR, item.filepath)
    if os.path.exists(full_path):
        os.remove(full_path)

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('wardrobe'))

if __name__ == '__main__':
    app.run(debug=True)