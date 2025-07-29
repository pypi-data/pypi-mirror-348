import random
import nlpaug.augmenter.word as naw
import constants

@staticmethod
def contexualAugmentation(augP):
    aug = naw.ContextualWordEmbsAug(model_path='bert-base-cased', action="substitute",aug_p=augP)
    return aug

@staticmethod
def replace_year_keyword(text):
    if "YEAR" in text:
        start_year = random.randint(constants.START_YEAR, constants.END_YEAR)
        duration = random.randint(5, 20)
        end_year = start_year + duration
        year_range = f"{start_year}-{end_year}"
        text = text.replace("YEAR", year_range)
    return text