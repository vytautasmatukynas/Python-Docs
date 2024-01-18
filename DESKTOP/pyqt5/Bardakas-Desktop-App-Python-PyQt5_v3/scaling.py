import ctypes

class pt_points:
    def __init__(self):
        # get windows scale ratio and aware of DPI change
        user32 = ctypes.windll.user32

        self.scale_factor = user32.GetDpiForSystem() / 96.0
        # print("Scale factor:", scale_factor)

        self.TEXT_PT = 10
        self.TEXT_PT_TABLE = 10
        self.TEXT_BUTTON_PT = 10

        self.BUTTON_HEIGHT = int(25 * self.scale_factor)
        self.BUTTON_WIDTH = int(110 * self.scale_factor)

        self.ENTRY_COMBO_HEIGHT = int(25 * self.scale_factor)

        self.SEARCH_BUTTON_WIDTH = int(90 * self.scale_factor)

        self.PROGRESS_WIDTH = int(150 * self.scale_factor)
        self.PROGRESS_HEIGHT = int(20 * self.scale_factor)

        self.TREE_TABLE_WIDTH = int(150 * self.scale_factor)

        self.IN_TB_ICON_WIDTH = int(17 * self.scale_factor)
        self.IN_TB_ICON_HEIGHT = int(17 * self.scale_factor)

        self.TOP_TB_ICON_WIDTH = int(30 * self.scale_factor)
        self.TOP_TB_ICON_HEIGHT = int(30 * self.scale_factor)

