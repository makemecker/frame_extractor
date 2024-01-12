import cv2
from tqdm import tqdm
import os
import argparse
import shutil


def check_image_path(path: str):
    """ Валидация указанного пути к папке с изображениями"""

    if not isinstance(path, str):
        print("Ошибка: Путь к изображениям (image_path) должен быть указан в виде строки.")
        return False
    if not os.path.exists(path):
        print("Ошибка: Указанного пути к изображениям не существует.")
        return False
    if not os.listdir(path):
        print(
            "Предупреждение: Папка с изображениями (image_path) пуста. Рекомендуется добавить изображения перед "
            "запуском функции.")
        return False
    return True


def frame_extractor(video_dir: str) -> bool:
    if not check_image_path(video_dir):
        return False

    output_path = "Frames"
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    frames_per_second = 1

    for video in tqdm(os.listdir(video_dir)):
        video_path = os.path.join(video_dir, video)
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_interval = fps // frames_per_second
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_number % frame_interval == 0:
                frames.append(frame)

        cap.release()
        for i, frame in enumerate(frames):
            frame_path = os.path.join(output_path, f"{os.path.splitext(os.path.basename(video_path))[0]}_frame_{i}.jpg")
            print(cv2.imwrite(frame_path, frame))

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FrameExtractor is a tool designed to split videos into frames..")
    parser.add_argument("--video_dir", required=True, help="Path to the folder containing videos.")
    args = parser.parse_args()
    video_dir_arg = args.video_dir

    if frame_extractor(video_dir=video_dir_arg):
        print("Frames from the video have been saved to a folder 'Frames'.")
