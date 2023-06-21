import os
import wave
import json
import vosk
from pydub import AudioSegment
from tkinter import Tk, filedialog, Button

def main():

    # Open a file dialog box to select the input audio file
    root = Tk()
    root.withdraw()
    file_path_rec = filedialog.askopenfilename(
        filetypes=[('Video Files', '*.mp4'), ('MP3 Files', '*.mp3'), ('OGG Files', '*.ogg'), ('WAV Files', '*.wav'), ('All Files', '*.*')]
    )

    # Convert non-WAV files to WAV with a sample rate of 8000
    audio_format_rec = os.path.splitext(file_path_rec)[1]
    if audio_format_rec != ".wav":
        sound_rec = AudioSegment.from_file(file_path_rec, format=audio_format_rec[1:])
        sound_rec = sound_rec.set_frame_rate(8000).set_channels(1)
        file_path_rec = os.path.splitext(file_path_rec)[0] + ".wav"

        sound_rec.export(file_path_rec, format="wav")
    elif file_path_rec.endswith(".mp4"):
        # Convert MP4 file to WAV with a sample rate of 8000
        sound_rec = AudioSegment.from_file(file_path_rec, format="mp4")
        sound_rec = sound_rec.set_frame_rate(8000).set_channels(1)
        wav_path_rec = os.path.splitext(file_path_rec)[0] + ".wav"
        sound_rec.export(wav_path_rec, format="wav")

    else:
        # Change the sample rate of the WAV file to 8000
        sound_rec = AudioSegment.from_file(file_path_rec, format="wav")
        sound_rec = sound_rec.set_frame_rate(8000).set_channels(1)
        file_path_rec = os.path.splitext(file_path_rec)[0] + "_8000.wav"
        sound_rec.export(file_path_rec, format="wav")

    # Open the WAV file
    wav_file_rec = wave.open(file_path_rec, 'rb')

    # Create a Vosk model and speech recognizer instance
    model_path_rec = 'vosk-model-ru-0.42'
    model_rec = vosk.Model(model_path_rec)
    recogn = vosk.KaldiRecognizer(model_rec, wav_file_rec.getframerate())

    # Create a TXT file with the same name as the input audio file
    txt_file_rec = open(os.path.splitext(file_path_rec)[0] + ".txt", "w", encoding="utf-8")

    # Read and recognize the audio file
    while True:
        data_rec = wav_file_rec.readframes(80000)
        if len(data_rec) == 0:
            break
        if recogn.AcceptWaveform(data_rec):
            rec_result = json.loads(recogn.Result())
            rec_time = wav_file_rec.tell() / wav_file_rec.getframerate()  # Calculate time in seconds
            txt_file_rec.write(f"{rec_time:.2f} s: {rec_result['text']}\n")
            print(f"{rec_time:.2f} s: {rec_result['text']}\n")

    # Get the final recognition result
    rec_result = json.loads(recogn.FinalResult())
    rec_time = wav_file_rec.getnframes() / wav_file_rec.getframerate()  # Calculate time in seconds
    txt_file_rec.write(f"{rec_time:.2f} s: {rec_result['text']}\n")

    # Close the files
    wav_file_rec.close()
    txt_file_rec.close()
    root = Tk()
    finish_button = Button(root, text="Завершить", command=root.destroy)
    finish_button.pack()

    # Запуск главного цикла отображения окна
    root.mainloop()
    
if __name__ == "__main__":
    main()
