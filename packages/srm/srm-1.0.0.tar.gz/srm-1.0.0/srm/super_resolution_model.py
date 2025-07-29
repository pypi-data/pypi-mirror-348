import os
import torch
import requests
from PIL import Image
from torchvision.transforms import ToTensor
import numpy as np


class SuperResolutionModel:
    def init(self, model_path, device=None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')

        # Если веса модели не существуют, скачать их
        if not os.path.exists(model_path):
            print(f"Model weights not found. Downloading from Google Drive...")
            self.download_model_weights(model_path)

        self.model = self._load_model(model_path)
        self.model.to(self.device)

        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True

    def download_model_weights(self, model_path):
        file_id = "1FP0aEnpULRvTpiiebVpX8uIi3H_dI6cH"  # ID файла
        url = f"https://drive.google.com/uc?export=download&id={file_id}"

        response = requests.get(url)

        if response.status_code == 200:
            with open(model_path, 'wb') as f:
                f.write(response.content)
            print(f"Model weights downloaded to {model_path}")
        else:
            print("Failed to download the model weights. Please check the link or your network.")

    def _load_model(self, model_path):
        model = torch.load(model_path, map_location=lambda storage, loc: storage, weights_only=False)
        return model


    def process_image(self, input_image_path, output_image_path):
        img = Image.open(input_image_path).convert('YCbCr')
        y, cb, cr = img.split()

        data = (ToTensor()(y)).view(1, -1, y.size[1], y.size[0])
        data = data.to(self.device)

        out = self.model(data)
        out = out.cpu()
        out_img_y = out.data[0].numpy()
        out_img_y *= 255.0
        out_img_y = out_img_y.clip(0, 255)
        out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')

        out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
        out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
        out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')

        out_img.save(output_image_path)
        print('Output image saved to', output_image_path)