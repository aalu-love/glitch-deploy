from flask import Flask, request, jsonify
from ntscraper import Nitter
import re

app = Flask(__name__)
scraper = None
profile_info = None

def is_valid_username(username):
    # Twitter usernames can contain only letters, numbers, and underscores
    # with a length between 1 and 15 characters
    pattern = re.compile("^[a-zA-Z0-9_]{1,15}$")
    return bool(pattern.match(username))

@app.route('/', methods=['GET'])
def home():
    return "working..."

@app.route('/get_profile_info', methods=['GET'])
def get_profile_info():
    global scraper
    if not scraper:  # Check if scraper is not initialized
        return "Instance not ready yet."
        scraper = Nitter()  # Initialize scraper if it's None
    username = request.args.get('username')
    # username = "messeduppcs"
    if username:
        # Define an asynchronous function to fetch the profile info
        if not is_valid_username(username):
            return jsonify({'error': 'Invalid username.'}), 400

        profile_info = scraper.get_profile_info(username)

        return jsonify(profile_info)
    else:
        return jsonify({'error': 'Username parameter is missing.'}), 400

@app.route('/get_tweets', methods=['GET'])
def get_tweets():
    usernames = request.args.getlist('username')
    number = int(request.args.get('number', default=5))

    if not usernames:
        return jsonify({'error': 'Usernames parameter is missing.'}), 400

    if not is_valid_username(usernames):
        return jsonify({'error': 'Invalid usernames.'}), 400

    tweets = scraper.get_tweets(usernames, mode="user", number=number)
    return jsonify(tweets)

if __name__ == '__main__':
    scraper = Nitter()  # Initialize scraper in the __main__ function
    app.run(host="0.0.0.0", debug=True)
