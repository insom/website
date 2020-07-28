import operator

def checkModTen(cc):
        digits = map(int, cc)
        for i in range(-2, -(len(digits)) - 2, -2):
                twice = digits[i] * 2
                d, r = divmod(twice, 10)
                digits[i] = d + r
        sum = reduce(operator.add, digits)
        checksum = (sum % 10)
        return checksum == 0
