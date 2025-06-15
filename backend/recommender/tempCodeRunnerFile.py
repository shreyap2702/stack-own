import spacy
from train import converted_data
from spacy.training import Example
import random

nlp=spacy.load("en_core_web_sm")

textcat=nlp.create_pipe( "textcat_multilabel" )
nlp.add_pipe(textcat, last=True)
nlp.pipe_names

textcat.add_label("dashboard")
textcat.add_label("realtime_system")
textcat.add_label("web_app")
textcat.add_label("ecommerce")
textcat.add_label("ml_task")
textcat.add_label("portfolio")
textcat.add_label("mobile_app")

examples = []
for text, annotations in converted_data:
    doc = nlp.make_doc(text)
    example =  Example.from_dict(doc, annotations)
    examples.append(example)

nlp.begin_training()
for iteration in range(20):
    random.shuffle(examples)
    losses = {}
    nlp.update(examples, losses=losses)
    print(f"Iteration {iteration}, Losses: {losses}")

nlp.to_disk("./model_output")



    
