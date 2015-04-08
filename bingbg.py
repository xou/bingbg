import json
import urllib
import urllib2
import tempfile
import subprocess

def set_image_cmd(filename):
    return ['/usr/bin/feh', '--bg-scale', filename]

API_URL = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'

def get_current_image_data():
    """return the latest bing image data: A dictionary
    contining the keys 'url' and 'description' at least.
    url is relative to http(s)://bing.com/"""
    req = urllib2.urlopen(API_URL)
    data = req.read()
    req.close()
    # returned data is a list of images, choose the first one
    data = json.loads(data)['images'][0]
    return data


def fetch_image(url):
    """fetches the image to a temporary location.
    Returns that location."""
    target = tempfile.mkstemp(prefix='bingbg')[1]
    urllib.urlretrieve(url, target)
    return target


def set_image(filename):
    cmd = set_image_cmd(filename)
    ret = subprocess.call(cmd)
    if ret:
        raise RuntimeError("Something went wrong when executing %r", cmd)


def main():
    data = get_current_image_data()
    url = 'http://bing.com/' + data['url']
    filename = fetch_image(url)
    set_image(filename)

def loop():
    """calls main(), waits for 24 hours to have passed,
    then calls main() again.

    The function actually wakes up more often than that,
    since the PC might spend some time in suspend/hibernate
    (standby), and i'm not sure how time.sleep() is affected
    by that."""
    while True:
        cur_time = time.time()
        wakeup_at = cur_time + (60*60*24)

        while time.time() < wakeup_at:
            time.sleep(300) # sleep for five minutes

        main()

if __name__ == "__main__":
    import sys, time
    main()

    if '-l' in sys.argv:
        loop()

