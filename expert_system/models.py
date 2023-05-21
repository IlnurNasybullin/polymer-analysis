from django.db import models
from datetime import datetime


class ResultManager(models.Manager):
    def create_result(self, comment, created_dt, user, im_chars, result_net, result_ex, uri):
        return self.create(comment=comment, 
                            created=created_dt, 
                            id_user=user,
                           image_characteristics=im_chars, 
                           result_network=result_net, 
                           result_expert_system=result_ex,
                           img_uri=uri)


class Result(models.Model):
    comment = models.TextField('Коммент')
    created = models.DateTimeField('Сохранён')
    id_user = models.EmailField("Почта")
    image_characteristics = models.TextField("Характеристики изображения")
    result_network = models.TextField("Результат от нейронной сети")
    result_expert_system = models.TextField("Результат от экспертной системы")
    img_uri = models.TextField('Ссылка на изображение')

    objects = ResultManager()

    def __str__(self):
        return self.result_expert_system
