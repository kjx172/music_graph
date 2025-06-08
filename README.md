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
- Select yes, and select which playlist you'd like to extract
- If ran previously extracted tracks are cached and can be used for following steps

#### 2. Youtube download
- Using the previously extracted (or cached) spotify track names, artists, and albums the program will search youtube using ytdlp and download an mp3 of the first result
- Its important to note that some download errors might occur as the first result might not always be the correct song
- Make sure to configure a cookies.txt with your cookies from youtube to avoid hitting the rate limit
- If ran previously downloaded tracks are cached and can be used for following steps

#### 3. Clip Division
- The Essentia Model requires that songs are divided into 30s clips
- If ran previously downloaded tracks are cached and can be used for following steps

#### 4. Running the model
- You will need to switch to your WSL system where Essentia, the Essentia Models, and your 2nd RunAudioModels.py is stored. Running the models may take a significant amount of time depending on the size of playlists
- If ran previously before the song embeddings are cached and can be used for following steps

#### 5. Visualizing the graph
- Switching back to the windows environment after the model has been fully run, selecting yes to visualize will generate a graphml and a csv file for your songs

#### 6. Reclustering
- This is optional, if you extract the modularity from your graphml file and copy paste it as a column into your csv file you can then select the reclustering option which will create a new graph ml based on each songs external cluster similarity rather than internal cluster similarity.