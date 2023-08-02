import os
import librosa
import numpy as np
import pydub
"C:\\Users\\MEIRW\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"


def extract_sample_from_track(track_path, start_time, end_time, output_path):
    # Load the input audio track using pydub
    # pydub.AudioSegment.ffmpeg = "C:\\Users\\MEIRW\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
    # check if the file exists
    if not os.path.exists(track_path):
        print("Error occurred: file doesn't exist")
        return
    track = pydub.AudioSegment.from_mp3(track_path)

    intro = track[:end_time]
    intro.export(output_path, format="mp3")
    return

    # Calculate the duration in milliseconds of the sample to extract
    duration = end_time - start_time

    # Convert to numpy array and normalize audio data
    track_array = np.array(track.get_array_of_samples())

    # Extract the sample from the track
    sample = track_array[start_time:end_time*10]

    # Save the sample to the specified path
    sample = pydub.AudioSegment(
        sample.tobytes(),
        frame_rate=track.frame_rate,
        sample_width=sample.dtype.itemsize,
        channels=1
    )
    sample.export(output_path, format="mp3")

def remove_segment_and_save(track_path, start_time, end_time, segment_path, output_path):
    # Load the input audio track and the segment to remove using pydub
    track_array = pydub.AudioSegment.from_file(track_path)
    segment = pydub.AudioSegment.from_file(segment_path)

    # Calculate the duration in milliseconds of the segment to remove
    duration = end_time - start_time

    # Ensure both audio files have the same sample rate
    if track_array.frame_rate != segment.frame_rate:
        raise ValueError("Sample rates of the input track and the segment do not match.")

    # Convert to numpy arrays and normalize audio data
    track = np.array(track_array.get_array_of_samples())
    segment = np.array(segment.get_array_of_samples())

    # Perform source separation and remove the specified segment
    output_track = []
    window_size = int(track_array.frame_rate * 10)  # 10-second window size
    step_size = int(track_array.frame_rate)  # 1-second step size

    for i in range(0, len(track) - window_size, step_size):
        window = track[i:i + window_size]

        if i >= start_time * track_array.frame_rate and i + window_size <= end_time * track_array.frame_rate:
            # The current window lies within the segment to be removed
            continue
        else:
            output_track.extend(window)

    # Convert the list back to a numpy array
    output_track = np.array(output_track)

    # Save the processed audio to a new file using pydub
    processed_audio = pydub.AudioSegment(output_track.tobytes(),
                                   frame_rate=track_array.frame_rate,
                                   sample_width=output_track.dtype.itemsize,
                                   channels=1)  # Mono audio

    processed_audio.export(output_path, format="mp3")



def remove_specific_sound(track_path, sound_path, output_path):
    # Load the input audio track and the sound to be removed using pydub
    track = pydub.AudioSegment.from_mp3(track_path)
    sound = pydub.AudioSegment.from_mp3(sound_path)

    # Ensure both audio files have the same sample rate
    frame_rate = track.frame_rate
    if track.frame_rate != sound.frame_rate:
        raise ValueError("Sample rates of the input track and the sound do not match.")

    # Convert to numpy arrays and normalize audio data
    track = np.array(track.get_array_of_samples(), dtype=np.float32)
    sound = np.array(sound.get_array_of_samples(), dtype=np.float32)

    # Compute the Short-Time Fourier Transform (STFT) of the input track and the sound
    stft_track = librosa.stft(track)
    stft_sound = librosa.stft(sound)

    # Perform source separation
    stft_result = stft_track - stft_sound

    # Inverse STFT to get the separated audio signal
    separated_track = librosa.istft(stft_result)

    # Save the separated audio to a new file using pydub
    separated_audio = pydub.AudioSegment(separated_track.tobytes(),
                                    frame_rate=frame_rate,
                                    sample_width=separated_track.dtype.itemsize,
                                    channels=1)  # Mono audio

    separated_audio.export(output_path, format="mp3")

if __name__ == "__main__":
    # Replace the following paths with your own track and segment files
    # Set the start and end time in seconds for the segment to remove
    start_time = 0*1000
    end_time = 9*1000
    # get the input track path it is in the same folder as the script and it called input.mp3
    input_track_path = os.path.dirname(os.path.realpath(__file__)) + "\\input.mp3"
    # print all the files in the current folder
    # print(os.listdir(os.path.dirname(os.path.realpath(__file__))))
    # exit()
    # concat to the input track path the name of the output track

    
    
    # extract_sample_from_track(input_track_path, start_time, end_time, "intro.mp3")
    segment_to_remove_path = "intro.mp3"
    output_track_path = "processed_track.mp3"

    # exit()

    # remove_segment_and_save(input_track_path, start_time, end_time, segment_to_remove_path, output_track_path)

    remove_specific_sound(input_track_path, segment_to_remove_path, output_track_path)
