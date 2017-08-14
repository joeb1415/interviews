from time import sleep
from light import green, yellow, red


class Intersection:
    def __init__(self, lights):
        self.lights = lights
        self.active_light = 0
        self.dir_count = len(self.lights)

    def add_light(self, light):
        self.lights.append(light)

    def run(self, duration):
        cycle_time = self.lights[0].set_color(green)
        self.active_light = 0
        for light in self.lights[1:]:
            _ = light.set_color(red)

        for t in range(duration):
            cycle_time -= 1

            message = 'Time: {time}, {lights}'.format(
                time=t,
                lights=', '.join(
                    'Light {dir}: {color}'.format(
                        dir=light.direction, color=light.color
                    ) for light in self.lights
                )
            )
            print(message)

            if cycle_time > 0:
                continue

            cycle_time = self.lights[self.active_light].set_next_color()

            # if we've finished a red cycle, begin next direction
            if cycle_time is None:
                self.active_light = (self.active_light + 1) % self.dir_count
                cycle_time = self.lights[self.active_light].set_next_color()

