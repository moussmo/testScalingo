

def parse_date(date_str):
    #Takes a date string ; returns it in (day,month,year) as ints
    L = date_str.split("/")
    day= int(L[0])
    month= int(L[1])
    year= int(L[2])
    return (day,month,year)
