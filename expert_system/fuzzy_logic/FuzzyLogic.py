from enum import Enum
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

measurements = 100

class Shape:

    def __init__(self) -> None:
        self.low_bound = -1
        self.high_bound = 1

        self.low_epsilon = 0.3
        self.high_epsilon = 0.8

    class ShapeEnum(Enum):
        NO = ("no", 0)
        LESS = ("less", 1)
        SPHERIC = ("spheric", 2)

        def __init__(self, varname, index) -> None:
            super().__init__()
            self.varname = varname
            self.index = index

    def no_fuzzy_function(self, x, epsilon):
        """
        (y - y_1) / (y_2 - y_1) = (x - x_1) / (x_2 - x_1)
        """
        y = np.zeros(len(x))

        a_l = self.low_bound
        a_r = self.high_bound

        e_l = -epsilon 
        e_r = epsilon

        y_delt_l = 0 - 1
        y_delt_r = 1 - 0

        x_delt_l = e_l - a_l
        x_delt_r = a_r - e_r

        #Left side
        idx = np.nonzero(x < e_l)[0]
        if (len(idx) != 0):
            y[idx] = y_delt_l * (x[idx] - a_l) / x_delt_l + 1

        #Right side
        idx = np.nonzero(x > e_r)[0]
        if (len(idx) != 0):
            y[idx] = y_delt_r * (x[idx] - e_r) / x_delt_r

        return y

    def less_fuzzy_function(self, x, low_epsilon, high_epsilon):
        """
        Two triangles (can be intersection)
        """

        y1 = fuzz.trimf(x, [-high_epsilon, (-high_epsilon - low_epsilon) / 2, -low_epsilon])
        y2 = fuzz.trimf(x, [low_epsilon, (low_epsilon + high_epsilon) / 2, high_epsilon])
        
        for i in range(len(y2)):
            if y2[i] > y1[i]:
                y1[i] = y2[i]

        return y1

    def fuzzy_function(self, x, epsilon):
        return fuzz.trimf(x, [-epsilon, 0, epsilon])

class Smoothness:

    def __init__(self) -> None:
        self.low_bound = 0
        self.upper_bound = 1

        self.low_epsilon = 0.25
        self.high_epsilon = 0.5

    class SmoothnessEnum(Enum):
        NO = ("no", 1)
        LESS = ("less", 1)
        SMOOTH = ("smooth", 2)

        def __init__(self, varname, index) -> None:
            super().__init__()
            self.varname = varname
            self.index = index

    def no_fuzzy_function(self, x, epsilon):
        return fuzz.trapmf(x, [epsilon, (epsilon + self.upper_bound) / 1.8, self.upper_bound, self.upper_bound])

    def less_fuzzy_function(self, x, low_epsilon, high_epsilon):
        return fuzz.trapmf(x, [low_epsilon - 0.01 * low_epsilon, low_epsilon, high_epsilon, high_epsilon + 0.01 * high_epsilon])

    def fuzzy_function(self, x, epsilon):
        return fuzz.trapmf(x, [self.low_bound, self.low_bound, (epsilon + self.low_bound) / 1.8, epsilon])

class Temperature:

    def __init__(self) -> None:
        self.low_bound = 120
        self.upper_bound = 210

        self.low_epsilon = 150
        self.high_epsilon = 180

    class TemperatureEnum(Enum):

        LOW = ("low", 0)
        MEDIUM = ("medium", 1)
        HIGH = ("high", 0)

        def __init__(self, varname, index) -> None:
            super().__init__()
            self.varname = varname
            self.index = index

    def low_fuzzy_function(self, x, epsilon):
        return fuzz.trapmf(x, [self.low_bound, self.low_bound, (epsilon + self.low_bound) / 2, epsilon])

    def medium_fuzzy_function(self, x, low_epsilon, high_epsilon):
        return fuzz.trapmf(x, [low_epsilon - 0.1 * low_epsilon, low_epsilon, high_epsilon, high_epsilon + 0.1 * high_epsilon])

    def high_fuzzy_function(self, x, epsilon):
        return fuzz.trapmf(x, [epsilon, (epsilon + self.upper_bound) / 2, self.upper_bound, self.upper_bound])

