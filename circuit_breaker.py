import time


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold=3,
        recovery_timeout=10
    ):

        self.failure_threshold = (
            failure_threshold
        )

        self.recovery_timeout = (
            recovery_timeout
        )

        self.failure_count = 0

        self.last_failure_time = None

        self.state = "CLOSED"


    # -----------------------------------
    # CHECK IF REQUEST ALLOWED
    # -----------------------------------

    def allow_request(self):

        if self.state == "OPEN":

            elapsed = (
                time.time() -
                self.last_failure_time
            )

            if elapsed > self.recovery_timeout:

                self.state = "HALF_OPEN"

                return True

            return False

        return True


    # -----------------------------------
    # RECORD SUCCESS
    # -----------------------------------

    def record_success(self):

        self.failure_count = 0

        self.state = "CLOSED"


    # -----------------------------------
    # RECORD FAILURE
    # -----------------------------------

    def record_failure(self):

        self.failure_count += 1

        self.last_failure_time = time.time()

        if (
            self.failure_count >=
            self.failure_threshold
        ):

            self.state = "OPEN"


    # -----------------------------------
    # EXECUTE PROTECTED CALL
    # -----------------------------------

    def call(
        self,
        func,
        *args,
        **kwargs
    ):

        if not self.allow_request():

            return {
                "error":
                "Circuit breaker OPEN."
            }

        try:

            result = func(
                *args,
                **kwargs
            )

            self.record_success()

            return result

        except Exception as e:

            self.record_failure()

            return {
                "error": str(e)
            }