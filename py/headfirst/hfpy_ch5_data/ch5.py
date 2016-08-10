def sanitize(time_string):
    if '-' in time_string :
        spliter = '-'
    elif ':' in time_string:
        spliter = ':'
    else:
        return time_string
    (mins, secs) = time_string.split(spliter)
    return mins + '.' + secs

def get_coach_data(filename):
    try:
        with open(filename) as f:
            data=f.readline()
        return data.strip().split(',')
    except IOError as ioerr:
        print ('file error' + str(ioerr))
        return (None)


sarah=get_coach_data("sarah.txt")
print(sarah)
sarah=[sanitize(item) for item in sarah]
print(sorted(set(sarah))[0:3])
sss={1,2,3,3}
print(sss)
