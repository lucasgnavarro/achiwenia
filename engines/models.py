from django.db import models


class DatabaseServer(models.Model):
    DATABASE_ENGINES = (
        ('django.db.backends.postgresql', 'Postgresql'),
    )
    DATABASE_PORTS = (5432,)

    engine = models.CharField(max_length=50, blank=None, choices=DATABASE_ENGINES, default='Postgresql')
    host = models.CharField(max_length=60, default='127.0.0.1')
    port = models.IntegerField(default=5432)

    def __str__(self):
        return '{engine}@{host}:{port}'.format(
            engine=dict(self.DATABASE_ENGINES).get(str(self.engine)),
            host=self.host,
            port=self.port
        )

    class Meta:
        app_label = 'tenants'