from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import warnings

warnings.filterwarnings('ignore')
print("Loading NLU model...")
training_data = load_data("nlu_data.md")
trainer = Trainer(config.load("nlu_config.yml"))
interpreter = trainer.train(training_data)

# Save the trained model for future use
model_directory = trainer.persist("./models/nlu", fixed_model_name="current")
