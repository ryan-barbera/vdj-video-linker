from csv import DictReader, DictWriter


def csvtodict():
    with open('SONGLIST.csv','r', encoding='utf-8') as data:
        retval = list(DictReader(data))
    data.close()
    return retval
 
 
def dicttocsv(dict_data):
    csv_columns = ['TRACKLIST_VALUE','ONLINE_PATH','LOCAL_PATH','TIME_START','TIME_END','ALWAYS_USE']
    print("Data to add:")
    print(dict_data)
    try:
        with open('SONGLIST.csv', 'w', encoding='utf-8') as csvfile:
            writer = DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")