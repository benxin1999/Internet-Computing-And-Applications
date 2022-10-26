import time

def extract_bill(obj):
    bill = {
        'id':obj.id,
        'source_type': obj.source_type,
        'bill_amount': obj.bill_amount,
        'category_name': obj.category_name,
        'category_id': obj.category_id,
        'bill_remark': obj.bill_remark,
        'bill_date': obj.bill_date,
        'category_icon_name': obj.category_icon_name
    }
    return bill

def time_period(str_time):
    map = {'1':31,'2':28,'3':31,'4':30,'5':31, '6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
    day = 86399
    try:
        start = time.mktime(time.strptime(str_time, "%Y-%m"))
        end = start + day*map[str_time.split('-')[1]]
    except :
        try:
            start = time.mktime(time.strptime(str_time, "%Y-%m-%d"))
            end = start + day
        except Exception as e:

            return 0,0

    return start*1000, end*1000


def date(timestamp):
    t = int(timestamp)
    t /= 1000
    dt = time.strftime("%Y-%m-%d", time.localtime(t))
    return dt

def details(obj):
    income, expense = 0, 0
    for e in obj:
        if e.source_type == 'expense':
            expense += int(e.bill_amount)
        elif e.source_type == 'income':
            income += int(e.bill_amount)
    return income, expense

def bills_count(list):
    count = 0
    for e in list:
        count += len(e['bills'])
    return count