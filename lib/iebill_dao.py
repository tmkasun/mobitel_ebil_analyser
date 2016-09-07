class IEbill_Dao(object):
    def add_ebill(self, ebill):
        """
        Insert new bill information to exsisting or new mobile number
        :param ebill: An instance of Ebill
        """
        raise NotImplemented("add_ebill method has not implemented yet!Please contact dev support.")

    def get_ebills(self, mobile_number):
        """
        Get mobile number from DB, If not exist return False ,  True otherwise
        :param mobile_number: Mobile number needs to be fetch as a String
        """
        raise NotImplemented("get_ebill method has not implemented yet!Please contact dev support.")

    def add_new_mobile(self, mobile_number):
        """
        Add new mobile number record to DB
        :param mobile_number: Mobile number needs to be fetch as a String
        """
        raise NotImplemented("add_new_mobile method has not implemented yet!Please contact dev support.")
