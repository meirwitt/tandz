import os
from selenium import webdriver
import requests
import time
from selenium.webdriver.common.by import By
import datetime as dt

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument("--log-level=3")

def download_soundtrack(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            # Save the data to the specified path
            with open(save_path, "wb") as f:
                f.write(response.content)
            print("Soundtrack downloaded successfully.")
        else:
            print(f"Failed to download the soundtrack. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))


class Tandz:

    id: str
    name: str
    url: str
    duration: int

    def __init__(self, id, name, duration):
        self.id = id
        self.name = name
        pref = "https://d2jti1fb5f3g5g.cloudfront.net/46434_"
        # mid = "64b526ea283232f7f876a946"
        suf = ".mp3"
        self.url = pref + id + suf
        self.date = ""
        self.duration = duration

    def download(self):
        try:
        # Send a GET request to the URL
            response = requests.get(self.url)
            # get current directory
            save_path = os.getcwd()
            # append the Downloads folder. make sure it compatible with linux and windows
            save_path = save_path + "\\Downloads"
            # save_path = save_path + "/Downloads"
            # check if the folder exists
            if not os.path.exists(save_path):
                # if not create it
                os.makedirs(save_path)



            if response.status_code == 200:
                # Save the data to the specified path
                # save it with the name of the file, if it doesn't exist create it
                save_path = save_path + "\\" + self.name + ".mp3" 
                # save_path = save_path + "\\" + "meir" + ".mp3" 
                with open(save_path, "wb+") as f:
                    f.write(response.content)  

                # with open(save_path, "wb+") as f:
                #     f.write(response.content)
                # print("Soundtrack downloaded successfully.")
            else:
                print(f"Failed to download the soundtrack. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
        except OSError as e:
            print("Error occurred:", str(e))
        except Exception as e:
            print("Error occurred:", str(e))
    
    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __hash__(self) -> int:
        return hash(self.id)

def download_soundtrack_with_selenium(url, start_time=None):
    # Set up the Selenium webdriver (here we use Chrome)
    driver = webdriver.Chrome(options=option)

    # Navigate to the webpage containing the soundtrack
    driver.get(url)
    the_list_of_ids = set()
    counter = 0
    last_length = 0
    t = 1
    while True and counter < 5:
        
        posts_list = driver.find_elements("class name", "posts_list")[0]
        # pc_list = posts_list.find_elements("xpath", "//li")
        pc_list = posts_list.find_elements("class name", "post-item")
        
        if len(pc_list) == last_length:
            counter += 1
        else:
            counter = 0

        if last_length > 100*t:
            t += 1
            print(f"found {last_length} tracks until now...", end="\r")

        

        # first scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # wait for the page to load
        time.sleep(3)




        last_length = len(pc_list)

        

    # raw tracks
    scroling_time = time.time() - start_time
    print(f"done scrolling, found {last_length}\nelapsed time: {round(scroling_time/60)} minutes")

    print("building set of ids...")
    for item in pc_list:
        if str(item.get_attribute("class")).startswith('post-item post_list'):
            player_cover_url = item.find_element("class name", "playandTime").find_element("class name", "player_cover").get_attribute("src")

            player_cover_id = player_cover_url.split("id=")[1].split(".")[0]
            title = ",".join(item.find_element("class name", "item_link_play").text.split(",")[1:])
            desc = item.find_element("class name", "edt-name").text
            minutes = int(item.find_element("class name", "playandTime").text.split(":")[0])
            
            if minutes > 50 and minutes < 150:
                name = (str(title + " - " + desc).encode("utf-8")).decode("utf-8")
                tandz_item = Tandz(player_cover_id, name, minutes)
                the_list_of_ids.add(tandz_item)
                

    set_building_time = time.time() - start_time
    print(f"found {len(the_list_of_ids)} items for download, elapsed time: {round(set_building_time/60)} minutes")
    print("downloading...")
    mean_time = 0
    down_until_now = 0
    for item in the_list_of_ids:
        down_timer = time.time()
        item.download()
        down_until_now += 1
        download_one_time = time.time() - down_timer

        mean_time = (mean_time * (down_until_now - 1) + download_one_time) / down_until_now
        minutes_left = (len(the_list_of_ids) - down_until_now) * mean_time / 60
        # calculate the time now + the time left in readable format
        tt = (dt.datetime.now() + dt.timedelta(minutes=minutes_left)).strftime("%H:%M:%S")

        # datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()+minutes_left*60)
        print(f"Downloaded {down_until_now}/{len(the_list_of_ids)}, estimated time left: {round(minutes_left)} minutes: {tt} ", end="\r")
        # mean_time += time.time() - down_timer

    print("\n", end="")


    print(f"Downloading complete")

        
        


if __name__ == "__main__":
    # mesure the time the program runs in minutes
    # print((dt.datetime.now() + dt.timedelta(minutes=10)).strftime("%H:%M:%S"))
    start_time = time.time()
    download_soundtrack_with_selenium("https://102fm.co.il/tandz", start_time)
    
    print("--- %s seconds ---" % (round(time.time() - start_time)))
