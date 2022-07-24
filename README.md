# Advanced Django Tutorial
- T-01 : project init
- T-02 : custom management command to create_data
- T-03 : api views, pagination, queryset optimization
- T-04 : unit tests
- T-05 : elastic search implementation



### Initial Commands
```
python manage.py makemigrations
python manage.py migrate
python manage.py create_data
```
### Elastic Search Command
```bash
python manage.py search_index --rebuild
```
### Celery Commands
```bash
# start the worker
celery -A src worker -l INFO
# start django celery beat
celery -A src beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# run celery flower
 celery -A src flower --port=5556
```
#### Creating a periodic task
```bash
In [1]: from django_celery_beat.models import PeriodicTask, IntervalSchedule
In [2]: schedule, created = IntervalSchedule.objects.get_or_create(
   ...: every=10,
   ...: period=IntervalSchedule.SECONDS
   ...: )

In [3]: created
Out[3]: True

In [4]: PeriodicTask.objects.create(
   ...: interval=schedule,
   ...: name="my counting author task :D",
   ...: task="app.tasks.count_authors",
   ...: )
Out[4]: <PeriodicTask: my counting author task :D: every 10 seconds>

In [5]: sc2, created2 = IntervalSchedule.objects.get_or_create(
   ...: every=5,
   ...: period=IntervalSchedule.SECONDS
   ...: )

In [6]: created2
Out[6]: True

In [7]: PeriodicTask.objects.create(
   ...: interval=sc2,
   ...: name="Book ratings getter task",
   ...: task="app.tasks.get_book_ratings",
   ...: )
Out[7]: <PeriodicTask: Book ratings getter task: every 5 seconds>

```