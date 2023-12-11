import csv

FILES_TO_READ = ('titanic.csv',)

if __name__ == "__main__":
    cherbourgers: int = 0
    survived_cherbourgers: int = 0
    total_m: int = 0
    total_w: int = 0
    surv_m: int = 0
    surv_w: int = 0

    for path in FILES_TO_READ:
        try:
            with open(path, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                gender_index = headers.index('Sex')
                embarkation_index = headers.index('Embarked')
                survived_index = headers.index('Survived')
                for row in reader:
                    if row[embarkation_index] == 'C':
                        cherbourgers += 1
                        if row[gender_index] == 'male':
                            total_m += 1
                        else:
                            total_w += 1
                        if row[survived_index] == '1':
                            survived_cherbourgers += 1
                            if row[gender_index] == 'male':
                                surv_m += 1
                            else:
                                surv_w += 1
        except FileNotFoundError:
            print('------------------')
            print(f'Файла {path} не существует, данные из него не прочитаны')
            print('------------------')

    print(f'Общее количество пассажиров, севших в порту Шербур составляет {cherbourgers} человек.')
    print(
        f'Выжило из них при крушении титаника {survived_cherbourgers} - {round((survived_cherbourgers / cherbourgers) * 100)}%.')
    print(f'Мужчины: село {total_m}; выжило {surv_m} - {round((surv_m / total_m) * 100)}%')
    print(f'Женщины: село {total_w}; выжило {surv_w} - {round((surv_w / total_w) * 100)}%')
