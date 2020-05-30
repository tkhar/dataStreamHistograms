# Implementation of AHIST-S


def AHIST_S(tokens, B, delta):

  ## Initialize: 
  # Q[k] represents intervals for k buckets
  # where the numbers in the same interval
  # are within (1 + delta) approx of each other
  Q = [[] for i in range(B + 1)]  # Start indexing at 1
  my_sum = 0
  sqsum = 0
  apx_err = float('inf')

  # Based on the simplificatin of squared error
  # in paper. Representative of interval is h, 
  # as shown in paper. Guha et. al 2006
  def sq_err(s, e, s_sum, e_sum, s_sqsum, e_sqsum):
    return ((e_sqsum - s_sqsum) 
      - (1/(e - s + 1))*(e_sum - s_sum)**2)

  def process(j):
    nonlocal my_sum, sqsum, apx_err
    # Maintain running sum and running square sum for 
    # sqerror calculations.
    my_sum += tokens[j]
    sqsum += tokens[j] * tokens[j]

    # Fill up error approximation matrix minimize 
    # apx error. 
    for k in range(2, B + 1):
      apx_err = float('inf')
      
      if k > 2:
        for (ai, bi, apx_err_sub, sub_sum, sub_sqsum) in Q[k - 1]:
          apx_err = min(apx_err, apx_err_sub + sq_err(bi, j, sub_sum, my_sum, sub_sqsum, sqsum))
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
      # Either expand range of last interval or insert as new interval 
      # in Q[k]. 
      if len(Q[k]) == 0:
        Q[k].append([j, j, apx_err, my_sum, sqsum])
      # Insert as new interval. 
      elif k <= B - 1 and apx_err > (1 + delta)*Q[k][-1][2]:  # apx_err_sub
          Q[k].append([j, j, apx_err, my_sum, sqsum])
      # Expand current last interval
      else:
          Q[k][-1][1] = j
        
  def output():
    return apx_err

  for j in range(len(tokens)):
    process(j)
  
  print(output())
  for q in Q:
    print(q)



if __name__ == "__main__":
  AHIST_S(list(range(1, 17)), 3, 0.99)