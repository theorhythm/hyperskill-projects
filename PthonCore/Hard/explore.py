import pandas as pd
import requests
import os


# scroll down to the bottom to implement your solution
def count_bigger_5(sr):
    return sr[sr > 5].count()


if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    df_A = pd.read_xml("../Data/A_office_data.xml")
    df_B = pd.read_xml("../Data/B_office_data.xml")
    df_hr = pd.read_xml("../Data/hr_data.xml")

    name_A = ['A' + str(i) for i in df_A["employee_office_id"]]
    name_B = ['B' + str(i) for i in df_B["employee_office_id"]]
    df_A.index = name_A
    df_B.index = name_B

    df_hr.set_index('employee_id', inplace=True)
    df_uni = pd.concat([df_A, df_B])
    df_m = df_uni.merge(df_hr, left_index=True, right_index=True, how='inner', indicator=True)
    df_mn = df_m.drop(columns=["employee_office_id", "_merge"])
    df_f = df_mn.sort_index()

    # stage 2
    # print(list(df_f.index))
    # print(list(df_f.columns))

    # stage 3
    # top10 = df_f.sort_values(by="average_monthly_hours", ascending=False).Department[:10]
    # projects = df_f.query("Department == 'IT' & salary == 'low'").number_project.sum()
    # spec = df_f.loc[["A4", "B7064", "A3033"], ["last_evaluation", "satisfaction_level"]]
    #
    # print(list(top10))
    # print(projects)
    # print(spec.values.tolist())

    # stage 4
    # df_a = df_f.groupby('left').agg({'number_project': ['median', count_bigger_5],
    #                                  'time_spend_company': ['mean', 'median'],
    #                                  'Work_accident': ['mean'],
    #                                  'last_evaluation': ['mean', 'std']}).round(2)
    # print(df_a.to_dict())

    # stage 5
    df_p1 = df_f.pivot_table(index="Department", columns=["left", "salary"], values="average_monthly_hours",
                             aggfunc='median')
    df_p1_sub = df_p1.loc[(df_p1[(0, 'high')] < df_p1[(0, 'medium')]) | (df_p1[(1, 'high')] > df_p1[(1, 'low')])]

    df_p2 = df_f.pivot_table(index="time_spend_company",
                             columns="promotion_last_5years",
                             values=["satisfaction_level", "last_evaluation"],
                             aggfunc=['min', 'max', 'mean'])
    df_p2_sub = df_p2.loc[df_p2[('mean', 'last_evaluation', 0)] > df_p2[('mean', 'last_evaluation', 1)]]
    print(df_p1_sub.to_dict())
    print(df_p2_sub.to_dict())
