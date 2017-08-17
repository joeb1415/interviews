green = 'green'
yellow = 'yellow'
red = 'red'


class Light:
    def __init__(self, direction, green_time=8, yellow_time=3, red_time=2):
        self.direction = direction  # ns or ew
        self.color_length = {
            green: green_time,
            yellow: yellow_time,
            red: red_time,
        }
        self.next_color = {
            green: yellow,
            yellow: red,
            red: green
        }
        self.color = red  # initialize as 'red'
        self.is_active = False

    def set_color(self, color):
        self.color = color
        if self.color == green:
            self.is_active = True
        return self.color_length[color]

    def set_next_color(self):
        if self.color in [green, yellow]:
            return self.set_color(self.next_color[self.color])
        else:  # self.color == red
            if self.is_active:
                self.is_active = False
                return None
            else:
                return self.set_color(green)