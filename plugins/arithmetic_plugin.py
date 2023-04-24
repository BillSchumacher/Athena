import re

from athena.plugins.plugin_base import PluginBase


class ArithmeticPlugin(PluginBase):
    def __init__(self):
        super().__init__("Arithmetic", "Performs basic arithmetic operations.")

    def can_process(self, input_text):
        return (
            re.search(r"\b(?:add|subtract|multiply|divide)\b", input_text) is not None
        )

    def process(self, input_text):
        input_text = input_text.lower()
        numbers = [int(num) for num in re.findall(r"\d+", input_text)]
        if "add" in input_text:
            result = sum(numbers)
            operation = "addition"
        elif "subtract" in input_text:
            result = numbers[0] - numbers[1]
            operation = "subtraction"
        elif "multiply" in input_text:
            result = numbers[0] * numbers[1]
            operation = "multiplication"
        elif "divide" in input_text:
            result = numbers[0] / numbers[1]
            operation = "division"
        else:
            return "I'm not sure what operation to perform."

        return f"The result of the {operation} is {result}."
