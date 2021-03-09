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
        self.data_one = []
        self.data_two = []

    def read_data_one(self, data_one):
        """Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
            data (csv): name of a file to read from

        Returns:
            None

        """
        data_one = pd.read_csv(data_one)
        self.data_one = data_one


    def read_data_two(self, data_two):
        """Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
            data (csv): name of a file to read from

        Returns:
            None

        """

        data_two = pd.read_csv(data_two)
        self.data_two = data_two