import pandas as pd


def convert2DF(raw_data):
    """
    raw_data: data get from scraping website

    return Data Frame save data each day.
    """
    # ======================================================
    # Check same element each row in all day
    # IF same in all row will return True
    # Else return Flase and save in filter
    #
    # ========================================================
    filter = []
    column = ["Average temperature", "Average humidity", "Average windspeed"]
    for idx in range(1, len(raw_data[1]) + 1):
        check = []

        if "Average temperature" in raw_data[0][idx] or "Average humidity" in raw_data[0][idx] or "Average windspeed" in raw_data[0][idx]:
            check += [raw_data[0][idx].split(" ")[i] == raw_data[4][idx].split(
                " ")[i] for i in range(len(raw_data[4][idx].split(" ")))]

            filter.append(check)
        if len(filter) == 3:
            break

    # ============== Get date ==============
    # Get date
    date = []
    check = [raw_data[1][0].split(" ")[i] == raw_data[2][0].split(" ")[i] 
                for i in range(len(raw_data[1][0].split(" ")))]

    for idx in range(len(raw_data)):
        current = ""
        for i in range(len(check)):
            if check[i] == False:
                current += f"{raw_data[idx][0].split()[i-1]} "
                current += raw_data[idx][0].split()[i]
        date.append(current)

    # ============== Get data ==============
    datas = []
    num_feature = 3 # get fist 7th column of data [Average temperature, Average humidity, Average dewpoint, Average barometer, Average windspeed, Average gustspeed, Average direction]
    for one_day in raw_data:
        data = []
        count = 0
        for idx in range(1, len(one_day)):
            if "Average temperature" in one_day[idx] or "Average humidity" in one_day[idx] or "Average windspeed" in one_day[idx]:
                for  i in range(len(filter[count])):
                    if filter[count][i] == False:
                        data.append(one_day[idx].split()[i])
                count = + 1
        datas.append(data)

    # ============== remove unit ==============
    for idx in range(len(datas)):
        for i in range(len(column)):
            if "F" in datas[idx][i]:
                datas[idx][i] = float(datas[idx][i][:-2])
            elif "%" in datas[idx][i] or "°" in datas[idx][i]:
                datas[idx][i] = float(datas[idx][i][:-1])
            else:
                datas[idx][i] = float(datas[idx][i])

    return pd.DataFrame(datas, columns=column[:num_feature], index=date), date


if __name__ == "__main__":
    from scraping import getRawData

    url = "https://www.estesparkweather.net/archive_reports.php?date=202001"
    raw_data = getRawData(url)

    df, date = convert2DF(raw_data)
    print(df.head(1))
