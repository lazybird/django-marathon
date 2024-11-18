from marathon.mixins import SingleRunner


class SingleRunnerCommand(SingleRunner):
    """
    This is a mixin class designed to be used in Django management commands.
    It helps prevent simultaneous running of a command.
    Subclasses should implement a `run_task` method, which will contain
    the logic of the command that is to be executed.
    A `lock_name` must be defined. The `run_task` method executes only if
    there is no lock acquired for the defined `lock_name`.
    """

    def handle(self, *args, **options):
        if self.is_locked():
            self.stdout.write(f"{self.lock_name} lock prevents from running.")
            return
        # From here, the command can run since there is no lock.
        try:
            self.run_task(*args, **options)
        except Exception as e:
            self.stderr.write(f"Error: {str(e)}")
        finally:
            self.release_lock()

    def run_task(self, *args, **options):
        """
        This method will contain the logic of the command to be executed
        and should be implemented in subclasses.
        """
        raise NotImplementedError("`run_task` Must be implemented in subclasses.")
