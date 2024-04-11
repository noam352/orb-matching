from pygame import Color


class Orb:
    ORB_SIZE = 50  # Orb diameter in pixels
    ORB_MARGIN = 10  # Margin between orbs
    temp_size = 0

    def __init__(self, x: int, y: int, color: Color) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.perma_color = color
        self.falling = 0

    def get_pos(self) -> int:
        return (self.x, self.y)

    def set_pos(self, x, y) -> None:
        self.x = x
        self.y = y

    def get_color(self):
        return self.color

    def get_coordinates(self, fall=False) -> int:
        x = (
            ((self.ORB_SIZE + self.ORB_MARGIN) * (self.x))
            + self.ORB_MARGIN
            + (self.ORB_SIZE // 2)
        )
        y = (
            ((self.ORB_SIZE + self.ORB_MARGIN) * (self.y))
            + self.ORB_MARGIN
            + (self.ORB_SIZE // 2)
        )
        if fall and self.falling > 0:
            y -= self.falling
            self.falling -= 1

        return x, y

    def add_falling(self, inc):
        self.falling = (
            ((self.ORB_SIZE + self.ORB_MARGIN) * (inc))
            + self.ORB_MARGIN
            + (self.ORB_SIZE // 2)
        )
