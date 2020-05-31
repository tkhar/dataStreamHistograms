# The class representing the histogram H_B

class Bucket_hist(object):
    def __init__(self, stream_length, bins):
        self.stream_length = stream_length
        self.bins = bins
        # start and end indices of each bucket
        self.start_r = []
        self.end_r = []
        # estimate value of each bucket
        self.hr = []

    def query(self, index):
        # find the bucket where the index falls in
        # poorman version
        for i in range(self.bins):
            if self.start_r[i] <= index <= self.end_r[i]:
                print("index: " + i)
                print("estimate value:" + self.hr[i])
                # return bucket index and estimate value
                return i, self.hr[i]

    # def update(self):
    # to be finished
