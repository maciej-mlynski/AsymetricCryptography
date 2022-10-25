'''Curve operations are essential for public key generation, signing & verifing messages, endocing & decoding messages'''



class ElipticCurveOperations:
    
    def __init__(self):
        self.P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime
        self.A = 0
        self.B = 7
        self.g = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
                    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
        self.n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

    
    def inverse_mod(self, k, p):

        if k == 0:
            raise ZeroDivisionError('x1 = x2 -> x1 - x2 = 0 -> number/0 -> You can not divide by 0!!')
        if k < 0:
            # k can not be negative number (-1 * -k = k)
            return p - self.inverse_mod(-k, p)

        return pow(k, -1, p)
    
    
    def is_on_curve(self, point):
        
        # check if generated point is on the curve
        # it will make us sure that all operations are legit
    
        if point is None:
            return True

        x, y = point
        return (y**2 - x**3 - self.A*x - self.B) % self.P == 0
        
    
    def point_add(self, point1, point2):
        
        assert self.is_on_curve(point1)
        assert self.is_on_curve(point2)
        
        # coordinates of the point1
        x1, y1 = point1
        # coordinates of the point2
        x2, y2 = point2
        
        lamb = (y1 - y2) * self.inverse_mod(x1 - x2, self.P)
        
        x3 = lamb**2 - x1 - x2
        y3 = lamb * (x1 - x3) - y1
        
        new_point = (x3 % self.P, y3 % self.P)
        assert self.is_on_curve(new_point)
        
        return new_point
        

    def point_double(self, point):
        
        assert self.is_on_curve(point)
        
        # coordinates of the point
        x, y = point
        
        lamb = (3 * x**2 + self.A) * self.inverse_mod(2 * y, self.P)
        
        x2 = lamb**2 - 2*x
        y2 = lamb * (x - x2) - y
        
        new_point = (x2 % self.P, y2 % self.P)
        
        assert self.is_on_curve(new_point)
        
        return new_point
    
    def point_multiply(self, value, point=None):
        
        
        # To generate public key -> our point is equal to g coordinates
        # But we use multiplication also to sign & verify message and in that case our point should be equal to publick key coordinates, whcih should be provided in method args
        if point == None:
            point = self.g
            

        if value >= self.n  or value == 0:
            raise KeyError('Invalid private Key or Generator')
        
        # set iterator as 0
        i = 0
        # shift all digits to the right after each loop untill binary sk equal 0
        while value:
            
            # when it finds the first value from right in binary sk is 1
            if value & 1 and i == 0:
                # set res as previous pk
                res = point
                i += 1
                
            # for next 1 values do the method point_add
            elif value & 1 and i > 0:
                res = self.point_add(res, point)
    
            point = self.point_double(point)
            
            # Binary right shift method
            value >>= 1
                        
        return res