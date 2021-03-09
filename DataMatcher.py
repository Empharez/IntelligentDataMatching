import pandas as pd
class DataMatcher:
    """
        Data matcher class class for matching records.

    		Attributes:
    			mean (float) representing the mean value of the distribution
    			stdev (float) representing the standard deviation of the distribution
    			data_list (list of data per row) a list of floats extracted from the data file
    """

    def __int__(self):
        self.data = []

    def read_data_file(self, data):
        """Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
            data (csv): name of a file to read from

        Returns:
            None

        """
        pd.read_csv(data)
        data_list = []
        self.data = data_list
