from copy import copy
from typing import List, Optional, Sequence

import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageFilter


class ParticleNet:
    _size: int = 64
    _model: torch.nn.Module
    _um_per_pixel: float

    def __init__(
        self, model_path: str, um_per_pixel: float, conf_threshold: float = 0.6
    ) -> None:
        assert 0.0 <= conf_threshold <= 1

        self._model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path)
        self._model.conf = conf_threshold
        self._um_per_pixel = um_per_pixel

    def predict(
        self, images: Sequence[str], um_per_pixel: Optional[float] = None
    ):
        um_per_pixel = self._um_per_pixel if um_per_pixel is None else um_per_pixel
        results = self._forward(images)

        # TODO: without save is not work (image with boxes), but it's real save in some directory
        results.render()

        results_list = results.tolist()

        df_list: List[pd.DataFrame] = []
        for result, image in zip(results_list, images):
            df = self._get_dataframe(result)

            df["roundness"] = self._get_roundness(result)
            df["roughness"] = self._get_roughness(result, image)
            df["particle_size"] = self._get_particle_size(result, um_per_pixel)

            df_list.append(df)

        return df_list, results.ims[0]

    @torch.inference_mode()
    def _forward(self, images):
        return self._model(images)

    @staticmethod
    def _get_dataframe(result) -> pd.DataFrame:
        df = result.pandas().xyxy[0]
        df = df.drop(["class", "name"], axis=1)
        return df

    @staticmethod
    def _get_roundness(result):
        wh = result.xywh[0][:, 2:4]
        roundness = 4 * wh.prod(dim=1) / wh.sum(dim=1).pow(2)
        return roundness

    def _get_roughness(self, result, image: np.ndarray) -> np.ndarray:
        mean = []
        for i in range(result.xyxy[0].shape[0]):
            target = (
                image.resize(
                    (self._size, self._size), Image.LANCZOS, box=result.xyxy[0][i, :4].numpy()
                )
                .convert("L")
                .filter(ImageFilter.MedianFilter(3))
                .filter(ImageFilter.FIND_EDGES)
            )
            target = np.asarray(target) / 255.0
            mean.append(target.mean())

        return np.asarray(mean)

    @staticmethod
    def _get_particle_size(result, um_per_pixel: float) -> np.ndarray:
        wh = result.xywh[0][:, 2:4].numpy()
        max_lenght = wh.max(axis=1)
        return max_lenght * um_per_pixel


if __name__ == "__main__":
    from pathlib import Path

    model_path = Path("weights/particles-yolov5l-best.pt")
    images = [path for path in Path("images").iterdir() if path.suffix in {".png"}]

    net = ParticleNet(
        model_path=model_path,
        um_per_pixel=20 / 100,
        conf_threshold=0.8,
    )

    df_list = net.predict(copy(images))

    for df, image_path in zip(df_list, images):
        df.to_csv(image_path.stem + ".csv", index=False)
