class Account:
    def __init__(self, balance):
        self.balance = balance

    def _register_express__transfer(self, amount):
        self.balance += amount
        return True

    def __register_transfer(self, amount):
        self.balance += amount
        return True

    def try_register_incoming_transfer(self, amount):
        if amount <= 0:
            return False

        return self.__register_transfer(amount)


    def try_register_outgoing_transfer(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False

        return self.__register_transfer(-amount)