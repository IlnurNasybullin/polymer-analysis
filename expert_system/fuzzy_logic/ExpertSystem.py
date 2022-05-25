import base64
from pandas import DataFrame
from . import FuzzyLogic as fz
import seaborn as sns
import io
from matplotlib.pylab import plt

class ExpertSystem:
    def __init__(self, df_polymers: DataFrame, temperature: float) -> None:
        self.df_polymers = df_polymers
        self.temperature = temperature

    def to_result(self) -> dict:
        mean = 0.0
        count = 0
        means = []

        for _, rows in self.df_polymers.iterrows():
            val = self._to_result(rows['roundness'] - 1, rows['roughness'], self.temperature)
            mean += val
            means.append(val)
            count += 1

        if (count != 0):
            mean /= count

        fig = plt.figure("")
        ax = sns.displot(means, color="0.25", bins=10)
        ax.set(xlabel='quality')

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        val = img_buf.getvalue()
        img_buf.close()

        return {"meanValue": mean, "displotImage": base64.b64encode(val).decode("utf-8")}

    def _to_result(self, roundness: float, roughness: float, temperature: float) -> float:
        return fz.Rules().predict(roundness, roughness, temperature)