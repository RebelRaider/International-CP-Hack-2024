import torch
import gc
import os
import torchaudio
from torchvision import transforms
from moviepy.editor import VideoFileClip
from imagebind.models.imagebind_model import ModalityType
from imagebind import data
from loguru import logger
from summarizer import summarize_description


def load_and_transform_video_data(video_path, device, chunk_size=32):
    video_transform = transforms.Compose(
        [
            transforms.Grayscale(num_output_channels=1),
            transforms.Lambda(lambda img: img.repeat(3, 1, 1)),
            transforms.Resize((224, 224)),
            transforms.Normalize(
                mean=(0.48145466, 0.4578275, 0.40821073),
                std=(0.26862954, 0.26130258, 0.27577711),
            ),
        ]
    )
    all_video = []
    with VideoFileClip(video_path) as video:
        for frame in video.iter_frames():
            frame_tensor = torch.tensor(frame).float().permute(2, 0, 1) / 255.0
            transformed_frame = video_transform(frame_tensor).unsqueeze(0)
            all_video.append(transformed_frame)

            if len(all_video) == chunk_size:
                yield torch.cat(all_video, dim=0).to(device)
                all_video = []
                torch.cuda.empty_cache()
                gc.collect()

        if all_video:
            yield torch.cat(all_video, dim=0).to(device)
            torch.cuda.empty_cache()
            gc.collect()


def get_text_embedding(text, imagebind_model, device):
    if not text.strip():
        logger.debug("Empty text input. Returning zero vector.")
        return torch.zeros(1024, device=device)
    inputs = {ModalityType.TEXT: data.load_and_transform_text([text], device)}
    with torch.no_grad():
        embeddings = imagebind_model(inputs)
    text_embedding = embeddings[ModalityType.TEXT][0]
    logger.debug("Computed text embedding.")
    return text_embedding


def get_audio_embedding(video_path, imagebind_model, device, cache_dir="cache/"):
    try:
        waveform, sr = torchaudio.load(video_path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            waveform = resampler(waveform)

        audio_path = f"{cache_dir}/temp_audio.wav"
        torchaudio.save(audio_path, waveform, 16000)

        inputs = {ModalityType.AUDIO: data.load_and_transform_audio_data([audio_path], device)}
        with torch.no_grad():
            embeddings = imagebind_model(inputs)
        audio_embedding = embeddings[ModalityType.AUDIO].mean(dim=0)

        os.remove(audio_path)
        logger.debug("Computed audio embedding.")
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        audio_embedding = torch.zeros(1024, device=device)
    return audio_embedding


def get_video_embedding(video_path, imagebind_model, device):
    embeddings_list = []
    try:
        with torch.no_grad():
            for video_chunk in load_and_transform_video_data(video_path, device):
                chunk_embeddings = imagebind_model({ModalityType.VISION: video_chunk})
                embeddings_list.append(chunk_embeddings[ModalityType.VISION].mean(dim=0))
                torch.cuda.empty_cache()
                gc.collect()

            video_embedding = torch.stack(embeddings_list).mean(dim=0)
            logger.debug(f"Computed video embedding for video at {video_path}.")
            torch.cuda.empty_cache()
            gc.collect()

    except Exception as e:
        logger.error(f"Error processing video at {video_path}: {e}")
        video_embedding = torch.zeros(1024, device=device)

    return video_embedding


def extract_embeddings(video_path, title, description, imagebind_model, summary_tokenizer, summary_model, device):
    title_embedding = get_text_embedding(title, imagebind_model, device)
    summarized_description = summarize_description(summary_tokenizer, summary_model, description, device)
    description_embedding = get_text_embedding(summarized_description, imagebind_model, device)
    audio_embedding = get_audio_embedding(video_path, imagebind_model, device)
    video_embedding = get_video_embedding(video_path, imagebind_model, device)

    embeddings = torch.cat([title_embedding, description_embedding, audio_embedding, video_embedding], dim=-1)
    logger.debug("Combined embeddings for video, audio, and text.")
    return embeddings


