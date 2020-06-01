import bucket_hist as bh
import matplotlib.pyplot as plt

if __name__ == "__main__":
    B = 20
    delta = 0.99
    H_us_case = bh.Bucket_hist(B)
    H_us_case.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    H_us_case.AHIST_S(delta)

    H_us_death = bh.Bucket_hist(B)
    H_us_case.read_data('stripped_data/us-cases-deaths.csv', 'deaths')
    H_us_case.AHIST_S(delta)

    #print(H_us_case.start_r)
    #print(H_us_case.end_r)
    #print(H_us_case.hr)
    #print(H_us_case.tokens)


