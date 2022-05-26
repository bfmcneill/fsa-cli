class Record:

    def __init__(self,account_id,record_date,debit,credit,memo):
        self.account_id = account_id
        self.record_date = record_date
        self.debit = debit
        self.credit = credit
        self.memo = memo

class Ledger():

    def __init__(self,account):
        self.account = account
        self.records = []

    def write(self,account_id,record_date,debit,credit,memo):
        record = Record(account_id,record_date,debit,credit,memo)
        self.records = [record] if not self.records else self.records.append[record]