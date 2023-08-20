import openai
import speech_recognition as sr

openai.api_key = "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"

def audiov():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)

    # Guardar el audio en un archivo temporal (opcional)
    audio_file = "audio_temp.wav"
    with open(audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    # Leer el archivo de audio para la transcripción con SpeechRecognition
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        transcripcion = r.recognize_google(audio_data, language='es-MX')  # O ajusta el idioma que desees

    print(transcripcion)
    return transcripcion

    # Eliminar el archivo temporal (opcional)
    import os
    os.remove(audio_file)