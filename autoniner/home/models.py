from django.db import models

TASK_CHOICES = (
    ('DOOR', 'DOOR'),
    ('SCANNER', 'SCANNER'),
)

# Create your models here.
class Task(models.Model):
    title = models.CharField('Task Name',max_length=50)
    description = models.CharField('Task Description',max_length=50, blank=True)
    task_type = models.CharField(max_length=10, choices=TASK_CHOICES, default='door count')

    # Administrative log information
    task_id = models.AutoField(primary_key=True) # This autoincrements, so we can guarentee uniqueness on this field.
    date_created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """ This is strictly optional, this just makes our lives easier when working with the ORM for this model. """
        ordering = ['date_created']
        verbose_name_plural = 'tasks'
        get_latest_by = ['date_created']
    
    def __str__(self):
        return '{}'.format(self.title)
    
class DoorCountInstance(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tid')
    id = models.IntegerField(primary_key=True)
    sensor_id = models.CharField(max_length=100)
    start_time = models.DecimalField(max_digits=100, decimal_places=20)
    end_time = models.DecimalField(max_digits=100,decimal_places=20)
    in_count = models.IntegerField()
    out_count = models.IntegerField()
    sensor_type = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=255)
    sensor_group = models.CharField(max_length=255)
    tmestamp = models.DecimalField(max_digits=100,decimal_places=20)