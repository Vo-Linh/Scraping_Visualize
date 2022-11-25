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
    #========================================================
    filter  = []

    for idx in range(len(raw_data[1])):
        check = []
        check += [raw_data[0][idx].split(" ")[i] == raw_data[4][idx].split(" ")[i] for i in range(len(raw_data[0][idx].split(" ")))]
        filter.append(check)
    
    # ============== Get date ==============
    date = []

    for idx in range(len(raw_data)):
        current = ""
        for  i in range(len(filter[0])):
            if filter[0][i] == False:
                current += f"{raw_data[idx][0].split()[i-1]} "
                current += raw_data[idx][0].split()[i]
        date.append(current)
    
    # ============== Get column ==============
    column = []
    for idx in range(1, len(raw_data[0])):
        name_column = ""
        for  i in range(len(filter[idx])):
            if filter[idx][i]:
                name_column += f" {raw_data[0][idx].split()[i]}"
            else:
                break
        column.append(name_column)
    
    # ============== Get data ============== 
    datas = []
    for one_day in raw_data:
        data = []
        for idx in range(1, len(one_day)):  
            count = 0
            if idx == 18: # 
                for  i in range(len(filter[idx][:5])):
                    
                    if count != 0:
                        break
                    if filter[idx][i] == False:
                        count += 1
                        data.append(one_day[idx].split()[i])
            else:
                for  i in range(len(filter[idx])):
                    
                    if count != 0:
                        break
                    if filter[idx][i] == False:
                        count += 1
                        data.append(one_day[idx].split()[i])
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
    
    return pd.DataFrame(datas, columns= column, index = date)

if __name__ == "__main__":
    from scraping import getRawData

    url= "https://www.estesparkweather.net/archive_reports.php?date=202211"
    raw_data = getRawData(url)

    df = convert2DF(raw_data)
    print(df.head(1))