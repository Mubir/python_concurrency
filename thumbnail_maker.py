# thumbnail_maker.py
import time
import os
import logging
from urllib.parse import urlparse
from urllib.request import urlretrieve
import threading
import PIL
from PIL import Image
CustomFORMAT = "[%(threadName)s,%(asctime)s,%(levelname)s,%(message)s]"
logging.basicConfig(filename='logfile.log',
                    level=logging.DEBUG, format=CustomFORMAT)


class ThumbnailMakerService(object):
    def __init__(self, home_dir='.'):
        self.home_dir = home_dir
        self.input_dir = self.home_dir + os.path.sep + 'incoming'
        self.output_dir = self.home_dir + os.path.sep + 'outgoing'
        self.downloaded_bytes = 0
        # lock created
        self.dl_lock = threading.Lock()
        # seamaphore to limit max 4 donwload
        max_concurrent_dl=4
        self.dl_sem = threading.Semaphore(max_concurrent_dl)
        self.i=0

    def donwload_image(self, url):
        # acquireing semaphore
        # allows only 4 thread to run at same time;
        self.dl_sem.acquire()
        try:
            logging.info("downloading"+url)
            img_filename = urlparse(url).path.split('/')[-1]
            dest_path = self.input_dir + os.path.sep + img_filename
            urlretrieve(url, dest_path)
            img_size = os.path.getsize(dest_path)
            # as modifiying donwloaded_bytes this should be 
            # under lock so that every thread(single donwload)
            # can only use it then other thread can use it one
            # by one;
            with self.dl_lock:
                self.downloaded_bytes += img_size
            logging.info("image [{} bytes] saved to {}".format(img_size,dest_path))
        finally:
            # releasing semaphore
            self.dl_sem.release()
            self.i=self.i+1
            logging.info("do noting")

    def download_images(self, img_url_list):
        # validate inputs
        if not img_url_list:
            return
        os.makedirs(self.input_dir, exist_ok=True)

        logging.info("beginning image downloads")

        start = time.perf_counter()
        thread_list = []
        for url in img_url_list:
            t = threading.Thread(target=self.donwload_image, args=(url,))
            t.start()
            # dont call join cause that will stop creating new tr before this ends
            # so we add all to a list and then run join
            thread_list.append(t)
        
        for cr_t in thread_list:
            #i=i+1
            logging.info("############################## ")
            logging.info(self.i)
            cr_t.join()

        end = time.perf_counter()

        logging.info("downloaded {} images in {} seconds".format(
            len(img_url_list), end - start))

    def perform_resizing(self):
        # validate inputs
        if not os.listdir(self.input_dir):
            return
        os.makedirs(self.output_dir, exist_ok=True)

        logging.info("beginning image resizing")
        target_sizes = [32, 64, 200]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()
        for filename in os.listdir(self.input_dir):
            orig_img = Image.open(self.input_dir + os.path.sep + filename)
            for basewidth in target_sizes:
                img = orig_img
                # calculate target height of the resized image to maintain the aspect ratio
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                # perform resizing
                img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)

                # save the resized image to the output dir with a modified file name
                new_filename = os.path.splitext(filename)[0] + \
                    '_' + str(basewidth) + os.path.splitext(filename)[1]
                img.save(self.output_dir + os.path.sep + new_filename)

            os.remove(self.input_dir + os.path.sep + filename)
        end = time.perf_counter()

        logging.info("created {} thumbnails in {} seconds".format(
            num_images, end - start))

    def make_thumbnails(self, img_url_list):
        logging.info("START make_thumbnails")
        start = time.perf_counter()

        self.download_images(img_url_list)
        # self.perform_resizing()

        end = time.perf_counter()
        logging.info("END make_thumbnails in {} seconds".format(end - start))
