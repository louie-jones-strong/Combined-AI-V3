

class PredictorBase:
    def __init__(self, dataSetManager, loadData):
        self.DataSetManager = dataSetManager

        if loadData:
            self.DataSetManager.LoadTableInfo()
        return
    