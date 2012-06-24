class Slide(object):

    def __init__(x, y, z = 0, content = '', title = '', format = 'step slide', scale = 0, rotate_x = 0, rotate_y = 0, rotate_z = 0):
        self.__table = {'content': content, 'title': title, 'format': format, 'x': x, 'y': y, 'z': z, 'scale': scale, 'rotate_x': rotate_x, 'rotate_y': rotate_y, 'rotate_z': rotate_z}

    def __retrieve(self, key):
        return self.__table[key]

    def x(self):
        """
        returns x-position

        """

        return self.__retrieve('x')

    def y(self):
        """
        returns y-position

        """

        return self.__retrieve('y')

    def z(self):
        """
        returns z-position

        """

        return self.__retrieve('z')

    def rotate_x(self):
        """
        returns rotation in x-direction

        """

        return self.__retrieve('rotate_x')

    def rotate_y(self):
        """
        returns rotation in y-direction

        """
        return self.__retrieve('rotate_y')

    def rotate_z(self):
        """
        returns rotation in z-direction

        """

        return self.__retrieve('rotate_z')

    def content(self):
        """
        returns the text content of the slid

        """
        return self.__retrieve('content')

    def scale(self):
        """
        returns size of the slide

        """

        return self.__retrieve('scale')

    def format(self):
        """
        returns the type and transition of the slide
        """

        return self.__retrieve('format')

    def title(self):
        """
        returns the id and title of the slide

        """

        return self.__retrieve('title')

