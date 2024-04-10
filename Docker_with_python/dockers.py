
# definition of docker properties here
import docker 

class Docker:
    def __init__(self) -> None:
        self.client = docker.from_env()
class Image(Docker):
    def __init__(self):
        super().__init__()
    
    def display_all_images(self, name: str=None, all: bool=True)-> list:
        return self.client.images.list(name, all=all)

        
    def display_image(self, image_name: str) -> str:
        return self.client.images.get(image_name)
    
    def pull_image(self, repository: str):
        self.client.images.pull(repository)
    
    def push_image(self, repository:str, tag:str = None) -> str:
        return self.client.images.push(repository, tag=tag)
    
    def remove_image(self, image: str) ->str:
        return self.client.images.remove(image)
    
    def search_image(self, term: str, limit: int)-> list:
        return self.client.images.search(term,limit)

    def tag_image(self, repository: str, tag: str, force: bool)->bool:
        return self.client.images.tag(repository,tag,force)
    
    def build_image(self, path: str, tag: str):
        return self.client.images.build(path=path, tag=tag)
    
 
    
class Container(Docker):
        def __init__(self):
            super().__init__()

        def run_container(self, image: str,detach : bool = True):
            return self.client.containers.run(image, detach=detach)
            
        
        def create_container(self, image: str, command: None)->str:
            return self.client.containers.create(image, command)
        
        def display_all_container(self, all: bool=True, since: str =None, before: str=None,limit: int=-1)->list:
            return self.client.containers.list(all=all,since=since, before=before, limit=limit)
        
        def start_container(self, container_name:str):
            return self.client.containers.get(container_name).start()
        
        def stop_container(self, container_name:str):
            return self.client.containers.get(container_name).stop()
        
        def restart_container(self, container_name:str, time_out:int=10):
            return self.client.containers.get(container_name).restart(time_out=time_out)
        
    


