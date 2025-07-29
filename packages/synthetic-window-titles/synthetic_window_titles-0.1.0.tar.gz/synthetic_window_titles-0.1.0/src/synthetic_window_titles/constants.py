PRESERVE_WORDS = [" Google Chrome", " Microsoft Edge", " Word ", " NAME ", "YEAR", "Explorer", "Outlook", " PKF "]
START_YEAR = 1950
END_YEAR = 2025
DEFAULT_AUG_PERCENTAGE = 0.9
METHOD_TYPES = {
    1: "segmentation",
    2: "segmentationwithNvariants",
    3: "randomaugmentation",
}

#USER-INPUT
OUTPUT_FILE_PATH = r"src\data\output\syntheticDataUsingRandomAugmentation.json"
INPUT_FILE_PATH = r"src\data\input\windowTitlesTranslated.json"
AUG_PPERCENTAGE = 0.3
N_VARIANTS = 3
METHOD = 1