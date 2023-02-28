import os
import sys
import time
from typing import Callable


class Autoload(object):
    '''Autoload all files in a directory tree and reload the app when a file is modified'''

    def __init__(self, path: str, callback: Callable = None) -> None:
        self.path: str = path
        self.callback: Callable = callback
        self.last_modified: int = 0
        self.interval: int = 1

    def check(self) -> None:
        '''Check if a file has been modified'''
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    # print(path)
                    last_modified = os.stat(path).st_mtime
                    if last_modified > self.last_modified:
                        self.last_modified = last_modified
                        if self.callback:
                            self.callback()
                        else:
                            self.reload()

    def reload(self) -> None:
        '''Reload the app'''
        print('Reloading...')
        os.execv(sys.executable, ['python'] + sys.argv)


    def watch(self) -> None:
        '''Watch for file changes'''
        while True:
            self.check()
            time.sleep(self.interval)
            

    def __call__(self):
        self.check()

    def __repr__(self) -> str:
        return f'Autoload({self.path})'

    def __str__(self) -> str:
        return f'Autoload({self.path})'


# if __name__ == '__main__':
#     def callback():
#         print('callback')

#     autoload = Autoload('.', callback)
#     autoload()
#     autoload.watch()
