import random


class SomeModel:
    def predict(self, message: str) -> float:
        if not isinstance(message, str):
            raise TypeError("Message must be str")
        prediction = random.uniform(0, 1)
        return prediction


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if not isinstance(message, str):
        raise TypeError("Message must be str")
    if not isinstance(model, SomeModel):
        raise TypeError("Model must be SomeModel")
    if not 0 < bad_thresholds < 1 or not 0 < good_thresholds < 1:
        raise ValueError("Thresholds must be in (0, 1)")
    if good_thresholds <= bad_thresholds:
        raise ValueError("Good thresholds must be greater then bad thresholds")

    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"
    return "норм"
