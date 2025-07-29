import json
import re
import random
from collections import defaultdict
import nlpaug.augmenter.word as naw
import constants
import common

class SyntheticDataUsingSubstitution:
    
    def __init__(self, data: None, augPercentage: float, preserveList: None, nVariants: int):
        self.data = data
        self.augPercentage = augPercentage
        self.preserveList = preserveList
        self.nVariants = nVariants
    
    def augment_text_preserving_words(self, title):
        pattern = '(' + '|'.join(re.escape(word) for word in self.preserveList) + ')'
        parts = re.split(pattern, title)
        aug = common.contexualAugmentation(self.augPercentage)
        augmented_parts = []
        for part in parts:
            if part in self.preserveList:
                augmented_parts.append(part)
            else:
                if part.strip():
                    augmented = aug.augment(part)
                    augmented_text = augmented[0] if isinstance(augmented, list) else augmented
                    augmented_parts.append(augmented_text)
                else:
                    augmented_parts.append(part)
        return ''.join(augmented_parts)
    
    def substituteWords(self, groupedTitles):
        synthetic_data = []
        for app, titles in groupedTitles.items():
            for title in titles:
                augmented_title = self.augment_text_preserving_words(title)
                # print("Title: ", title)
                final_text = common.replace_year_keyword(augmented_title)
                # print(final_text)
                synthetic_data.append(final_text)
                
        # print(synthetic_data)
        return synthetic_data

    def substituteWordsNVariants(self, groupedTitles, nVariants):    
        syntheticData = []    
        for app, titles in groupedTitles.items():
            for title in titles:
                for _ in range(nVariants):
                    augmented_title = self.augment_text_preserving_words(title)
                    final_text = common.replace_year_keyword(augmented_title)
                    print(final_text)
                    # variant_list.append(final_text)
                syntheticData.append(final_text)
                
        return syntheticData

    def syntheticDataUsingSubstitution(data, augPercentage, preserveWordsList, nVariants):
        
        preserveWords = list(constants.PRESERVE_WORDS)
        if preserveWordsList:
            preserveWords.extend(preserveWordsList)
            
        mapper = SyntheticDataUsingSubstitution(
            data,
            augPercentage,
            preserveWords,
            nVariants
        )
        
        if nVariants > 1:
            results = mapper.substituteWordsNVariants(data, nVariants)
        else:
            results = mapper.substituteWords(data)
        # print("results: ", results)
        return results