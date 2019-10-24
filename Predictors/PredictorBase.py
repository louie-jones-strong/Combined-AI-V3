from Shared import OutputFormating as Format

class PredictorBase:

    NumPredictions = 0

    def __init__(self, dataSetManager, loadData):
        self.DataSetManager = dataSetManager

        if loadData:
            self.DataSetManager.LoadTableInfo()
        return

    def PredictorInfoOutput(self):
        info = ""
        info += "Number of predictions: "+Format.SplitNumber(self.NumPredictions)

        return info
    
