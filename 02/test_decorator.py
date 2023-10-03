import time

from decorators import last_callbacks_avg_time


def test_decorator_log_message(capsys):
    last_callbacks_number = 5

    @last_callbacks_avg_time(last_callbacks_number)
    def test_callback():
        return "Test callback"

    for callback_count in range(1, 11):
        test_callback()
        captured = capsys.readouterr()
        callback_count = min(callback_count, last_callbacks_number)
        assert (
            f"Average execution time of {callback_count} last callbacks:"
            in captured.out
        )


def test_decorator_output_time(capsys):
    last_callbacks_number = 5

    @last_callbacks_avg_time(last_callbacks_number)
    def test_callback():
        time.sleep(0.1)
        return "Test callback"

    for _ in range(3):
        test_callback()
        captured = capsys.readouterr()
        colon_pos = captured.out.find(":")
        output_time = float(captured.out[colon_pos+1:])
        assert 0.09 <= output_time <= 0.11
