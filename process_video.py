import os
import time
import whisper
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
from openai import OpenAI

def cut_video(input_video, start_time, end_time, output_video):
    """cortando video de acordo com o tempo de inicio e de fim para facilitar o processo"""
    video = VideoFileClip(input_video)
    video_cortado = video.subclip(start_time, end_time)
    video_cortado.write_videofile(output_video, codec="libx264")

def extract_audio_from_video(video_file, output_audio_file):
    """Extraindo audio para arquivo .wav"""
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(output_audio_file)

def transcribe_audio(audio_file):
    """Transcrevendo texto speech-to-text"""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    with open("transcription_full.txt", "w") as file:
        file.write(result['text'])
    return result['text']

def translate_text(text):
    """Traduz usando gpt 3-5"""
    client = OpenAI()
    translation = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator and your is translate portuguese video to English."},
            {"role": "user", "content": f"Translate the following text to English: {text}"},
            {"role": "user", "content": " reminder: 'rotimarte' means Hotmart"}
        ]
    )
    translated_text = translation.choices[0].message.content
    with open("translated_text_openai.txt", "w") as file:
        file.write(translated_text)
    return translated_text

def get_audio(text_segments):
    """Gerando audio a partir da tradução do trasncript """
    client = OpenAI()
    segment_files = []
    for i, segment in enumerate(text_segments):
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=segment,
        )
        segment_file = f"output_segment_{i + 1}.mp3"
        response.stream_to_file(segment_file)
        segment_files.append(segment_file)
        print(f"audio salvo como {segment_file}")
    return segment_files

def combine_audio_segments(segment_files, output_file):
    """Combina os arquivos de audio em um arquivo, processo necessário devido o tamanho modelo tts-1"""
    combined_audio = AudioSegment.from_file(segment_files[0])
    for segment_file in segment_files[1:]:
        next_segment = AudioSegment.from_file(segment_file)
        combined_audio += next_segment
    combined_audio.export(output_file, format="mp3")

def adjust_audio_speed(input_audio_file, output_audio_file, speed_factor=0.9):
    """Ajusta o tempo do audio para caber no video"""
    audio = AudioSegment.from_file(input_audio_file)
    slowed_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)
    slowed_audio.export(output_audio_file, format="mp3")

def replace_audio_in_video(video_file, audio_file, output_video_file):
    """substituindo o audio do video para o da voz feito pela IA"""
    with VideoFileClip(video_file) as video:
        with AudioFileClip(audio_file) as audio:
            final_audio = audio.subclip(0, video.duration)
            video_with_new_audio = video.set_audio(final_audio)
            video_with_new_audio.write_videofile(output_video_file, codec="libx264", audio_codec="aac")

def close_files(temp_files):
    """Caso algum arquivo ainda esteja em aberto é fechado para continuar o processo"""
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except PermissionError:
            print(f"Arquivo temporario {temp_file} ainda em uso, não foi fechado")


def main():
    # Defini tudo como mesmo diretório do codigo
    input_video = "case_ai (3).mp4"
    cut_video_file = "case_ai_5min.mp4"
    audio_file = "audio_5min.wav"
    combined_audio_file = "combined_audio_slowed.mp3"
    output_video_file = "video_with_english_audio.mp4"

    try:
        #cortando o video
        cut_video(input_video, start_time=0, end_time=300, output_video=cut_video_file)

        #Extraindo o audio do video cortado
        extract_audio_from_video(cut_video_file, audio_file)

        #transformando audio em texto
        transcribed_text = transcribe_audio(audio_file)

        #traduzindo texto do audio transcrito
        translated_text = translate_text(transcribed_text)

        #divindo o texto em segmentos menores por o modelo de transformar em texto em audio tem limite de 4096 tokens
        text_segments = list(translated_text[i:i + 4096] for i in range(0, len(translated_text), 4096))
        segment_files = get_audio(text_segments)

        #combina os audios e ajusta a velocidade
        combine_audio_segments(segment_files, combined_audio_file)
        adjust_audio_speed(combined_audio_file, combined_audio_file, speed_factor=0.9)

        #substitui o audio original do vodeo com novo traduzido
        replace_audio_in_video(cut_video_file, combined_audio_file, output_video_file)

    finally:
        # Limpar arquivos temporários
        close_files(segment_files + [combined_audio_file])

    print(f"Video final salvo como '{output_video_file}'")

if __name__ == "__main__":
    main()
