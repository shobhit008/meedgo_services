from datetime import datetime

def order_number(user_id):
    dateTime = datetime.now()
    return ("Med"+str(dateTime.year)+str(dateTime.month)+str(dateTime.day)+str(dateTime.hour)+str(dateTime.minute)+str(dateTime.second)+str(user_id))