class Quality:
    
    def __init__(self) -> None:
        self.low_bound = 0
        self.upper_bound = 1

    class QualityEnum(Enum):

        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

        def __init__(self, varname) -> None:
            super().__init__()
            self.varname = varname

    def low_fuzzy_function(self, x, epsilon):
        return fuzz.trapmf(x, [self.low_bound, self.low_bound, (epsilon + self.low_bound) / 2, epsilon])

    def medium_fuzzy_function(self, x, low_epsilon, high_epsilon):
        return fuzz.trapmf(x, [low_epsilon - 0.1 * low_epsilon, low_epsilon, high_epsilon, high_epsilon + 0.1 * high_epsilon])

    def high_fuzzy_function(self, x, epsilon):
        return fuzz.trapmf(x, [epsilon, (epsilon + self.upper_bound) / 2, self.upper_bound, self.upper_bound])

class Rules:

    def __init__(self) -> None:
        self.rules = self._create_rules()
        product_quality_ctrl = ctrl.ControlSystem(self.rules)
        self.product_quality = ctrl.ControlSystemSimulation(product_quality_ctrl)

    def _calculate_quality(self, shape, smoothness, temperature) -> Quality:
        sigm = 3 * shape.index + 3 * smoothness.index + temperature.index
        if sigm < 7:
            return Quality.QualityEnum.LOW
        elif sigm < 10:
            return Quality.QualityEnum.MEDIUM
        else:
            return Quality.QualityEnum.HIGH

    def _create_rules(self):
        shap = Shape()
        smth = Smoothness()
        tmp = Temperature()
        ql = Quality()

        shape = ctrl.Antecedent(np.linspace(shap.low_bound, shap.high_bound, measurements), 'shape')
        smoothness = ctrl.Antecedent(np.linspace(smth.low_bound, smth.upper_bound, measurements), 'smoothness')
        temperature = ctrl.Antecedent(np.linspace(tmp.low_bound, tmp.upper_bound, measurements), 'temperature')

        quality = ctrl.Consequent(np.linspace(ql.low_bound, ql.upper_bound, measurements), 'quality')

        shape[Shape.ShapeEnum.NO.varname] = shap.no_fuzzy_function(shape.universe, shap.high_epsilon - 0.1)
        shape[Shape.ShapeEnum.LESS.varname] = shap.less_fuzzy_function(shape.universe, shap.low_epsilon - 0.1, shap.high_epsilon + 0.1)
        shape[Shape.ShapeEnum.SPHERIC.varname] = shap.fuzzy_function(shape.universe, shap.low_epsilon + 0.1)

        smoothness[Smoothness.SmoothnessEnum.NO.varname] = smth.no_fuzzy_function(smoothness.universe, smth.high_epsilon)
        smoothness[Smoothness.SmoothnessEnum.LESS.varname] = smth.less_fuzzy_function(smoothness.universe, smth.low_epsilon, smth.high_epsilon)
        smoothness[Smoothness.SmoothnessEnum.SMOOTH.varname] = smth.fuzzy_function(smoothness.universe, smth.low_epsilon)

        temperature[Temperature.TemperatureEnum.LOW.varname] = tmp.low_fuzzy_function(temperature.universe, tmp.low_epsilon)
        temperature[Temperature.TemperatureEnum.MEDIUM.varname] = tmp.medium_fuzzy_function(temperature.universe, tmp.low_epsilon, tmp.high_epsilon)
        temperature[Temperature.TemperatureEnum.HIGH.varname] = tmp.high_fuzzy_function(temperature.universe, tmp.high_epsilon)

        quality[Quality.QualityEnum.LOW.varname] = ql.low_fuzzy_function(quality.universe, 0.35)
        quality[Quality.QualityEnum.MEDIUM.varname] = ql.medium_fuzzy_function(quality.universe, 0.30, 0.70)
        quality[Quality.QualityEnum.HIGH.varname] = ql.high_fuzzy_function(quality.universe, 0.65)

        rules = []
        for sh in Shape.ShapeEnum:
            for sm in Smoothness.SmoothnessEnum:
                for temp in Temperature.TemperatureEnum:
                    qual = self._calculate_quality(sh, sm, temp)
                    rules.append(ctrl.Rule(shape[sh.varname] & smoothness[sm.varname] & temperature[temp.varname], quality[qual.varname]))

        return rules;

    def predict(self, shape: float, smoothness: float, temperature: float) -> float:
        self.product_quality.inputs({
            'shape': shape,
            'smoothness': smoothness,
            'temperature': temperature
        })

        self.product_quality.compute()
        return self.product_quality.output['quality']