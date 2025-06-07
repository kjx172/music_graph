# Music Graph Visualizer

This tool exports your spotify playlist and creates a network graph of your musics similarity. This can be used to detect clusters of similar songs within your playlist, these songs will usually share an artist, genre, or time period. By reclustering the graph based on similarity to songs outside of the self contained cluster then you can make inferences about songs that are similar without them sharing an immediatly obvious connection.

## Features

## Setup
#### 1. **Clone the repository:**
- git clone https://github.com/kjx172/music_graph.git
- cd music_graph

#### 2. **Install dependencies:**
- Ensure you have Python and pip installed. Then run:
   ```sh
   pip install -r requirements.txt

#### 3. **Install essentia:**
- Follow the instructions at https://github.com/MTG/essentia to download the essentia *note needs to be run in a linux environment, i used WSL*
- Ensure essentia is installed with tensorflow support
- Clone the essentia models repo as well to get access to effnetdiscoogs https://github.com/MTG/essentia-models

#### 3. **Set up environment variables:**
Create a .env file in the root directory and add your Spotify API credentials:

client_id=your_openai_api_key
client_secret=your_openai_api_secret

I also placed my FFMPEG path here since i had seperate python versions and was running into errors with my code being unable to find it

## Usage
#### 1. Spotify Collection
- When you run the code you'll be prompted as to whether you want to gather playlist information from spotify
- Select yes, and select which playlist you'd like to ext