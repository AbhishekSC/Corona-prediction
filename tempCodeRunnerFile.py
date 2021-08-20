
# Making Functions
def data_split(data, ratio):
        np.random.seed(42)
        shuffled = np.random.permutation(len(data))
        test_set_size = int(len(data) * ratio)
        test_indices = shuffled[:test_set_size]
        train_indices = shuffled[test_set_size:]
        return data.iloc[train_indices], data.iloc[test_indices]

def Predict():
        # string= self.ageVar.get(), self.feverVar.get(), self.runnyNoseVar.get(), self.bodyPainVar.get(), self.breathinVar.get()
        # print(string)

        # Reading data
        df=pd.read_csv('cric3.csv')
        # df.head()
        # df.tail()
        # df.info()