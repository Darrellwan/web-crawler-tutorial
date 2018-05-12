import requests
import warnings

# Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''


def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload).json()
    print(file['access_token'])  # to test what the FB api responded with
    return file['access_token']


if __name__ == '__main__':
    get_fb_token(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
