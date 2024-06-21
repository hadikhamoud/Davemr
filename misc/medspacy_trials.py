import spacy; import medspacy
# # Option 1: Load default
# #import context from medspacy
# #nlp = spacy.load("en_core_web_sm")
# #nlp.add_pipe("context")
# # Option 2: Load custom
# nlp = medspacy.load(enable=["context"])
# # Option 3: Load custom with custom config
# #nlp = medspacy.load(enable=["context"], config={"context": {"max_length": 100}})
# # Option 4: Load custom with custom config


# nlp = medspacy.load()

# #call the ConTexT object on a medspacy doc
# context = medspacy.Context()
# doc = nlp("The patient has a history of hypertension and diabetes. She is currently taking lisinopril and metformin.")
# context(doc)


#example use case for medspacy ConText

#load medspacy
import spacy; import medspacy
from medspacy.visualization import visualize_dep
nlp = medspacy.load(enable=["context"])
#call the ConTexT object on a medspacy doc
context = medspacy.context.ConText(nlp)
doc = nlp("The patient has a history of hypertension and diabetes. She is currently taking lisinopril and metformin.")

#visualize the ConText output
visualize_dep(doc)

