import csv

if __name__ == "__main__":
    cherbourgers: int = 0
    survived_cherbourgers: int = 0
    total_m: int = 0
    total_w: int = 0
    surv_m: int = 0
    surv_w: int = 0

    with open('train.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[11] == 'C':
                cherbourgers += 1
                if row[4] == 'male':
                    total_m += 1
                else:
                    total_w += 1
                if row[1] == '1':
                    survived_cherbourgers += 1
                    if row[4] == 'male':
                        surv_m += 1
                    else:
                        surv_w += 1

    ch_list = []
    with open('test.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[10] == 'C':
                cherbourgers += 1
                if row[3] == 'male':
                    total_m += 1
                else:
                    total_w += 1
                ch_list.append(row)

    with open('gender_submission.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for cherbourger in ch_list:
                if row[0] == cherbourger[0]:
                    if row[1] == '1':
                        survived_cherbourgers += 1
                        if cherbourger[3] == 'male':
                            surv_m += 1
                        else:
                            surv_w += 1

    print(f'Общее количество пассажиров, севших в порту Шербур составляет {cherbourgers} человек.')
    print(f'Выжило из них при крушении титаника {survived_cherbourgers} - {round((survived_cherbourgers / cherbourgers) * 100)}%.')
    print(f'Мужчины: село {total_m}; выжило {surv_m} - {round((surv_m / total_m) * 100)}%')
    print(f'Женщины: село {total_w}; выжило {surv_w} - {round((surv_w / total_w) * 100)}%')
