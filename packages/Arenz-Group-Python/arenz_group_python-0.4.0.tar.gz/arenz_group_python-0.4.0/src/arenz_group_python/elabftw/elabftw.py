from pathlib import Path
import elabapi_python
import os
from arenz_group_python import Project_Paths
import warnings

EXPERIMENTS_API = elabapi_python.ExperimentsApi()
#api_client = elabapi_python.ApiClient()

API_KEY_NAME = 'elab_API_KEY'
API_HOST_URL = 'https://elabftw.dcbp.unibe.ch/api/v2'


class entry:
    def __init__(self, ID, path, title, uploads): 
        self.ID = ID
        self.path = path
        self.title = title
        self.uploads = len(uploads)

def fix_title(title):
    
    return str(title).replace(":", "-").replace("\\", "-").replace("/", "-").replace(" ", "_")




class elabFTW_wrapper:
    def __init__(self):
        self.connected = False
        self.api_client = None
        self.EXPERIMENTS_API = EXPERIMENTS_API
        self.API_HOST_URL = API_HOST_URL
        
    def get_experiments_api(self):
        if self.isConnected():
            return EXPERIMENTS_API
        
    def isConnected(self):
        if not self.connected:
            print("Connection has not been established to the data base. Run 'connect' first.")
        return self.connected
    
    def connect_to_database(self, verify_ssl = False):
        
        API_KEY = os.getenv('elab_API_KEY')
        global API_HOST_URL
        url = os.getenv('elab_API_HOST')
        if url is not None:
            API_HOST_URL = url
        if API_KEY is None:
            raise ValueError("'elab_API_KEY' environment variable not set in '.env'.")
        if API_HOST_URL is None:
            raise ValueError("elab_API_HOST environment variable not set in '.env'.")  
        
    # Configure the api client
        configuration = elabapi_python.Configuration()
        configuration.api_key['api_key'] = API_KEY
        configuration.api_key_prefix['api_key'] = 'Authorization'
        configuration.host = API_HOST_URL
        configuration.debug = False
        configuration.verify_ssl = verify_ssl

        
        # For convenience, mask the warnings about skipping TLS verification
        if not configuration.verify_ssl:
            import urllib3
            urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

        # create an instance of the API class
        
        self.api_client = elabapi_python.ApiClient(configuration)
        # fix issue with Authorization header not being properly set by the generated lib
        self.api_client.set_default_header(header_name='Authorization', header_value=API_KEY)

        self.connected = True
        #### SCRIPT START ##################

        info_client = elabapi_python.InfoApi(self.api_client)
        api_response = info_client.get_info()
        if api_response is not None:
            print("Connected to DB.")
        # Load the experiments api
            global EXPERIMENTS_API 
            self.EXPERIMENTS_API = elabapi_python.ExperimentsApi(self.api_client)
            #print(EXPERIMENTS_API.api_client.configuration.host)
        
    
    
    def api_read_experiments(self, *args, **kwargs):
        """_summary_
            
            :param str q: Search for a term in title, body or elabid. 
        Returns:
            list: experiments
        """
        if self.isConnected():
            return self.EXPERIMENTS_API.read_experiments(**kwargs)

    def api_get_experiment(self,ID,**kwargs):
        if self.isConnected():
            return self.EXPERIMENTS_API.get_experiment(ID,**kwargs)
     
    def get_struct(self,ID,parentpath=Project_Paths().rawdata_path):
        if  self.isConnected():
            exp = self.api_get_experiment(ID)
            #entries.append(entry(exp.id, parentpath / exp.title, exp.title, exp.uploads))
            title =fix_title(exp.title)
            entries = [entry(exp.id, parentpath, title, exp.uploads)]
            for j in exp.related_experiments_links:
                if j.entityid != ID:
                    entries.extend(self.get_struct(j.entityid, parentpath / title ))
            return entries    
        
            
    def create_experiment_directory(self,experimentID, path_to_parentdir):
        if self.isConnected():
            exp = self.api_get_experiment(experimentID)
            path_to_dir = Path(path_to_parentdir) / fix_title(exp.title)
            if not path_to_dir.exists():
                os.makedirs(path_to_dir)
            return path_to_dir
        

    def download_experiment_info(self,experimentID, fileEnding="json",path_to_dir=Path.cwd()):
        if self.isConnected():
            exp = self.api_get_experiment(experimentID)
            title = fix_title(exp.title)
            
            filename = f'{title}.{fileEnding}'
            if path_to_dir:
                path_to_dir = Path(path_to_dir)
                if not path_to_dir.exists():
                    os.makedirs(path_to_dir)
                    
            if path_to_dir:
                path_to_file  = Path(path_to_dir) / filename
            else:
                path_to_file = filename
            print(f'\t\tSaving file "{filename}"')
            with open(path_to_file, 'wb') as file:
                # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
                file.write(self.EXPERIMENTS_API.get_experiment(exp.id, format=fileEnding, _preload_content=False).data)
            

    def download_experiment_pdf(self,experimentID, path_to_dir=Path.cwd()):
        return self.download_experiment_info(experimentID, fileEnding="pdf", path_to_dir=path_to_dir)
            
    def download_experiment_json(self,  experimentID, path_to_dir=Path.cwd()):
        return self.download_experiment_info(experimentID, fileEnding="json", path_to_dir=path_to_dir)
        
###################################################################################################
    def download_experiment_dataFiles(self,experimentID, path_to_dir):
        exp = self.api_get_experiment(experimentID)
        
        if path_to_dir:
            path_to_dir = Path(path_to_dir)
            if not path_to_dir.exists():
                print(f'Create directory {path_to_dir} first')
                return
                
            ##############################   
            uploadsApi = elabapi_python.UploadsApi(self.api_client)

            # get experiment with ID 256
            exp = self.api_get_experiment(experimentID)
            # upload the file 'README.md' present in the current folder
            # display id, name and comment of the uploaded files
            if len(exp.uploads) == 0:
                print('\t\tNo uploads found')
                return
            else:
                print(f'\t\tFound {len(exp.uploads)} uploads')
                index = 0
                for upload in uploadsApi.read_uploads('experiments', exp.id):
                    index = index+1
                    print("\t\t", index,"\t", upload.id, upload.real_name, upload.comment)
                    #get and save file
                    path_to_file = path_to_dir / upload.real_name
                    with open(path_to_file, 'wb') as file:
                        # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
                        file.write(uploadsApi.read_upload('experiments', experimentID, upload.id, format='binary', _preload_content=False).data)
        else:
            print('Directory not defined')
            return    
    

    def download_experiment_single(self,experimentID,path_to_parent):
        dir = self.create_experiment_directory(experimentID,path_to_parent )
        self.download_experiment_pdf(experimentID,dir)
        self.download_experiment_json(experimentID,dir)
        self.download_experiment_dataFiles(experimentID,dir)    
    
    def create_structure_and_download_experiments(self,experimentID):
        experiment_structure = self.get_struct(experimentID, Project_Paths().rawdata_path)
        print("Found", len(experiment_structure), "experiments")
        for i,obj in enumerate(experiment_structure):
            path=Path(obj.path) / fix_title(obj.title)
            relpath = path.relative_to(Project_Paths().rawdata_path.parent.parent)
            print(f"----{i+1}/{len(experiment_structure)}------------------ID=", obj.ID, f"\t<Project>\{relpath}")
            self.download_experiment_single(obj.ID,obj.path)



