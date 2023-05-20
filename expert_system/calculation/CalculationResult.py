from PIL import Image
import io
from io import BytesIO
from expert_system.fuzzy_logic.ExpertSystem import ExpertSystem

from expert_system.particle_model.particlenet.particle_net import ParticleNet
import base64

model_path='expert_system/particle_model/weights/particles-yolov5l-best.pt'

class Calculation:
    def __init__(self, image_bytes: bytearray, um_per_pixel: float, temperature: float, min_disp: float, max_disp: float) -> None:
        self.image = Image.open(io.BytesIO(image_bytes))
        self.um_per_pixel = um_per_pixel
        self.temperature = temperature
        self.min_disp = min_disp
        self.max_disp = max_disp

    def to_result(self) -> dict:
        pn = ParticleNet(model_path=model_path, um_per_pixel=self.um_per_pixel)
        dfl, img = pn.predict([self.image], self.um_per_pixel)

        pil_img = Image.fromarray(img)
        buff = BytesIO()
        pil_img.save(buff, format="PNG")
        str_image = base64.b64encode(buff.getvalue()).decode("utf-8")

        df = dfl[0]

        all_polymers_count = len(df)

        disps = df["particle_size"] / self.um_per_pixel
        print(df)
        disp_polymers = df[(disps >= self.min_disp) & (disps <= self.max_disp)][["roundness", "roughness"]]

        disp_polymers_count = len(disp_polymers)
        dict_res = ExpertSystem(disp_polymers, self.temperature).to_result()

        res = {
            "allPolymersCount": all_polymers_count,
            "dispPolymersCount": disp_polymers_count,
            "prImage": str_image
        }

        res.update(dict_res)

        return res

class CalculationAdapter:
    def to_calculation(args: dict) -> Calculation:
         image_bytes = args["image_bytes"]
         um_per_pixel = float(args["um_per_pixel"])
         temperature = float(args["temperature"])
         min_disp = float(args["min_disp"])
         max_disp = float(args["max_disp"])

         return Calculation(image_bytes, um_per_pixel, temperature, min_disp, max_disp)
        

