from datetime import datetime

def order_number(user_id, id_type = "Med_"):
    dateTime = datetime.now()
    return (id_type+str(dateTime.year)+str(dateTime.month)+str(dateTime.day)+str(dateTime.hour)+str(dateTime.minute)+str(dateTime.second)+str(user_id))