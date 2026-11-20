def add_numbers(payload: dict):

    num1 = payload["num1"]
    num2 = payload["num2"]

    result = num1 + num2

    return {
        "num1": num1,
        "num2": num2,
        "result": result
    }