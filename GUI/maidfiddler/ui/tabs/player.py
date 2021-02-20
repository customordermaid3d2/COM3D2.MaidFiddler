from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal
from .ui_tab import UiTab
from maidfiddler.ui.qt_elements import NumberElement, TextElement, CheckboxElement, MIN_MAX_DICT, FLOAT_TYPES
from maidfiddler.util.translation import tr, tr_str
from maidfiddler.util.logger import logger

class PlayerTab(UiTab):
    update_player_props_signal = pyqtSignal(dict)
    on_player_prop_change_signal = pyqtSignal(dict)

    def __init__(self, ui):
        UiTab.__init__(self, ui)

        self.properties = {}

    def create_line(self, t):
        if t in MIN_MAX_DICT:
            s = QDoubleSpinBox()
            s.setDecimals(0)
            return NumberElement(s, type=t)
        if t in FLOAT_TYPES:
            return NumberElement(QDoubleSpinBox())
        if t == "System.Boolean":
            return CheckboxElement(QCheckBox())
        return TextElement(QLineEdit())

    def update_ui(self):
        self.properties.clear()
        self.ui.player_params_table.clearContents()

        self.ui.player_params_table.setRowCount(
            len(self.game_data["player_status_settable"]))

        player_params_header = self.ui.player_params_table.horizontalHeader()

        player_params_header.setSectionResizeMode(0, QHeaderView.Stretch)
        player_params_header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)
        player_params_header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)

        for i, prop in enumerate(self.game_data["player_status_settable"]):
            prop_type = self.game_data["player_status_settable"][prop]
            name = QTableWidgetItem(prop)
            name.setWhatsThis(f"player_props.{prop}")
            line = self.create_line(prop_type)
            line.qt_element.setProperty("prop_name", prop)

            if prop_type != "System.Boolean":
                line.qt_element.setStyleSheet("width: 15em;")
            else:
                line.checkbox.setProperty("prop_name", prop)

            checkbox = QCheckBox()
            widget = QWidget()
            hbox = QHBoxLayout(widget)
            hbox.addWidget(checkbox)
            hbox.setAlignment(Qt.AlignCenter)
            hbox.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(hbox)

            checkbox.setProperty("prop_name", prop)

            self.ui.player_params_table.setItem(i, 0, name)
            self.ui.player_params_table.setCellWidget(i, 1, line.qt_element)
            self.ui.player_params_table.setCellWidget(i, 2, widget)

            self.properties[prop] = (line, checkbox)

            line.connect(self.commit_prop)
            checkbox.stateChanged.connect(self.commit_lock)

    def init_events(self, event_poller):
        self.update_player_props_signal.connect(self.update_player_props)
        self.on_player_prop_change_signal.connect(self.on_player_prop_change)
        event_poller.on("deserialize_done", self.update_player_props_signal)
        event_poller.on("player_prop_changed", self.on_player_prop_change_signal)

    def commit_prop(self):
        sender = self.sender()
        prop = sender.property("prop_name")
        el = self.properties[prop][0]
        try:
            self.core.SetPlayerData(prop, el.value())
        except Exception as e:
            logger.error(f"Failed to set player data: {e}")

    def commit_lock(self):
        sender = self.sender()
        self.core.TogglePlayerStatusLock(sender.property(
            "prop_name"), sender.checkState() == Qt.Checked)

    def on_player_prop_change(self, args):
        self.properties[args["prop_name"]][0].set_value(args["value"])

    def update_player_props(self, args):
        if not args["success"]:
            return
        self.reload_player_props()

    def reload_player_props(self):
        data = self.core.GetAllPlayerData()

        locked_vals = set(data["locked_props"])

        for prop, value in data["props"].items():
            logger.debug(f"data.items: {prop} , {value}")
            (el, cb) = self.properties[prop]
            el.set_value(value)

            cb.blockSignals(True)
            cb.setCheckState(
                Qt.Checked if prop in locked_vals else Qt.Unchecked)
            cb.blockSignals(False)

    def translate_ui(self):
        self.ui.ui_tabs.setTabText(5, tr(self.ui.tab_player_info))

        for group in self.ui.tab_player_info.findChildren(QGroupBox):
            group.setTitle(tr(group))

        for row in range(0, self.ui.player_params_table.rowCount()):
            name = self.ui.player_params_table.item(row, 0)
            name.setText(tr(name))

        for col in range(0, self.ui.player_params_table.columnCount()):
            name = self.ui.player_params_table.horizontalHeaderItem(col)
            name.setText(tr(name))
