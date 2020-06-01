from setup import get_us_cases, get_china_cases

def v_opt(tokens, B):
  n = len(tokens)
  sum = [0 for _ in range(n)]
  sqsum = [0 for _ in range(n)]
  t_err = [[0 for _ in range(B)] for _ in range(n)]
  sqErr = [[0 for _ in range(n)] for _ in range(n)]

  def sq_err(s, e, sum_range, sqsum_range):
    val = (sqsum_range
            - (1 / (e - s + 1)) * (sum_range) ** 2)
    sqErr[s][e] = val
    # print(s,e,val)
    return val

  # Base cases
  sum[0] = tokens[0]
  sqsum[0] = tokens[0]*tokens[0]
  for i in range(1, n):
    sum[i] = sum[i - 1] + tokens[i]
    sqsum[i] = sqsum[i - 1] + tokens[i]**2
    # One bucket.
    t_err[i][0] = sq_err(0, i, sum[i], sqsum[i])
  
  for j in range(n):
    # t_err[j][1:] = [float('inf')] * len(t_err[j])
    for k in range(1, B):
      t_err[j][k] = float('inf')
      for i in range(j):
        t_err[j][k] = min(t_err[j][k], t_err[i][k - 1] + sq_err(i + 1, j, sum[j] - sum[i], sqsum[j] - sqsum[i]))
  

  # Recovery

  j = n - 1
  k = B - 1
  print("Min error:", t_err[j][k])
  while k > 0:
    for i in range(j):
      if t_err[j][k] == t_err[i][k - 1] + sq_err(i + 1, j, sum[j] - sum[i], sqsum[j] - sqsum[i]):
        print("Split at index: ", i)
        break
    j = i
    k = k - 1

  print(sum)
  print(sqsum)
  # for line in sqErr:
  #   print(line)
    


if __name__ == "__main__":
    #HB = hb.Bucket_hist(16, 3)
    v_opt(list(range(1, 17)) + [19], 2)
    # v_opt(get_us_cases(), 3)
    # v_opt(get_china_cases(), 3)

