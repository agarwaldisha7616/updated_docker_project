import streamlit as st 
from dockers import Image,Container
from datetime import datetime
import requests


st.set_page_config(page_title="Docker Manager", page_icon="🚢",layout="wide")

def main_page():
    st.sidebar.markdown("Docker Manager 🐟")
def chat_bot():
    st.sidebar.header(" Chat Bot 🤖")
    
def conversational():
    st.sidebar.header("Co-pilot 💻r ")


page_names_to_funcs = {
    "Main Page": main_page,
    "Chat Bot": chat_bot,
    "Conversational": conversational,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()


#instance of an image
image = Image()
#image of container
container_object = Container()

st.title(":blue[Docker Manager] by Tech Army! 🇮🇳 ")

st.divider()


st.header(":blue[Docker Images]")

st.divider()

repo, tag, image_id, created, size = st.columns(5,gap="medium")

repo.subheader("Repository")
tag.subheader("Tag")
image_id.subheader("Image ID")
created.subheader("Created At")
size.subheader("Size")


for img in image.display_all_images(): 
    #preprocessing
    docker_img_attributes = img.attrs 
    repo_tag = docker_img_attributes["RepoTags"][0]
    repo_name,repo_version = repo_tag.split(":")
    docker_img_attributes["Created"] = docker_img_attributes["Created"].split("T")[0]
    dt = datetime.strptime(docker_img_attributes["Created"],"%Y-%m-%d")
    day = dt.strftime("%Y-%m-%d-%A")
    
    #FIXME: this works
    # day = docker_img_attributes["Created"].split("T")[0]
   
    repo.write(repo_name)
  
    
    tag.write(repo_version)
    image_id.write(docker_img_attributes["Id"])
    size.write(f"{int(docker_img_attributes['Size'] / (1024 ** 2))} MB")
    created.write(day)

st.divider()
st.title("Pull :blue[Docker] Images")
image_to_be_pull : str = st.text_input("Enter image: ")
if st.button("Pull"):
    image.pull_image(image_to_be_pull)

st.divider()

token = "dckr_pat_h4HHJcgk-m2J7TYyvNLPpRqed7s"
def search_action(query):
    # print("Search query: ",query)
    url = f"https://hub.docker.com/api/content/v1/products/search?q={query}&type=image"
    headers = {
        "Authorization": f"Bearer dckr_pat_h4HHJcgk-m2J7TYyvNLPpRqed7s"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    #st.write(data)
    results = data.get('summaries', [])
    
    st.subheader("Search Results:")
    for result in results[:10]:
        repository_name = result['slug']
        if st.button(repository_name):
            pull_image(repository_name)
       
def pull_image(repository: str):
    st.write(f"Image {repository} pulled sucessfully")
st.title(':orange[Docker] Im:blue[a]ge :green[Search] 🐋')
search_query = st.text_input('Enter your search query')
if st.button('Search'):
    search_action(search_query)
    
    

st.header(":blue[Docker Container]")

st.divider()

container_attributes = container_object.display_all_container()

container_id, container_image, container_status, container_created, container_names,start_container, stop_container = st.columns(7,gap="medium")

container_id.subheader("Container ID")
container_image.subheader("Image")
container_status.subheader("Status")
container_created.subheader("Created At")
container_names.subheader("Name")
start_container.subheader(":green[Launch]")
stop_container.subheader(":red[Terminate]")

#FIXME:
# use the state of the container to style it as running, stopped, or 
for container in container_attributes:
    container_attributes = container.attrs
    container_attributes["Created"] = container_attributes["Created"].split("T")[0]
    container_dt = datetime.strptime(container_attributes["Created"],"%Y-%m-%d")
    container_day = container_dt.strftime("%Y-%m-%d-%A")
    
    container_id_ = container_attributes["Id"]
    container_img = container_attributes["Image"]
    container_stats = container_attributes["State"]["Status"]

    container_name = container_attributes["Name"]
 
    
    
    container_id.write(container_id_)
    container_image.write(container_img)
    container_created.write(container_day)
    container_status.write(container_stats == "running" and ":green[Running]" or ":red[Stopped]")
    container_started = start_container.button(":green[Start]",key=(container_id_ + "j"))
    if container_started:
        container_object.start_container(container_name[1:])
        
    container_stopped = stop_container.button(":red[End]",key=(container_id_ + "k"))
    if container_stopped:
        container_object.stop_container(container_name[1:])
    with container_names:
        run_container:bool = st.button(container_name, key=container_id_)
        if run_container:
            container_object.run_container(container_name[1:])
    


