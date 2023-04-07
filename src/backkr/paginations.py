class Paginate:
    '''A pagination class for dict objects'''

    def __init__(self, object: list, by: int = 2):
        self.by = by
        self.object = [
            object[i: i + by]
            for i in range(0, len(object), by)
        ]
        self.index = -1

    def next(self):
        '''Get next object'''
        self.index += 1
        if self.index >= len(self.object):
            self.index = len(self.object)
            return None
        return self.object[self.index]

    def previous(self):
        '''Get previous object'''
        self.index -= 1
        if self.index < 0:
            self.index = -1
            return None
        return self.object[self.index]

    def latest(self, by_field: str = 'id'):
        '''Get the latest object'''
        return max(self.object, key=lambda obj: obj.get(by_field))

    def first(self):
        '''Get the first object'''
        return self.object[0]

    def get(self, by_field: str, value: str):
        '''Get single object'''
        for obj in self.object:
            if obj.get(by_field) == value:
                return obj
        return None

    def filter(self, by_field: str, value: str):
        '''Get objects matching field value'''
        return [obj for obj in self.object if obj.get(by_field) == value]

    def all(self):
        '''Get all objects'''
        return Paginate(object=self.object, by=self.by)

    def __str__(self):
        return '<Paginate Object>'

    def __repr__(self):
        return f'{self.__class__}(object={self.object}, by={self.by})'

    def __len__(self):
        return len(self.object)

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def __getitem__(self, index):
        return self.object[index]
    
    def __setitem__(self, index, value):
        self.object[index] = value

    def __delitem__(self, index):
        del self.object[index]

    def __call__(self):
        return self
    
    def __bool__(self):
        return bool(self.object)
    
    def __eq__(self, other):
        return self.object == other
    
    def __ne__(self, other):
        return self.object != other
    
    def __lt__(self, other):
        return self.object < other
    
    def __le__(self, other):
        return self.object <= other
    
    def __gt__(self, other):
        return self.object > other
    
    def __ge__(self, other):
        return self.object >= other
    
    def __add__(self, other):
        return self.object + other
    
    def __sub__(self, other):
        return self.object - other
    
    def __mul__(self, other):
        return self.object * other
    
    def __truediv__(self, other):
        return self.object / other
    
    def __floordiv__(self, other):
        return self.object // other
    
    def __mod__(self, other):
        return self.object % other
    
    def __pow__(self, other):
        return self.object ** other
    
    def __and__(self, other):
        return self.object & other
    
    def __or__(self, other):
        return self.object | other
    
    def __xor__(self, other):
        return self.object ^ other
    
    def __lshift__(self, other):
        return self.object << other
    
    def __rshift__(self, other):
        return self.object >> other
    
    def __iadd__(self, other):
        self.object += other
        return self
    
    def __isub__(self, other):
        self.object -= other
        return self
    
    def __imul__(self, other):
        self.object *= other
        return self
    
    def __itruediv__(self, other):
        self.object /= other
        return self
    
