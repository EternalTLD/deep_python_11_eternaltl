import pytest

from predict_message_mood import SomeModel, predict_message_mood


@pytest.mark.parametrize("prediction_value", [0.3, 0.5, 0.8])
def test_normal_predict_message_mood(mocker, prediction_value):
    mocker.patch(
        "predict_message_mood.SomeModel.predict", return_value=prediction_value
    )
    model = SomeModel()
    assert predict_message_mood("test", model) == "норм"


@pytest.mark.parametrize("prediction_value", [0.81, 0.9, 0.99])
def test_good_predict_message_mood(mocker, prediction_value):
    mocker.patch(
        "predict_message_mood.SomeModel.predict", return_value=prediction_value
    )
    model = SomeModel()
    assert predict_message_mood("test", model) == "отл"


@pytest.mark.parametrize("prediction_value", [0.29, 0.1, 0.01])
def test_bad_predict_message_mood(mocker, prediction_value):
    mocker.patch(
        "predict_message_mood.SomeModel.predict", return_value=prediction_value
    )
    model = SomeModel()
    assert predict_message_mood("test", model) == "неуд"


@pytest.mark.parametrize(
    "bad_thresholds, good_thresholds, prediction_value, result",
    [(0.5, 0.51, 0.505, "норм"), (0.1, 0.2, 0.05, "неуд"), (0.8, 0.9, 0.99, "отл")],
)
def test_custom_thresholds(
    mocker, bad_thresholds, good_thresholds, prediction_value, result
):
    mocker.patch(
        "predict_message_mood.SomeModel.predict", return_value=prediction_value
    )
    model = SomeModel()
    assert (
        predict_message_mood(
            "test",
            model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )
        == result
    )


@pytest.mark.parametrize("message", [1, 0.1, (1, 2, 3), [1, 2, 3], {"1": 1}])
def test_message_type(message):
    model = SomeModel()
    with pytest.raises(TypeError) as exception:
        predict_message_mood(message, model)
    assert "Message must be str" in str(exception.value)


@pytest.mark.parametrize("model", [1, 0.1, (1, 2, 3), [1, 2, 3], {"1": 1}, "test"])
def test_model_type(model):
    with pytest.raises(TypeError) as exception:
        predict_message_mood("test", model)
    assert "Model must be SomeModel" in str(exception.value)


@pytest.mark.parametrize(
    "bad_thresholds, good_thresholds",
    [
        (2, 3),
        (2, 0.5),
        (0.5, 2),
        (-1, 0.5),
        (0.5, -1),
        (-1, -2),
    ],
)
def test_thresholds_value(bad_thresholds, good_thresholds):
    model = SomeModel()
    with pytest.raises(ValueError) as exception:
        predict_message_mood(
            "test",
            model,
            bad_thresholds=bad_thresholds,
            good_thresholds=good_thresholds,
        )
    assert "Thresholds must be in (0, 1)" in str(exception.value)


def test_bad_thresholds_equal_good_thresholds():
    model = SomeModel()
    with pytest.raises(ValueError) as exception:
        predict_message_mood("test", model, bad_thresholds=0.5, good_thresholds=0.5)
    assert "Good thresholds must be greater then bad thresholds" in str(exception.value)


def test_bad_thresholds_greater_then_good_thresholds():
    model = SomeModel()
    with pytest.raises(ValueError) as exception:
        predict_message_mood("test", model, bad_thresholds=0.8, good_thresholds=0.3)
    assert "Good thresholds must be greater then bad thresholds" in str(exception.value)


@pytest.mark.parametrize("predict_input", [1, 0.1, (1, 2, 3), [1, 2, 3], {"1": 1}])
def test_some_model_predict_input(predict_input):
    model = SomeModel()
    with pytest.raises(TypeError) as exception:
        model.predict(predict_input)
    assert "Message must be str" in str(exception.value)
