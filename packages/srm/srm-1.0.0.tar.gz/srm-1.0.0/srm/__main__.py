import argparse
import os
from srm.super_resolution_model import SuperResolutionModel

def parse_args():
    parser = argparse.ArgumentParser(description="Обработка изображений с суперразрешением.")
    parser.add_argument('image_files', nargs='+', help='Пути к изображениям для обработки')
    parser.add_argument('--model_path', required=True, help='Путь к весам модели')
    parser.add_argument('--output_dir', required=True, help='Папка для сохранения результатов')
    return parser.parse_args()

def main():
    args = parse_args()

    print(f"Файлы для обработки: {args.image_files}")
    print(f"Путь к модели: {args.model_path}")
    print(f"Папка для результата: {args.output_dir}")

    # Инициализация модели
    sr_model = SuperResolutionModel()
    sr_model.init(args.model_path)

    # Создаем папку для результатов, если её нет
    os.makedirs(args.output_dir, exist_ok=True)

    # Обработка каждого файла
    for img_path in args.image_files:
        output_path = os.path.join(args.output_dir, f"sr_{os.path.basename(img_path)}")
        sr_model.process_image(img_path, output_path)
        print(f"Обработано и сохранено: {output_path}")

    print("Обработка завершена.")

if __name__ == "__main__":
    main()