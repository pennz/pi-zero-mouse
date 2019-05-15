import numpy as np
from numpy.random import normal
import time
import math

def _clip(v,min_v, max_v):
    if v > max_v:
        return max_v
    if v < min_v:
        return min_v
    return v

class operator():
    def __init__(self, g_n='/dev/hidg0'):
        self.gadget_name = g_n
        self.dev_pf = open(self.gadget_name, "wb", buffering=0)
        self._pointer_accuracy = 0 # for debug

        self.screen_x_len = 1080
        self.screen_y_len = 2340 # not pixel perfect, don't bother
        self.x_max=127
        self.x_min=-127
        self.y_max=127
        self.y_min=-127

        self.x_pos = -1
        self.y_pos = -1

        self.button_state = 0 
        self._blank_state = self._mouse_op_to_binary(0,0, button_click=-1)
        self._pasue_time_table_init()

        self._debug_pause = 30/1000
        self._init_pause  = 200/1000
        self._pointer_pos_init()


    def _pasue_time_table_init(self):
        init_pause_time = 20 # ms
        end_pause_time = 30 # ms
        mid_pause_time = 0 # fatest

        mid_place = 70 # /100
        end_place = 100

        self._pause_time_table = np.array([
            (init_pause_time*(mid_place-i) + mid_pause_time*i)/mid_place \
                    if i < mid_place else \
            (mid_pause_time*(end_place-i) + end_pause_time*(i-mid_place))/(end_place-mid_place) \
                for i in range(end_place)])

    def _pointer_pos_init(self):
        # go to middle to the right (right thrumb)
        # first to to right
        # then to the bottom
        #
        # then go middle and left a little
        self._to_b_r(self._init_pause)
        #time.sleep(1)
        self.move_relative(-self.screen_x_len/4, -self.screen_y_len/2, self._init_pause)
        #time.sleep(1)

    def _update_pos(self,x,y, rel=True):
        if rel:
            x += self.x_pos
            y += self.y_pos

        self.x_pos = _clip(x,0,self.screen_x_len)
        self.y_pos = _clip(y,0,self.screen_y_len)

    def _to_b_r(self, pause_time):
        for _ in range(19):
            self._write_move_relative(self.x_max, self.y_max, sleep_time=pause_time)
        self.x_pos=self.screen_x_len
        self.y_pos=self.screen_y_len

    def move_relative(self,x,y, pause_time):
        x_sign = 1 if x > 0 else -1
        y_sign = 1 if y > 0 else -1

        x_abs = abs(x)
        y_abs = abs(y)
        x_steps = int(x_abs // self.x_max) # assume x_max and x_min same magnitude.
        y_steps = int(y_abs // self.y_max)

        if (x_steps < 1 and y_steps < 1):
            self._write_move_relative(x, y)
            self._update_pos(x,y)
            return

        x_remain = int(x_abs % self.x_max)
        y_remain = int(y_abs % self.y_max)

        for _ in range(min(x_steps, y_steps)):
            self._write_move_relative(x_sign*self.x_max, y_sign*self.y_max, sleep_time=pause_time)
        if x_steps >= y_steps: # go x, still need to x
            y_extra_sign = 0
        else: # go y
            y_extra_sign = 1
        for _ in range(abs(x_steps - y_steps)):
            self._write_move_relative((1-y_extra_sign)*x_sign*self.x_max, y_extra_sign*y_sign*self.y_max, sleep_time=pause_time)

        self._write_move_relative(x_remain*x_sign, y_remain*y_sign, sleep_time=pause_time)
        self._update_pos(x,y)

    def _mouse_op_to_binary(self,x,y,button_click=-1, button_release=False):
        bytes_3 = bytearray()
        if button_release:
            self.button_state = 0 # reset state
        else: # normal click or simply not click
            if (button_click >= 0 and button_click < 3):
                self.button_state = self.button_state | 1 << button_click
        #bytes_3.append(button_report.to_bytes(1,'big',signed=False))
        bytes_3.append(self.button_state)

        x_report = _clip(x, self.x_min, self.x_max)
        y_report = _clip(y, self.y_min, self.y_max)
        bytes_3.append(x_report.to_bytes(1,'big',signed=True)[0])
        bytes_3.append(y_report.to_bytes(1,'big',signed=True)[0])

        return bytes_3


    def close(self):
        if self.dev_pf: self.dev_pf.close()

    def _write_move_relative(self, x,y, sleep_time=0):
        if sleep_time > 0: time.sleep(sleep_time)
        #print( (x,y) )
        binary_24_bits = self._mouse_op_to_binary(x,y)
        self.dev_pf.write(bytes(binary_24_bits))

    # reference https://www.codeproject.com/Tips/759391/Emulate-Human-Mouse-Input-with-Bezier-Curves-and-G
    def move_click(self, x, y, button, pause=False, rel=False):
        """
        move_click not relative for x,y here
        """
        # target x and y, more nature, you can't be that accurate
        # so need to consider the boxing box when try to click
        x += normal()*self._pointer_accuracy
        y += normal()*self._pointer_accuracy

        self.move_along_bezier_curve(x,y, pause)
        self.click(button)

    def move_along_bezier_curve(self, x,y, pause=False, rel=False):
        _x = x
        _y = y
        if rel:
            x += self.x_pos
            y += self.y_pos

        orig_x = self.x_pos
        orig_y = self.y_pos

        mid_point_x = (x - orig_x)/2
        mid_point_y = (y - orig_y)/2

        mid_distance = math.sqrt(mid_point_x*mid_point_x+mid_point_y*mid_point_y)
        #Find a co-ordinate normal to the straight line between start and end point, starting at the midpoint and normally distributed
        #This is reduced by a factor of 4 to model the arc of a right handed user.
        bezier_mid_x = int(mid_distance/4 * normal())+mid_point_x+orig_x
        bezier_mid_y = int(mid_distance/4 * normal())+mid_point_y+orig_y

        l_pause = len(self._pause_time_table)
        num_data_points = int(30 * mid_distance*2/700)
        num_data_points = _clip(num_data_points,0, l_pause+1) # trace will minus 1

        trace = beizier_curve_quad(orig_x,orig_y,bezier_mid_x, bezier_mid_y,
               x, y, n=num_data_points)
        trace = [self._clip_in_screen( ( int(round(c[0])), 
            int(round(c[1])) ) ) for c in trace]
        trace = [(trace[i+1][0]-trace[i][0], 
            trace[i+1][1]-trace[i][1]) for i in range(len(trace)-1)]

        if pause:
            pause_counts = 20
            pause_counts = _clip(pause_counts,0, num_data_points)

            #step_length_for_pause = num_data_points // pause_counts # clipped

            # for pause time (speed), just triangle,(easier)(in fact, could also
            # try bezier. just use easier one for test
            pre_p_t = self._pause_time_table[
                np.linspace(0, l_pause-1, pause_counts, endpoint=True, dtype=int)]
            pause_time_sum = self._get_pause_time_sum(_x,_y,rel)
            sleep_time_normalized = pause_time_sum/1000 * pre_p_t / pre_p_t.sum()

            p_t_idx = np.linspace(0, num_data_points-1, pause_counts, endpoint=True, dtype=int)
            sleep_time = np.zeros( (num_data_points,) )
            for pre_i,idx in enumerate(p_t_idx):
                sleep_time[idx] = sleep_time_normalized[pre_i]

            for i,c in enumerate(trace):
                self._write_move_relative(c[0],c[1], sleep_time=self._debug_pause+sleep_time[i])
                #if sleep_time[i] > 0: time.sleep(sleep_time[i]) # sleep more
        else:
            for c in trace:
                self._write_move_relative(c[0],c[1], sleep_time=self._debug_pause)

        self._update_pos(_x,_y, rel)


    def press_down(self, button):
        binary_24_bits = self._mouse_op_to_binary(0,0, button) # button down, up use release_all_buttons
        self.dev_pf.write(bytes(binary_24_bits))

    def release_all_buttons(self):
        binary_24_bits = self._mouse_op_to_binary(0,0,button_release=True) # button down, up use release_all_buttons
        self.dev_pf.write(bytes(binary_24_bits))

    def click(self, button):
        self.press_down(button)
        self.release_all_buttons()

    def _get_pause_time_sum(self, x,y,rel=True):
        if not rel:
            x -= self.x_pos
            y -= self.y_pos
        return math.sqrt(x*x+y*y)/200 * 150 # ms, for 200 pixels

    def _clip_in_screen(self, c):
        return (_clip(c[0], 0, self.screen_x_len),
                _clip(c[1], 0, self.screen_y_len))

def beizier_curve_quad(orig_x,orig_y,bezier_mid_x, bezier_mid_y, target_x, target_y, n=100):
    #np.array
    ts = np.linspace(0,1,n,endpoint=True)
    return [( (1-t)**2*orig_x+2*(1-t)*t*bezier_mid_x+t*t*target_x,
     (1-t)**2*orig_y+2*(1-t)*t*bezier_mid_y+t*t*target_y ) for t in ts]

if __name__ == "__main__":
    o = operator()
    o.move_along_bezier_curve(500, 500)
