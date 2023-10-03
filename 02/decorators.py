import time


def last_callbacks_avg_time(last_callbacks_number):
    def inner(func):
        callbacks_time = []
        callbacks_count = 0

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            nonlocal callbacks_time
            nonlocal callbacks_count
            callbacks_time.append(end_time - start_time)
            callbacks_count += 1
            if len(callbacks_time) > last_callbacks_number:
                callbacks_time.pop(0)
                callbacks_count = last_callbacks_number
            avg_time = sum(callbacks_time) / len(callbacks_time)
            print(
                f"Average execution time of {callbacks_count} last callbacks: {avg_time}"
            )
            return result

        return wrapper

    return inner
