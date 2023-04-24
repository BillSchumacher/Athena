class PluginBase:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def can_process(self, input_text):
        raise NotImplementedError(
            "The 'can_process' method must be implemented in derived classes."
        )

    def process(self, input_text):
        raise NotImplementedError(
            "The 'process' method must be implemented in derived classes."
        )
