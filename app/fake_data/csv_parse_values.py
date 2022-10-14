import csv

with open('opa.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    print('insert into service_provider (name, display_name, cpf, email, phone_number, signal, description) VALUES ')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            print(f'(\'{row[0]}\', \'{row[1]}\',\'{row[2]}\',\'{row[3]}\',\'{row[4]}\',{row[5]},\'{row[6]}\'),')
            line_count += 1
    # print(f'Processed {line_count} lines.')