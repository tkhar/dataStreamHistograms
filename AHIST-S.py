# Implementation of AHIST-S
import bucket_hist as hb

def AHIST_S(tokens, B, delta):
    ## Initialize:
    # Q[k] represents intervals for k buckets
    # where the numbers in the same interval
    # are within (1 + delta) approx of each other
    Q = [[] for i in range(B + 1)]  # Start indexing at 1
    my_sum = 0
    sqsum = 0
    apx_err = float('inf')

    max_index = len(tokens) - 1
    optimal_sub = 0.0
    tmp_sum = 0
    tmp_sqsum = 0


    # Based on the simplificatin of squared error
    # in paper. Representative of interval is h,
    # as shown in paper. Guha et. al 2006
    def sq_err(s, e, s_sum, e_sum, s_sqsum, e_sqsum):
        return ((e_sqsum - s_sqsum)
                - (1.0 / (e - s + 1.0)) * (e_sum - s_sum) ** 2)

    def process(j):
        nonlocal my_sum, sqsum, apx_err
        # for constructing the histogram
        nonlocal max_index, optimal_sub, tmp_sum, tmp_sqsum
        # Maintain running sum and running square sum for
        # sqerror calculations.
        previous_sum = my_sum
        previous_sqsum = sqsum
        my_sum += tokens[j]
        sqsum += tokens[j] * tokens[j]


        # debug
        # print("j = " + str(j))
        # Fill up error approximation matrix minimize
        # apx error.
        for k in range(1, B + 1): #change the range of k here to match the notation in the paper
            apx_err = float('inf')
            optimal_err = apx_err
            optimal_sub = apx_err

            if k > 1:
                for (ai, bi, apx_err_sub, sub_sum, sub_sqsum, start_err) in Q[k - 1]:
                    # debug
                    #print("ai, bi, apx_err_sub, sub_sum, sub_sqsum: " + str(ai) + "," + str(bi) + ","
                          # + str(apx_err_sub) + "," + str(sub_sum) + "," + str(sub_sqsum))

                    if bi <= j:
                        tmp_sq_err = sq_err(bi, j, sub_sum, my_sum, sub_sqsum, sqsum)
                        tmp_apx_err = apx_err_sub + tmp_sq_err
                        # print("tmp_sq_err: " + str(tmp_sq_err))
                        # print("tmp_apx_err:" + str(tmp_apx_err))
                        apx_err = min(apx_err, tmp_apx_err)

                    # constructing histogram buckets
                    if k == B and j == len(tokens) - 1:
                        if optimal_err > apx_err:
                            optimal_err = apx_err
                            optimal_sub = apx_err_sub
                            max_index = bi + 1
                            tmp_sum = sub_sum
                            tmp_sqsum = sub_sqsum
                            #HB.start_r[B-1] = index
                        #print("index: " + str(index))



                    # apx_err_cand = apx_err_sub + sq_err(bi, j, sub_sum, my_sum, sub_sqsum, sqsum)
                #   if apx_err_cand < apx_err:
                #     min_index = bi
                #     apx_err = apx_err_cand
                # if k == B and j == len(tokens) - 1:
                #   print(min_index)

            else:
                # Base case. When k = 2, subproblem of k - 1 = 1 bucket
                # Approximation error is just sqsum to j.
                apx_err = sq_err(0, j, 0, my_sum, 0, sqsum)

            # debug
            #print("apx_err:" + str(apx_err))

            # Either expand range of last interval or insert as new interval
            # in Q[k].
            if len(Q[k]) == 0:
                # 6th element is to record the approx. error of the start index of the interval
                # used when deciding whether to add a new interval
                Q[k].append([j, j, apx_err, previous_sum, previous_sqsum, apx_err])
                # debug
                #print("Q[" + str(k) + "] add: " +str(j) + "," + str(j) + ","
                #          + str(apx_err) + "," + str(my_sum) + "," + str(sqsum))

            # Insert as new interval.
            elif k <= B - 1  and apx_err > (1.0 + delta) * Q[k][-1][5]:  # apx_err_sub
                Q[k].append([j, j, apx_err, previous_sum, previous_sqsum, apx_err])
                #print("Q[" + str(k) + "] add: " + str(j) + "," + str(j) + ","
                 #     + str(apx_err) + "," + str(my_sum) + "," + str(sqsum))
            # Expand current last interval
            else:
                Q[k][-1][1] = j
                Q[k][-1][2] = apx_err
                Q[k][-1][3] = previous_sum
                Q[k][-1][4] = previous_sqsum
                if apx_err == float('inf'):
                    Q[k][-1][5] = apx_err
                #print("Q[" + str(k) +"] expanded to " + str(j))
            # debug
            # if k == 1:
                #print("APR[" + str(j) +"," + str(k) + "] = " + str(apx_err))

    def construct_buckets(max_index, opt_err_sub, tmp_sum, tmp_sqsum):
        start_r = []
        end_r = []
        for i in range(B):
            start_r.append(0)
            end_r.append(0)

        start_r[B-1] = max_index
        end_r[B-1] = len(tokens)-1
        b_idx = B-2

        # calculate start indices for each bucket
        # reversely find every index bound that optimizes the square error
        previous_ai = 0
        previous_bi = 0
        previous_apx_err = 0.0
        while b_idx >= 1:
            end_r[b_idx] = max(start_r[b_idx + 1] - 1, 0)
            for (ai, bi, apx_err_sub, sub_sum, sub_sqsum, start_err) in Q[b_idx+1]:

                if apx_err_sub >= opt_err_sub and previous_bi <= start_r[b_idx+1]:
                    start_r[b_idx] = previous_bi
                    opt_err_sub = previous_apx_err
                    #opt_err_sub = opt_err_sub - sq_err(bi, end_r[b_idx], sub_sum, tmp_sum, sub_sqsum, tmp_sqsum)
                    #tmp_sum = sub_sum
                    #tmp_sqsum = sub_sqsum
                    break

                previous_ai = ai
                previous_bi = bi
                previous_apx_err = apx_err_sub
            b_idx = b_idx - 1

        end_r[b_idx] = max(start_r[b_idx + 1] - 1, 0)
        # calculate h_r(mean of values of x_i in bucket r)
        for i in range(B):
            print("bucket " + str(i) + ": " + str(start_r[i]) + " - " + str(end_r[i]))


    def output():
        return apx_err

    for j in range(len(tokens)):
        process(j)
    construct_buckets(max_index, optimal_sub, tmp_sum, tmp_sqsum)

    print(output())
    for q in Q:
        print(q)


if __name__ == "__main__":
    #HB = hb.Bucket_hist(16, 3)
    AHIST_S(list(range(1, 100)), 8, 0.99)