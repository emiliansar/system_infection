class Cell:
    def __init__(
        self,
        type='cell',
        bg_color=(25, 25, 25),
        image=None,
        unit_type=None,
        unit_name=None
    ):
        self.bg_color = bg_color
        self.type = type
        self.image = image
        self.unit_type = unit_type
        self.unit_name = unit_name