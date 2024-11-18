Django Marathon
===============

::

    +---------------------------+
    |                           |
    |                           |
    |             \O            | Django Marathon helps manage single runner tasks
    |             /\            | that need to avoid concurrency issues.
    |          __/\ `           | It provide a lock in database to ensure that tasks
    |          `    \,          | are executed without overlapping.
    |                           |
    |                           | 
    |                           | 
    +---------------------------+

Features
--------

- Ensures single execution of tasks to avoid concurrency.
- Easy integration with Django management commands.

How Django Marathon Works
-------------------------

Under the hood, Django Marathon uses a simple locking mechanism to prevent concurrent
execution of tasks.

1. **Lock Model**: Single runner tasks will create a lock in the database,
using the `Lock` model. A lock has unique name representing the tasks.
It also has a timestamp indicating when the lock was created.
Each task that needs to avoid concurrency will first have to check the lock
table before running.

2. **SingleRunnerCommand**: This is a helper class that is designed to be used in
Django management commands.

3. **Lock Acquisition and Release**: When a command using `SingleRunnerCommand` is executed,
it first checks if a lock with the specified name exists. If it does, the command does not run.
If no lock exists, the command proceeds, and a lock is created.
Once the command completes, the lock is released, allowing future executions.


Requirements
------------

- Python 3.6+
- Django 3.1+

Installation
------------

You can install Django Marathon via pip:

::

    pip install django-marathon


Add `marathon` to your Django project's `INSTALLED_APPS`:

::

    INSTALLED_APPS = [
        ...
        'marathon',
    ]


Usage With Django Management Commands
-------------------------------------

Define a tasks that should be run without concurrency.


`SingleRunnerCommand` is a base command class provided by Django Marathon to
ensure that a management command does not run concurrently.

::

    from marathon.commands import SingleRunnerCommand
    from django.core.management.base import BaseCommand

    class Command(SingleRunnerCommand, BaseCommand):
        help = 'Your command description here'

        def handle(self, *args, **options):
            self.stdout.write('Starting task...')
            # Your task logic here
            self.stdout.write('Task completed.')


Using the Locking Mechanism Outside Management Commands
-------------------------------------------------------

Django Marathon's locking mechanism can also be utilized outside of management commands.


Here's a general approach:

- Check if the lock exists
- Create a new lock if not
- Implement you task logic
- Release the lock

In practice, we would typically do the first 2 steps together.

Example Implementation:

::

    from marathon.models import Lock

    def my_task():
        lock_name = "my-unique-task-lock"
        # Get the existing lock or create a new one
        lock, created = Lock.objects.get_or_create(name=lock_name)
        if not created:
            print("Task is already running, please try again later.")
            return
        try:
            # Your task logic here
            print("Task is running...")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            # Release the lock
            lock.delete()
        print("Task completed successfully.")
