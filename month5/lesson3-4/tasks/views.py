from rest_framework.views import APIView  # Базовый класс для создания ручных API-представлений
from rest_framework.response import Response  # Класс для отправки JSON-ответов
from rest_framework import status  # Набор стандартных HTTP-статусов (например, 201, 400)
from .serializer import TaskSerializer  # Импорт сериализатора для перевода модели в JSON и обратно
from .models import Task  # Импорт модели Task
from rest_framework import generics, mixins  # Импорт готовых блоков для CRUD

class TaskView(APIView):  # Создание обычного класса-представления API вручную
    def get(self, request, *args, **kwargs):  # Обработка GET-запроса (получение всех задач)
        tasks = Task.objects.all()  # Достать из базы данных абсолютно все задачи
        serializer = TaskSerializer(tasks, many=True)  # Превратить список задач в формат JSON (many=True — если объектов много)
        return Response(serializer.data)  # Вернуть сериализованные данные клиенту

    def post(self, request):  # Обработка POST-запроса (создание новой задачи)
        serializer = TaskSerializer(data=request.data)  # Передать входящие данные в сериализатор
        if serializer.is_valid():  # Проверка: прошли ли данные валидацию по правилам сериализатора?
            serializer.save()  # Если всё ок — сохранить новую задачу в базу данных
            return Response({
                "message": "Задача успешна создана",
            }, status=status.HTTP_201_CREATED)  # Отправить ответ об успехе со статусом 201 (Created)
        
        return Response({
            "message": "Ошибка валидации данных",
        }, status=status.HTTP_400_BAD_REQUEST)  # Отправить ошибку со статусом 400 (Bad Request), если данные неверные

class TaskListView(  # Класс для работы со списком задач и их создания
    mixins.ListModelMixin,  # Миксин, который умеет отдавать список элементов
    mixins.CreateModelMixin,  # Миксин, который умеет создавать элемент
    generics.GenericAPIView):  # generic-класс, связывающий миксины

    queryset = Task.objects.all()  # Базовый набор всех задач для выборки
    serializer_class = TaskSerializer  # Указываем сериализатор, который будет использоваться

    def get_queryset(self):  # Переопределение метода для получения задач с возможностью фильтрации
        queryset = Task.objects.all()  # Берем все задачи
        q = self.request.query_params.get('q')  # Ищем параметр 'q' в строке запроса (параметры фильтрации)
        if q:  # Если пользователь передал текст для поиска
            queryset = queryset.filter(name__icontains=q)  # Фильтруем задачи по имени (без учета регистра)
        return queryset  # Возвращаем итоговый набор задач

    def get(self, request, *args, **kwargs):  # Обработка GET-запроса для списка
        return self.list(request, *args, **kwargs)  # Вызов встроенного метода миксина для показа списка

    def post(self, request, *args, **kwargs):  # Обработка POST-запроса для создания
        return self.create(request, *args, **kwargs)  # Вызов встроенного метода миксина для создания

class TaskDetailView(  # Класс для работы с одной конкретной задачей по её ID
    mixins.RetrieveModelMixin,  # Миксин для просмотра одной записи
    mixins.UpdateModelMixin,  # Миксин для полного обновления записи (PUT)
    mixins.DestroyModelMixin,  # Миксин для удаления записи (DELETE)
    generics.GenericAPIView):  # Базовый generic-класс

    queryset = Task.objects.all()  # Набор всех задач, среди которых будет искаться нужная по ID
    serializer_class = TaskSerializer  # Указываем используемый сериализатор

    def get(self, request, *args, **kwargs):  # Обработка GET-запроса для одной задачи
        return self.retrieve(request, *args, **kwargs)  # Вызов миксина для получения конкретной задачи

    def put(self, request, *args, **kwargs):  # Обработка PUT-запроса (полное обновление задачи)
        return self.update(request, *args, **kwargs)  # Вызов миксина для полного обновления

    def patch(self, request, *args, **kwargs):  # Обработка PATCH-запроса (частичное обновление задачи)
        return self.partial_update(request, *args, **kwargs)  # Вызов миксина для частичного обновления

    def delete(self, request, *args, **kwargs):  # Обработка DELETE-запроса (удаление задачи)
        return self.destroy(request, *args, **kwargs)  # Вызов миксина для удаления записи из базы
