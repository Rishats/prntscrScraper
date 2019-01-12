import string, random, os, sys, _thread, httplib2, time
# from PIL import Image

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " (Number of threads)")
THREAD_AMOUNT = int(sys.argv[1])

INVALID = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]

if not os.path.isdir("images_jpg"):
    try:
        path = "images_jpg"
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

def scrape_pictures(thread):
    while True:
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        if length == 6:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
            url += '.jpg'

            filename = url.rsplit('/', 1)[-1]

            h = httplib2.Http('.cache' + thread)
            response, content = h.request(url)
            out = open(filename, 'wb')
            out.write(content)
            out.close()

            file_size = os.path.getsize(filename)
            if file_size in INVALID:
                print("[-] Invalid: " + url)
                os.remove(filename)
            else:
                print("[+] Valid: " + url)

for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(scrape_pictures, (thread,))
    except:
        print('Error starting thread ' + thread)
print('Succesfully started ' + thread + ' threads.')

while True:
    time.sleep(1)
