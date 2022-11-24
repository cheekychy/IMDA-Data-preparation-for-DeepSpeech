from pydub import AudioSegment
from pathlib import Path
import pandas as pd
import textgrid
import os
import soundfile as sf
import natsort
import random

"""
Data preparation script to format data as per DeepSpeech requirements
"""

pd.options.mode.chained_assignment = None

def split(files):
    
    os.chdir("/home/tzeminhhhh/delete") # Change to your own directory where audio files are stored

    split_1 = int(0.5*len(files))
    split_2 = int(0.7*len(files))
    train_data = files[:split_1]
    dev_data = files[split_1:split_2]
    test_data = files[split_2:]

    # print(f"No. of training examples: {len(train_data)}")
    # print(f"No. of dev examples: {len(dev_data)}")
    # print(f"No. of testing examples: {len(test_data)}")

    return train_data, dev_data, test_data

def create_csv_for_split(train_data, dev_data, test_data, final_df, path): # /home/tzeminhhhh/ds_dataset
    df = pd.DataFrame()
    
    train = final_df.loc[final_df['wav_filename'].isin(train_data)]
    dev = final_df.loc[final_df['wav_filename'].isin(dev_data)]
    test = final_df.loc[final_df['wav_filename'].isin(test_data)]

    csvlist = ["train", "dev", "test"]
    i = 0
    for df in [train, dev, test]: 
        df.name = csvlist[i]
        output_path = "{}/{}/{}.csv".format(path, "wav_files", df.name)   
      
        df.loc[:, 'wav_filename'] = "/DeepSpeech/delete/wav_files/" + df['wav_filename'].astype(str)
        df.reset_index(drop = True, inplace = True)
        df.to_csv(output_path)
        print("CSV file saved to ", output_path)
        i += 1


def split_audio_on_silence(audio_path, df_transcript, textgrid_filename):

    item = ""
    length = len(df_transcript)

    chunk_path = os.path.join(os.path.dirname(audio_path), "wav_files")
  
    for filename in os.listdir(audio_path):
        name = os.path.splitext(filename)[0]

      
        textgrid_filename = os.path.splitext(textgrid_filename)[0]
        if ((filename.endswith('.wav')) and (name == textgrid_filename)): 
            f = os.path.join(audio_path, filename) 
            item = AudioSegment.from_wav(f)
            print("Splitting audio of filename {}...".format(filename))
         
            for i in range(length):
                name = os.path.splitext(filename)[0]
                output_chunk = "{}/{}_chunk{}.wav".format(chunk_path, name, i+1) # name of output wav file
                audio_chunk = item[(df_transcript.loc[i,'start'])*1000:(df_transcript.loc[i,'stop'])*1000]  
                # chunk_name = "{}_chunk{}.wav".format(name, i)
                # print("Exporting chunk: ", chunk_name)
                audio_chunk.export(output_chunk, format="wav")
              

   
    files = [f for f in os.listdir(chunk_path) if f.endswith(".wav")]
    files = natsort.natsorted(files)
    random.seed(230)
    random.shuffle(files)
    train_data, dev_data, test_data = split(files) 
                   
    print("Splitting done")
    return train_data, dev_data, test_data


        
def convert_textgrid_to_csv(root_path, audio_path):
    final_df = pd.DataFrame()
    textgrid_path = os.path.join(root_path, "textgrid_files") # replace with the name of your textgrid folder
    
    textgrid_files = natsort.natsorted(os.listdir(textgrid_path))
    for j, filename in enumerate(textgrid_files):
        if filename.endswith('.TextGrid'):
           tgrid = textgrid.read_textgrid("{}/{}".format(textgrid_path, filename))
           name = os.path.splitext(filename)[0]
           df = pd.DataFrame(tgrid)

           df.insert(loc=0, column="wav_filename", value="")
           df.insert(loc=1, column="wav_filesize", value="")
           df["duration"] = df['stop'] - df['start']
           df.rename(columns={'name':'transcript'}, inplace=True)

           output_file = "{}/transcript.csv".format(textgrid_path) # per transcript file
           train_data, dev_data, test_data = split_audio_on_silence(audio_path,df,name)
    
           final_df = pd.concat([final_df, df])

    final_df = final_df.reset_index(drop=True)
    print("Removing silent transcript...")
  
    chunk_path = os.path.join(root_path, "wav_files")
    os.chdir(chunk_path)
   
    chunklist = natsort.natsorted(os.listdir(chunk_path))
   
    for i, chunk in enumerate(chunklist): # chunk = wav filename 
        filesize = Path(chunk).stat().st_size
        final_df.loc[i,'wav_filename'] = chunk
        final_df.loc[i,'wav_filesize'] = filesize


    final_df = final_df.drop(['start','stop','tier','duration'], axis=1)
    unwanted = ["<Z>", "<S>"]
    final_df = final_df[~final_df['transcript'].str.contains('|'.join(unwanted))]
    final_df['transcript'] = final_df['transcript'].str.replace(r"[^a-zA-Z\s]+", "",regex=True).str.lower()
    final_df = final_df.loc[(final_df['transcript'].astype(bool)) & (final_df['transcript'].str.len() >= 50)]  
    final_df['transcript'] = final_df['transcript'].str.replace('\t', ' ')
    
    final_df.reset_index(drop = True, inplace = True)
    final_df.to_csv(output_file)
    print("CSV file saved to ", output_file)

    create_csv_for_split(train_data, dev_data, test_data, final_df, root_path)
    print("Data cleaning done!")
    
   

    

def main():
    convert_textgrid_to_csv("/home/tzeminhhhh/delete", "/home/tzeminhhhh/delete/clips") # Change path to your own directory

if __name__ == "__main__":
    main()

