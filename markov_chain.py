import markovify


class MarkovChain:
    def __init__(self):
        self.model = None
        self.create_model()

    def create_model(self) -> None:
        with open("logs.txt", "r", encoding='utf8') as logs:
            text = logs.read()
        self.model = markovify.NewlineText(text)
        self.model = self.model.compile()

    def generate(self, start_phrase) -> str:
        generated_message = self.model.make_sentence_with_start(start_phrase, strict=False)
        return generated_message
