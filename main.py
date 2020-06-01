import bucket_hist as bh
import pandas as pd
import matplotlib.pyplot as plt

def show_plot(HB, title, xlabel, ylabel):
    # reference: https://realpython.com/python-histograms/
    #           https://github.com/carsonfarmer/streamhist
    #           https://matplotlib.org/tutorials/introductory/pyplot.html
    # size, scale = self.tokens, self.bins
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis='y')
    plt.bar(HB.start_r, HB.hr)
    plt.show()

if __name__ == "__main__":
    B = 2
    delta = 0.99
    #H_us_case = bh.Bucket_hist(B)
    #H_us_case.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    #H_us_case.AHIST_S(delta)

    #H_us_death = bh.Bucket_hist(B)
    #H_us_death.read_data('stripped_data/us-cases-deaths.csv', 'deaths')
    #H_us_death.AHIST_S(delta)

    df = pd.read_csv('stripped_data/china-cases-deaths.csv')
    china_date = list(df['date'])

    H_china_case = bh.Bucket_hist(B)
    H_china_case.read_data('stripped_data/china-cases-deaths.csv', 'cases')
    #H_china_case.AHIST_S(delta)

    H_china_death = bh.Bucket_hist(B)
    H_china_death.read_data('stripped_data/china-cases-deaths.csv', 'deaths')
    H_china_death.AHIST_S(delta)
    #H_china_death.show_plot('China Death', 'Date Index', 'Deaths')
    #print(H_us_case.start_r)
    #print(H_us_case.end_r)
    #print(H_us_case.hr)
    #print(H_us_case.tokens)
    print(H_china_death.start_r)
    print(H_china_death.end_r)
    print(H_china_death.hr)
    #show_plot(H_china_death, 'China Death', 'Date Index', 'Deaths')


