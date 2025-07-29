import json
from syntheticData import SyntheticData
from syntheticDataUsingSubstitution import SyntheticDataUsingSubstitution
from syntheticDataUsingRandomAugmentation import SyntheticDataUsingRandomAugmentation
import constants

if __name__ == '__main__':
    with open(constants.INPUT_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    data = SyntheticData.prepareData(data)

    if constants.METHOD == 1:        
        syntheticData = SyntheticDataUsingSubstitution.syntheticDataUsingSubstitution(data, constants.AUG_PPERCENTAGE, None)
    elif constants.METHOD == 2:
        syntheticData = SyntheticDataUsingSubstitution.syntheticDataUsingSubstitution(data, constants.AUG_PPERCENTAGE, None, constants.N_VARIANTS)
    else: 
        syntheticData = SyntheticDataUsingRandomAugmentation.syntheticDataUsingRandomAugmentation(data, None)
    
    print(syntheticData)
    with open(constants.OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(syntheticData, f, ensure_ascii=False, indent=2)