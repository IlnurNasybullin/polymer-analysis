from django.db import models
from datetime import datetime


class ResultManager(models.Manager):
    def create_result(self, comment, user, im_chaar, result_net, result_ex):
        return self.create(comment=comment, 
                            data=datetime.now(), 
                            id_user=user,
                           image_characteristics=im_chaar, 
                           result_network=result_net, 
                           result_expert_system=result_ex)


class Result(models.Model):
    comment = models.TextField('Коммент')
    data = models.DateField()
    id_user = models.EmailField("Почта")
    image_characteristics = models.TextField("Характеристики изображения")
    result_network = models.TextField("Результат от нейронной сети")
    result_expert_system = models.TextField("Результат от экспертной системы")

    objects = ResultManager()

    def __str__(self):
        return self.result_expert_system
