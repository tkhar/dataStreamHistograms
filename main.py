import bucket_hist as bh
import pandas as pd
import matplotlib.pyplot as plt

def my_plot(csv_file, column, H, B, y_label, x_label, title, incre_flag):
    #https://stackoverflow.com/questions/11244514/modify-tick-label-text
    #https://stackoverflow.com/questions/19125722/adding-a-legend-to-pyplot-in-matplotlib-in-the-simplest-manner-possible
    df = pd.read_csv(csv_file)
    original_data = list(df[column])
    if incre_flag == True:
        original_data = calculate_increment(original_data)
    original_date = list(df['date'])
    length = len(original_date)
    plt.plot(original_date, original_data, color='r', label="original")
    plt.legend(loc="upper left", fontsize='20')
    # plt.scatter(indices, original_china_deaths)
    hist_median = []
    for b in range(B):
        hist_median.append((H.start_r[b] + H.end_r[b]) / 2)

    for b in range(B):
        plt.bar(hist_median[b], H.hr[b], color='gray',
                width=(H.end_r[b] - H.start_r[b]), label="approx.")
        if(b == 0):
            plt.legend(loc="upper left", fontsize='20')

    plt.ylabel(y_label, size='20')
    plt.xlabel(x_label, size= '20')
    plt.title(title, size='20')

    index_tick = H.start_r
    index_tick.append(H.end_r[B - 1])

    mapped_date = date_mapping(original_date, index_tick)
    plt.xticks(index_tick, mapped_date, rotation='60')

    plt.show()

def date_mapping(date_list, bin_start_points):
    mapping_result = []
    for b in range(len(bin_start_points)):
        mapping_result.append(date_list[bin_start_points[b]])
    return mapping_result

def calculate_increment(tokens):
    new_tokens = []
    new_tokens.append(tokens[0])
    for i in range(1, len(tokens)):
        new_tokens.append(tokens[i] - tokens[i-1])
    return new_tokens


if __name__ == "__main__":
    B = 10
    delta = 0.02

    H_us_case = bh.Bucket_hist(B)
    H_us_case.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    H_us_case.AHIST_S(delta)

    H_us_case_dp = bh.Bucket_hist(B)
    H_us_case_dp.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    H_us_case_dp.HIST_DP()

    H_us_death = bh.Bucket_hist(B)
    H_us_death.read_data('stripped_data/us-cases-deaths.csv', 'deaths')
    H_us_death.AHIST_S(delta)

    H_us_death_dp = bh.Bucket_hist(B)
    H_us_death_dp.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    H_us_death_dp.HIST_DP()


    df_china = pd.read_csv('stripped_data/china-cases-deaths.csv')
    china_date = list(df_china['date'])
    df_us = pd.read_csv('stripped_data/us-cases-deaths.csv')
    us_date = list(df_us['date'])


    H_china_case = bh.Bucket_hist(B)
    H_china_case.read_data('stripped_data/china-cases-deaths.csv', 'cases')
    H_china_case.AHIST_S(delta)

    H_china_death = bh.Bucket_hist(B)
    H_china_death.read_data('stripped_data/china-cases-deaths.csv', 'deaths')
    H_china_death.AHIST_S(delta)

    H_us_new_cases = bh.Bucket_hist(B)
    H_us_new_cases.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    H_us_new_cases.calculate_increment()
    H_us_new_cases.AHIST_S(delta)

    H_us_new_cases_dp = bh.Bucket_hist(B)
    H_us_new_cases_dp.read_data('stripped_data/us-cases-deaths.csv', 'cases')
    H_us_new_cases_dp.calculate_increment()
    H_us_new_cases_dp.HIST_DP()

    #plot
    my_plot('stripped_data/us-cases-deaths.csv', 'cases', H_us_new_cases, B, 'cases', 'date', 'US New Cases', True)
    my_plot('stripped_data/china-cases-deaths.csv', 'cases', H_china_case, B, 'cases', 'date', 'China Cases', False)
    my_plot('stripped_data/china-cases-deaths.csv', 'deaths', H_china_death, B, 'deaths', 'date', 'China Deaths', False)
    my_plot('stripped_data/us-cases-deaths.csv', 'cases', H_us_case, B, 'cases', 'date', 'US Cases', False)
    my_plot('stripped_data/us-cases-deaths.csv', 'deaths', H_us_death, B, 'deaths', 'date', 'US Deaths', False)

    ## Uncomment following chunks to get new deaths histogram

    # H_us_new_deaths = bh.Bucket_hist(B)
    # H_us_new_deaths.read_data('stripped_data/us-cases-deaths.csv', 'deaths')
    # H_us_new_deaths.calculate_increment()
    # H_us_new_deaths.AHIST_S(delta)

    # H_us_new_deaths_dp = bh.Bucket_hist(B)
    # H_us_new_deaths_dp.read_data('stripped_data/us-cases-deaths.csv', 'deaths')
    # H_us_new_deaths_dp.calculate_increment()
    # H_us_new_deaths_dp.HIST_DP()

    ## Uncomment following chuncks to plot the comparision of AHIST-S and DP

    # plt.plot(H_us_case.start_r, H_us_case.hr, label="AHIST-S(approx.)")
    # plt.plot(H_us_case_dp.start_r, H_us_case_dp.hr, label="DP(non approx.)")
    # plt.scatter(H_us_case.start_r, H_us_case.hr)
    # plt.scatter(H_us_case_dp.start_r, H_us_case_dp.hr)
    # plt.title('Comparison of AHIST-S and DP (US total cases)')
    # plt.xlabel('index of date')
    # plt.ylabel('cases')
    # plt.legend(fontsize='12')
    # plt.show()

    # plt.plot(H_us_new_cases.start_r, H_us_new_cases.hr, label="AHIST-S(approx.)")
    # plt.plot(H_us_new_cases_dp.start_r, H_us_new_cases_dp.hr, label="V-Optimal(non approx.)")
    # plt.scatter(H_us_new_cases.start_r, H_us_new_cases.hr)
    # plt.scatter(H_us_new_cases_dp.start_r, H_us_new_cases_dp.hr)
    # plt.title('Comparison of AHIST-S and V-Optimal (US new cases)')
    # plt.xlabel('index of date')
    # plt.ylabel('cases')
    # plt.legend(loc="upper left")
    # plt.show()




