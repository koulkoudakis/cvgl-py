"""
Author: Sharome Burton
Date: 02/11/2022

"""
import numpy as np
import cv2

from random import randint


class PixMatrix:
    def __init__(self,  size=(16, 9), img_size=(720, 1280, 3)):
        self.matrix = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        self.size = size
        self.img_size = img_size
        self.img = np.full(img_size, 123, np.uint8)

    def img_grid(self, rand=False):
        """

        :return:
        """
        n_rows = self.size[0]
        n_cols = self.size[1]

        row_width = self.img_size[1] // n_rows
        col_height = self.img_size[0] // n_cols

        for i in range(n_rows):

            for j in range(n_cols):
                if rand:
                    self.img = cv2.rectangle(self.img,
                                  (i*row_width, j*col_height),
                                  (i*row_width+row_width, j*col_height+col_height),
                                  (randint(0, 255), randint(0, 255), randint(0, 255)),
                                  -1
                                  )

    def get_img(self):
        """

        :return:
        """
        return self.img

    def get_matrix(self):
        """

        :return: (numpy array) - Array of pixel matrix
        """
        return self.matrix

    def mat_to_img(self):
        """

        :return:
        """
        n_rows = self.size[0]
        n_cols = self.size[1]

        row_width = self.img_size[1] // n_rows
        col_height = self.img_size[0] // n_cols

        for i in range(n_rows):

            for j in range(n_cols):

                self.img = cv2.rectangle(self.img,
                              (i*row_width, j*col_height),
                              (i*row_width+row_width, j*col_height+col_height),
                              (self.matrix[i][j][0], self.matrix[i][j][1], self.matrix[i][j][2]),
                              -1
                              )

    def paint_fill_matrix(self, xp, yp, color = (50, 50, 50)):
        n_rows = self.size[0]
        n_cols = self.size[1]

        row_width = self.img_size[1] // n_rows
        col_height = self.img_size[0] // n_cols

        # row = min([(xp - x for x in range(n_rows) if (xp - x) > 0)])
        row = (xp + row_width//2) // row_width
        print(f'ROW: {row}')


        # col = min([(yp - y for y in range(n_cols) if (yp - y) > 0)])
        col = (yp + col_height // 2) // col_height
        print(f'COL: {col}')

        self.img = cv2.rectangle(
            self.img,
            (row*row_width, col*col_height),
            (row*row_width + row_width, col*col_height + col_height),
            color,
            -1
        )
        return (row, col)

    def save_img(self, filename="sprite.png"):
        """

        :return:
        """
        cv2.imwrite(filename, self.img)
        print(f'SPRITE SAVED: {filename}')

    def show_img(self):
        """

        :return:
        """
        cv2.imshow('matrix', self.img)



if __name__ == '__main__':
    mat = PixMatrix()

    while True:
        mat.img_grid(rand=True)
        mat.show_img()
        cv2.waitKey(500)