import unittest
from movement import operator
import time

class TestOperator(unittest.TestCase):

    def setUp(self):
        self.o = operator()
        self.sx = self.o.screen_x_len
        self.sy = self.o.screen_y_len

    def tearDown(self):
        self.o.close()

    def _test_init_operator(self):
        o = self.o
        self.assertEqual(o.x_pos, int(self.sx*3/4))
        self.assertEqual(o.y_pos, int(self.sy*1/2))

    def _test_pos_mapping(self):
        o = self.o
        #o._pointer_pos_init()
        #o._to_b_r()

        o.move_along_bezier_curve(-100, -100,rel=True, pause=True)
        o.move_along_bezier_curve(100, 100,rel=True, pause=True) # move 100 bonding box

        o.move_along_bezier_curve(-200, 0,rel=True, pause=True)
        o.move_along_bezier_curve(-200, 0,rel=True, pause=True)

        o.move_along_bezier_curve(0, -200,rel=True, pause=True)
        o.move_along_bezier_curve(0, -200,rel=True, pause=True)
        self.assertTrue(True)

    def _test_drag(self):
        o = self.o
        print("move the mouse to the place for starting drag")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print(o.button_state)
        print("pressed down")
        o.click(0) # click to let it focus
        print(o.button_state)
        o.press_down(0)
        print(o.button_state)
        o.move_along_bezier_curve(0, -100,rel=True, pause=True)
        o.press_down(1)
        o.move_along_bezier_curve(100, 0,rel=True, pause=True)
        o.release_all_buttons()

        time.sleep(1)
        #o.press_down(2)
        o.click(2)
        o.move_along_bezier_curve(-100, 100,rel=True, pause=True)
        print(o.button_state)
        print("let it go")
        o.release_all_buttons()
        print(o.button_state)

        self.assertTrue(True)

    def _test_click(self):
        o = self.o
        print("move the mouse to the place for clicking")
        time.sleep(3)
        o.click(1)

        print("move the mouse to the place for clicking")
        time.sleep(3)
        o.click(0)

        print("move the mouse to the place for clicking")
        time.sleep(3)
        o.click(2)
        self.assertTrue(True)

    def test_moving_rel(self):
        o = self.o
        #o._pointer_pos_init()
        #o._to_b_r()

        #o.move_along_bezier_curve(-100, -100,rel=True, pause=True)
        #o.move_along_bezier_curve(100, 100,rel=True, pause=True) # move 100 bonding box

        time.sleep(1)


        o.move_along_bezier_curve(-200, -200,rel=True, pause=True)
        time.sleep(3)
        print(o.x_pos, o.y_pos)
        #o.move_along_bezier_curve(-300, 0,rel=True, pause=True)

        time.sleep(1)
        o.press_down(0)
        for _ in range(10):
            o.move_along_bezier_curve(300, 300,rel=True, pause=True)
            time.sleep(3)
            print(o.x_pos, o.y_pos)
            o.move_along_bezier_curve(0, -300,rel=True, pause=True)
            time.sleep(3)
            print(o.x_pos, o.y_pos)
            o.move_along_bezier_curve(-300, 0,rel=True, pause=True)
            time.sleep(3)
            print(o.x_pos, o.y_pos)
        #o.move_along_bezier_curve(0, -300,rel=True, pause=True)
        #self.assertTrue(True)
        #o.move_relative(-200, 0)
        #o.move_relative(0, -200)
        o.release_all_buttons()
        self.assertTrue(True)

    def _test_move_and_record_pos(self):
        o = self.o

        x_pos = o.x_pos
        y_pos = o.y_pos
        sx = o.screen_x_len
        sy = o.screen_y_len
        o.move_relative(-sx,-sy) # from (0,0)
        self.assertEqual(o.x_pos, 0)
        self.assertEqual(o.y_pos, 0)

        x_r = int(sx/3)
        y_r = int(sy/3)
        o.move_relative(sx/3,sy/3)
        self.assertEqual(o.x_pos, x_r)
        self.assertEqual(o.y_pos, y_r)

    def _test_b_curve(self):
        o = self.o

        sx = o.screen_x_len
        sy = o.screen_y_len

        o.move_along_bezier_curve(sx//4, sy//4)
        self.assertEqual(o.x_pos, sx//4)
        self.assertEqual(o.y_pos, sy//4)

        o.move_along_bezier_curve(sx//2, sy//2,pause=True)
        self.assertEqual(o.x_pos, sx//2)
        self.assertEqual(o.y_pos, sy//2)

        x=o.x_pos
        y=o.y_pos
        o.move_along_bezier_curve(sx//3, sy//3,rel=True)
        self.assertEqual(o.x_pos, x+sx//3)
        self.assertEqual(o.y_pos, y+sy//3)

if __name__ == '__main__':
    unittest.main()
