from collections import defaultdict

class SyntheticData:
    
    def __init__(self, data: any, methodType: str, nVariants: int, augPercentage: float):
        self.data = data
        self.methodType = methodType
        self.nVariants = nVariants
        self.augPercentage = augPercentage

    #group window titles by the "applicationname" field        
    @staticmethod
    def prepareData(data):
        grouped_titles = defaultdict(list)
        for entry in data:
            app = entry.get("applicationname", "Unknown")
            title = entry.get("windowtitle", "").strip()
            if title:
                grouped_titles[app].append(title)
                
        return grouped_titles
    
