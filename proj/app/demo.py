import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

application = get_wsgi_application()

from app.serializers import SnippetSerializer_ModelSerializer

serializer = SnippetSerializer_ModelSerializer()
# 序列化器具有的一个很好的特性是，您可以通过打印其表示来检查序列化器实例中的所有字段
print(repr(serializer))
