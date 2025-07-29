import re
import random
import nlpaug.augmenter.word as naw
import constants
import common

class SyntheticDataUsingRandomAugmentation:
    
    def __init__(self, data: None, preserveList: None):
        self.data = data
        self.preserveList = preserveList
        self.swap_aug = naw.RandomWordAug(action="swap")
        self.delete_aug = naw.RandomWordAug(action="delete")
        self.insert_aug = naw.RandomWordAug(action="insert")

    def augment_text_preserving_words(self, title):
        pattern = '(' + '|'.join(re.escape(word) for word in self.preserveList) + ')'
        parts = re.split(pattern, title)
        augmented_parts = []
        for part in parts:
            if part in self.preserveList:
                augmented_parts.append(part)
            else:
                if part.strip():
                    augmented_text = self.random_aug(part)
                    augmented_parts.append(augmented_text)
                else:
                    augmented_parts.append(part)
        return ''.join(augmented_parts)
    
    def random_aug(self, text):
        random_augmenters = [self.swap_aug, self.delete_aug, self.insert_aug]
        selected_aug = random.choice(random_augmenters)
        try:
            augmented = selected_aug.augment(text)
        except NotImplementedError:
            augmented = common.contexualAugmentation(constants.DEFAULT_AUG_PERCENTAGE).augment(text)
        return augmented[0] if isinstance(augmented, list) else augmented

    
    def randomAugmentation(self, groupTitles):   
        synthetic_data = [] 
        for app, titles in groupTitles.items():
            for title in titles:
                augmented_title = self.augment_text_preserving_words(title)
                final_text = common.replace_year_keyword(augmented_title)
                synthetic_data.append(final_text)
                # print(final_text)
                
        # print(synthetic_data)
        return synthetic_data
    

    def syntheticDataUsingRandomAugmentation(data, preserveWordsList):
        
        preserveWords = list(constants.PRESERVE_WORDS)
        if preserveWordsList:
            preserveWords.extend(preserveWordsList)
            
        mapper = SyntheticDataUsingRandomAugmentation(
            data,
            preserveWords
        )
        
        results = mapper.randomAugmentation(data)

        return results
    
