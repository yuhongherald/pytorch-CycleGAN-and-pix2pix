from gdrive import gdrive

def main():
    file_id='1Ubi4-MJflgn5J_5erkd7sZLNJxFwk93aZtSruOEWBUo'
    ranges='Sheet!' #1:2 first 2 rows
    current_row = 2
    num_columns = 6
    headers = ['Timestamp', 'Photo', 'class', 'name', 'Background', 'Image']

    drive = gdrive('credentials.json')
    current_row, data = drive.getData(file_id, current_row, num_columns)
    csv_file.writerow(['filename', 'class', 'background'])
    with open('class.csv', 'w') as csv_file:
        for row in data:
            id = row[5].split('id=', 1)[1]
            print(id)
            filename = drive.download(id) #customize with name later
            if row[1] == 'Photo':
                # convert to edges
                
                # save to test folder
            else:
                # save to test folder

                # write entry in csv file
            csv_file.writerow([filename,row[3], row[4]])
    
if __name__ == '__main__':
    main()