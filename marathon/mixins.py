from marathon.models import Lock


class SingleRunner:
    """
    Mixin class that helps prevent simultaneous running of tasks.
    It provides a way to check if a task already running or not.
    It writes a lock in the database and gives a way to it releases
    the lock by deleting the lock database entry.
    A lock consists of lock name, which could be shared by multiple
    tasks.
    """

    lock_name = None

    def is_locked(self):
        """
        Creates lock if it does not exist and returns True.
        If lock already exists, it returns False.
        """
        if not self.lock_name:
            raise NotImplementedError("lock_name must be set")
        _, created = Lock.objects.get_or_create(name=self.lock_name)
        is_locked = not created  # is created <=> is not locked
        return is_locked

    def release_lock(self):
        """
        Deletes the existing lock.
        """
        Lock.objects.filter(name=self.lock_name).delete()
