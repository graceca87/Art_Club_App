import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'temporary password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

IMG_FOLDER = os.path.join('static', 'IMG')

# store cloudinary vars in local environment
os.environ['CLOUD_NAME'] = "dtxjqazzg"
os.environ['API_KEY'] = "362937972547594"
os.environ['API_SECRET'] = "0nambxAqIE5U6fpE1fKy9w-j82k"


# CLOUD_NAME="dtxjqazzg"
# API_KEY="362937972547594"
# API_SECRET="0nambxAqIE5U6fpE1fKy9w-j82k"