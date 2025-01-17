# The class representing the histogram H_B
import pandas as pd

class Bucket_hist:
    def __init__(self, bins):
        self.stream_length = 0
        self.bins = bins
        # start and end indices of each bucket
        self.start_r = []
        self.end_r = []
        self.hr = []
        for i in range(bins):
            self.start_r.append(0)
            self.end_r.append(0)
            self.hr.append(0)
        # estimate value of each bucket

        self.tokens = []
        # self.read_data()

    # answer query
    def query(self, index):
        # find the bucket where the index falls in
        # poorman version
        for i in range(self.bins):
            if index <= self.end_r[i]:
                print("index: " + i)
                print("estimate value:" + self.hr[i])
                # return bucket index and estimate value
                return i, self.hr[i]

    # read data from csv file
    def read_data(self, csv_file, title):
        # temporarily generate an array
        # n = 21
        # for i in range(n):
        #     self.tokens.append(i)
        # self.stream_length = n
        # self.tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19]
        # self.stream_length = 17
        df = pd.read_csv(csv_file)
        self.tokens = list(df[title])
        self.stream_length = len(self.tokens)

    # run AHIST_S with parameter delta
    def AHIST_S(self, delta):
        ## Initialize:
        # Q[k] represents intervals for k buckets
        # where the numbers in the same interval
        # are within (1 + delta) approx of each other
        B = self.bins
        Q = [[] for i in range(B + 1)]  # Start indexing at 1
        my_sum = 0
        sqsum = 0
        apx_err = float('inf')

        max_index = len(self.tokens) - 1
        optimal_sub = 0.0

        # Based on the simplificatin of squared error
        # in paper. Representative of interval is h,
        # as shown in paper. Guha et. al 2006
        def sq_err(s, e, s_sum, e_sum, s_sqsum, e_sqsum):
            return ((e_sqsum - s_sqsum)
                    - (1.0 / (e - s + 1.0)) * (e_sum - s_sum) ** 2)

        # too bruteforce, need to be optimized
        def sq_err_interval(s, e):
            i_sum = 0
            i_sqsum = 0
            for i in range(s, e + 1):
                i_sum += self.tokens[i]
                i_sqsum += self.tokens[i] * self.tokens[i]
            return (i_sqsum - (1.0 / (e - s + 1.0)) * i_sum * i_sum)

        def process(j):
            nonlocal my_sum, sqsum, apx_err
            # for constructing the histogram
            nonlocal max_index, optimal_sub
            # Maintain running sum and running square sum for
            # sqerror calculations.
            my_sum += self.tokens[j]
            sqsum += self.tokens[j] * self.tokens[j]

            # Fill up error approximation matrix minimize
            # apx error.
            for k in range(1, B + 1):  # change the range of k here to match the notation in the paper
                apx_err = float('inf')
                optimal_err = apx_err
                optimal_sub = apx_err
                if k > 1:
                    for (ai, bi, apx_err_sub, sub_sum, sub_sqsum, start_err) in Q[k - 1]:

                        if bi < j:
                            tmp_sq_err = sq_err(bi + 1, j, sub_sum, my_sum, sub_sqsum, sqsum)
                            tmp_apx_err = apx_err_sub + tmp_sq_err
                            apx_err = min(apx_err, tmp_apx_err)

                        # prepare to construct histogram buckets
                        if k == B and j == len(self.tokens) - 1:
                            if optimal_err > apx_err:
                                optimal_err = apx_err
                                optimal_sub = apx_err_sub
                                max_index = bi + 1
                else:
                    # Base case. When k = 2, subproblem of k - 1 = 1 bucket
                    # Approximation error is just sqsum to j.
                    apx_err = sq_err(0, j, 0, my_sum, 0, sqsum)

                # Either expand range of last interval or insert as new interval
                # in Q[k].
                if len(Q[k]) == 0:
                    # 6th element is to record the approx. error of the start index of the interval
                    # used when deciding whether to add a new interval
                    # Q[k].append([j, j, apx_err, my_sum, sqsum, apx_err, start_err])
                    Q[k].append([j, j, 0.0, my_sum, sqsum, 0.0])
                # Insert as new interval.
                elif k <= B - 1 and apx_err > (1.0 + delta) * Q[k][-1][5]:  # apx_err_sub
                    if apx_err != float('inf'):
                        Q[k].append([j, j, apx_err, my_sum, sqsum, apx_err])
                # Expand current last interval
                else:
                    Q[k][-1][1] = j
                    Q[k][-1][2] = apx_err
                    Q[k][-1][3] = my_sum
                    Q[k][-1][4] = sqsum
                    if apx_err == float('inf'):
                        Q[k][-1][5] = apx_err

        def construct_buckets(max_index, opt_err_sub):
            self.start_r[B - 1] = max_index
            self.end_r[B - 1] = len(self.tokens) - 1
            self.end_r[B - 2] = max_index - 1
            b_idx = B - 2
            epsilon = 0.5
            # calculate start indices for each bucket
            # reversely find every index bound that optimizes the square error

            # there's an exact same approx error for bucket_{B-2}
            # without calculating the sq_err
            # if b_idx == 0:
            #     self.start_r[b_idx] = 0
            # elif b_idx > 0:
            #     for (ai, bi, apx_err_sub, sub_sum, sub_sqsum, start_err) in Q[b_idx + 1]:
            #         if  -epsilon < apx_err_sub - opt_err_sub < epsilon:
            #             self.start_r[b_idx] = bi
            #             self.end_r[b_idx - 1] = bi - 1
            #             break
            #     b_idx = b_idx - 1


            while b_idx > 0:
                self.end_r[b_idx] = max(self.start_r[b_idx + 1] - 1, 0)
                previous_sub_err = opt_err_sub
                previous_bi = 0
                for (ai, bi, apx_err_sub, sub_sum, sub_sqsum, start_err) in Q[b_idx + 1]:
                    #if bi < self.end_r[b_idx]:
                    if apx_err_sub <= opt_err_sub:
                        if bi == self.end_r[b_idx]:
                            tmp_err = apx_err_sub
                        else:
                            approx_sq_err = sq_err_interval(bi, self.end_r[b_idx])
                            tmp_err = apx_err_sub + approx_sq_err
                            sub_err = tmp_err - opt_err_sub
                            # when previous err sub is positive, and current one is negative,
                            # the division index lies between
                        if sub_err <= 0.0:
                            self.start_r[b_idx] = bi
                            opt_err_sub = apx_err_sub
                            break
                        previous_bi = bi
                        previous_sub_err = sub_err
                        #assign it to last bi if sub_err always > 0
                        self.start_r[b_idx] = bi
                b_idx = b_idx - 1

            self.end_r[b_idx] = max(self.start_r[b_idx + 1] - 1, 0)
            # calculate h_r(mean of values of x_i in bucket r)

        # for i in range(B):
        # print("bucket " + str(i) + ": " + str(self.start_r[i]) + " - " + str(self.end_r[i]))

        def calculate_bucket_means():
            for b in range(B):
                tmp_sum = 0
                for j in range(self.start_r[b], self.end_r[b] + 1):
                    tmp_sum += self.tokens[j]
                    self.hr[b] = tmp_sum / (self.end_r[b] - self.start_r[b] + 1)
                # print(self.hr[b])

        for j in range(len(self.tokens)):
            process(j)
        construct_buckets(max_index, optimal_sub)
        calculate_bucket_means()
        #for q in Q:
           #print(q)

    # run v-optimal (dynamic programming) without approximation
    def HIST_DP(self):
        B = self.bins
        n = len(self.tokens)
        sum = [0 for _ in range(n)]
        sqsum = [0 for _ in range(n)]
        t_err = [[0 for _ in range(B)] for _ in range(n)]

        def sq_err(s, e, sum_range, sqsum_range):
            val = (sqsum_range
                   - (1 / (e - s + 1)) * (sum_range) ** 2)
            return val

        # Base cases
        sum[0] = self.tokens[0]
        sqsum[0] = self.tokens[0] * self.tokens[0]
        for i in range(1, n):
            sum[i] = sum[i - 1] + self.tokens[i]
            sqsum[i] = sqsum[i - 1] + self.tokens[i] ** 2
            # One bucket.
            t_err[i][0] = sq_err(0, i, sum[i], sqsum[i])

        for j in range(n):
            # t_err[j][1:] = [float('inf')] * len(t_err[j])
            for k in range(1, B):
                t_err[j][k] = float('inf')
                for i in range(j):
                    t_err[j][k] = min(t_err[j][k],
                                      t_err[i][k - 1] + sq_err(i + 1, j, sum[j] - sum[i], sqsum[j] - sqsum[i]))

        # Recovery

        j = n - 1
        k = B - 1
        self.end_r[k] = n-1
        #print("Min error:", t_err[j][k])
        while k > 0:
            for i in range(j):
                if t_err[j][k] == t_err[i][k - 1] + sq_err(i + 1, j, sum[j] - sum[i], sqsum[j] - sqsum[i]):
                    #print("Split at index: ", i)
                    self.start_r[k] = i
                    self.end_r[k-1] = i-1
                    break
            j = i
            k = k - 1

        #def calculate_bucket_means():
        #calculate means of each bucket
        for b in range(B):
            tmp_sum = 0
            for j in range(self.start_r[b], self.end_r[b] + 1):
                tmp_sum += self.tokens[j]
                self.hr[b] = tmp_sum / (self.end_r[b] - self.start_r[b] + 1)
    # def show_plot(self, title, xlabel, ylabel):
    #     # reference: https://realpython.com/python-histograms/
    #     #           https://github.com/carsonfarmer/streamhist
    #     #           https://matplotlib.org/tutorials/introductory/pyplot.html
    #     #size, scale = self.tokens, self.bins
    #     plt.title(title)
    #     plt.xlabel(xlabel)
    #     plt.ylabel(ylabel)
    #     plt.grid(axis='y')
    #     plt.bar(self.start_r, self.hr)
    #     plt.show()
    # calculate new cases

    def calculate_increment(self):
        new_tokens = []
        new_tokens.append(self.tokens[0])
        for i in range(1, self.stream_length):
            new_tokens.append(self.tokens[i] - self.tokens[i-1])
        self.tokens = new_tokens