import requests

def GetPaginatedList(url, accessToken, payload={}):
        """
        Returns a full list of Canvas items

        url - Canvas URL to access (string)
        accessToken - Canvas API access token (string)
        payload - payload dictionary for the Canvas API request (optional, default={})
        """
        
        authHeader = {'Authorization': 'Bearer ' + accessToken}
        
        itemList = []
        
        r = requests.get(url, headers=authHeader, data=payload)
        for item in r.json():
                itemList.append(item)
        
        while 'next' in r.links:
                r = requests.get(r.links['next']['url'], headers=authHeader, data=payload)
                for item in r.json():
                        itemList.append(item)
        
        return itemList


def UploadFile(url, accessToken, fileName, displayName=None):
        """
        Upload a file to Canvas

        url - Canvas URL to which file will be posted (string)
        accessToken - Canvas API access token (string)
        fileName - local file to upload (string)
        displayName - file name to show on Canvas (optional, default=fileName)
        """

        authHeader = {'Authorization': 'Bearer ' + accessToken}
        
        # Step 1
        payload = {}
        if displayName is not None: 
                payload = {'name': displayName}
        results = requests.post(url, headers=authHeader, data=payload)
        abc = results.json()
        
        # Step 2
        results = requests.post(abc['upload_url'], data=abc['upload_params'],  allow_redirects=False, files={'file': open(fileName,'rb')})
        abc = results.headers
        
        # Step 3
        results = requests.post(abc['location'], headers=authHeader)
        abc = results.json()
        
        if abc['upload_status'] != 'success':
                return -1
        return 0

def GetFolderID(courseURL, accessToken, folderName, makeFolder = True):
        """
        Find a folder ID within a course based on folder name

        courseURL - Canvas URL to course where folder is located (string)
        accessToken - Canvas API access token (string)
        folderName - name of folder to search (string)
        makeFolder - create the folder if not found (optional, default=True)

        Searches '{courseURL}/folders/by_path/{folderName}'
        """

        authHeader = {'Authorization': 'Bearer ' + accessToken}

        
        r = requests.get(courseURL + f'folders/by_path/{folderName}', headers=authHeader)
        if r.status_code == requests.codes.ok:
                folderList = r.json()
                folderID = folderList[-1]['id']
        elif makeFolder:
                payload = {'name': folderName, 'parent_folder_path': '/'}
                r = requests.post(courseURL + 'folders', headers=authHeader, data=payload)
                print(f'Creating folder {folderName}')
                folderInfo = r.json()
                folderID = folderInfo['id']

        return folderID
