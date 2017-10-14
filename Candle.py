import datetime


#  historical data for one part of the time
class Candle:

    filled = False
    __date = datetime.date(2001, 1, 1)
    __time = datetime.time(0, 0, 0)

    @staticmethod
    #  format: ddMMyyyy
    def convert_str_to_date(string):
        if len(string) != 8:
            return datetime.date(2001, 1, 1)
        try:
            return datetime.date(int(string[4:8]), int(string[2:4]), int(string[0:2]))
        except ValueError:
            return datetime.date(2001, 1, 1)

    @staticmethod
    #  format: HHMMSS
    def convert_str_to_time(string):
        if len(string) != 6:
            return datetime.time(0, 0, 0)
        try:
            return datetime.time(int(string[0:2]), int(string[2:4]), int(string[4:6]))
        except ValueError:
            return datetime.time(0, 0, 0)

    def init_datetime(self):
        self.__date = self.convert_str_to_date(self.date)
        self.__time = self.convert_str_to_time(self.time)
        if self.__date == datetime.date(2001, 1, 1) or self.__time == datetime.time(0, 0, 0):
            return False
        return True

    def __fill_from_string(self, data):

        array = data.split(';')
        if len(array) == 7:
            try:
                self.date = array[0]
                self.time = array[1]
                self.open = float(array[2])
                self.high = float(array[3])
                self.low = float(array[4])
                self.close = float(array[5])
                self.volume = int(array[6])
                if self.init_datetime():
                    self.filled = True
            except ValueError:
                self.filled = False
        else:
            if len(data.rstrip()) > 1:
                print("Invalid format of input string: " + data)
            self.filled = False

    def __init__(self):
        pass

    def to_string(self):

        res = '{0};{1};{2:.4f};{3:.4f};{4:.4f};{5:.4f};{6}'.format(
            self.date, self.time, self.open, self.high, self.low, self.close, self.volume)
        return res

    @staticmethod
    #  create a new candle from input string
    def from_string(data):
        res = Candle()
        res.__fill_from_string(data)
        return res

    @staticmethod
    #  create a new candle from other candle (source)
    def from_candle(source):
        res = Candle()
        res.date = source.date
        res.time = source.time
        if res.init_datetime():
            res.filled = True
        else:
            res.filled = False
        return res

    @staticmethod
    #  calculate spread
    def make_spread(_candle1, _factor1, _candle2, _factor2):
        res = Candle.from_candle(_candle1)
        res.open = _candle1.open * _factor1 - _candle2.open * _factor2
        res.high = _candle1.high * _factor1 - _candle2.high * _factor2
        res.low = _candle1.low * _factor1 - _candle2.low * _factor2
        res.close = _candle1.close * _factor1 - _candle2.close * _factor2
        res.volume = min(_candle2.volume, _candle1.volume)
        return res

    def is_older(self, candle):
        return self.__date < candle.__date or (self.__date == candle.__date and self.__time < candle.__time)

    def is_same_time(self, candle):
        return self.__date == candle.__date and self.__time == candle.__time
