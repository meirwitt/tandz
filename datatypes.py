


import requests
import os
import datetime as dt


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

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "duration": self.duration
        }
    
    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __hash__(self) -> int:
        return hash(self.id)