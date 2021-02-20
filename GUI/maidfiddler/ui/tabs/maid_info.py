from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QLabel, QCheckBox
from .ui_tab import UiTab
from maidfiddler.ui.qt_elements import TextElement, ComboElement, NumberElement, PlainTextElement, CheckboxElement
from maidfiddler.util.translation import tr, tr_str
from maidfiddler.util.logger import logger

class MaidInfoTab(UiTab):
    maid_prop_changed_signal = pyqtSignal(dict)

    def __init__(self, ui):
        UiTab.__init__(self, ui)
        self.personality_names = []
        self.contracts_names = []
        self.relations_names = []
        self.feeling_names = []
        self.additional_relations_names = []
        self.special_relation_names = []
        self.seikeiken_names = []
        self.job_classes_names = []
        self.yotogi_classes_names = []

        self.properties = {
            "firstName": TextElement(self.ui.first_name_edit),
            "lastName": TextElement(self.ui.last_name_edit),
            "personal": ComboElement(self.ui.personality_combo),
            "contract": ComboElement(self.ui.contract_combo),
            "relation": ComboElement(self.ui.relation_combo),
            "feeling": ComboElement(self.ui.feeling_combo),
            "additionalRelation": ComboElement(self.ui.additional_relation_combo),
            "specialRelation": ComboElement(self.ui.special_relation_combo),
            "seikeiken": ComboElement(self.ui.current_combo),
            "initSeikeiken": ComboElement(self.ui.initial_combo),
            "current_job_class_id": ComboElement(self.ui.job_class_combo),
            "current_yotogi_class_id": ComboElement(self.ui.yotogi_class_combo),
            "employmentDay": NumberElement(self.ui.employment_day_box),
            "profileComment": PlainTextElement(self.ui.maid_description_edit),
            "freeComment": PlainTextElement(self.ui.user_comment_text),
            "age": NumberElement(self.ui.age_box),

            "isFirstNameCall": CheckboxElement(self.ui.isFirstNameCallCheck, False),
            "leader": CheckboxElement(self.ui.leaderCheck, False),
            "mainChara": CheckboxElement(self.ui.mainCharaCheck, False),
            "nightCommu": CheckboxElement(self.ui.nightCommuCheck, False),
            "noonCommu": CheckboxElement(self.ui.noonCommuCheck, False)
        }

    def update_ui(self):
        personalities = self.properties["personal"].index_map()
        contracts = self.properties["contract"].index_map()
        relations = self.properties["relation"].index_map()
        feelings = self.properties["feeling"].index_map()
        additional_relations = self.properties["additionalRelation"].index_map()
        special_relation = self.properties["specialRelation"].index_map()
        cur_seikeiken = self.properties["seikeiken"].index_map()
        init_seikeiken = self.properties["initSeikeiken"].index_map()
        job_classes = self.properties["current_job_class_id"].index_map()
        yotogi_classes = self.properties["current_yotogi_class_id"].index_map()

        personalities.clear()
        contracts.clear()
        relations.clear()
        feelings.clear()
        additional_relations.clear()
        special_relation.clear()
        cur_seikeiken.clear()
        init_seikeiken.clear()
        job_classes.clear()
        yotogi_classes.clear()

        self.personality_names.clear()
        self.contracts_names.clear()
        self.relations_names.clear()
        self.feeling_names.clear()
        self.additional_relations_names.clear()
        self.special_relation_names.clear()
        self.seikeiken_names.clear()
        self.job_classes_names.clear()
        self.yotogi_classes_names.clear()

        self.ui.personality_combo.blockSignals(True)
        self.ui.contract_combo.blockSignals(True)
        self.ui.relation_combo.blockSignals(True)
        self.ui.feeling_combo.blockSignals(True)
        self.ui.additional_relation_combo.blockSignals(True)
        self.ui.special_relation_combo.blockSignals(True)
        self.ui.current_combo.blockSignals(True)
        self.ui.initial_combo.blockSignals(True)
        self.ui.job_class_combo.blockSignals(True)
        self.ui.yotogi_class_combo.blockSignals(True)

        self.ui.personality_combo.clear()
        self.ui.contract_combo.clear()
        self.ui.relation_combo.clear()
        self.ui.additional_relation_combo.clear()
        self.ui.special_relation_combo.clear()
        self.ui.current_combo.clear()
        self.ui.initial_combo.clear()
        self.ui.job_class_combo.clear()
        self.ui.yotogi_class_combo.clear()

        for i, personal in enumerate(self._game_data["personal_list"]):
            self.ui.personality_combo.addItem(personal["name"], personal["id"])
            personalities[personal["id"]] = i
            self.personality_names.append(f"personality.{personal['name']}")

        for i, contract_name in enumerate(self._game_data["contract"]):
            contract_id = self._game_data["contract"][contract_name]
            self.ui.contract_combo.addItem(contract_name, contract_id)
            contracts[contract_id] = i
            self.contracts_names.append(f"contracts.{contract_name}")

        for i, relation_name in enumerate(self._game_data["relation"]):
            relation_id = self._game_data["relation"][relation_name]
            self.ui.relation_combo.addItem(relation_name, relation_id)
            relations[relation_id] = i
            self.relations_names.append(f"relations.{relation_name}")

        for i, feeling_name in enumerate(self._game_data["feeling"]):
            feeling_id = self._game_data["feeling"][feeling_name]
            self.ui.feeling_combo.addItem(feeling_name, feeling_id)
            feelings[feeling_id] = i
            self.feeling_names.append(f"feeling.{feeling_name}")

        for i, relation_name in enumerate(self._game_data["additional_relation"]):
            relation_id = self._game_data["additional_relation"][relation_name]
            self.ui.additional_relation_combo.addItem(relation_name, relation_id)
            additional_relations[relation_id] = i
            self.additional_relations_names.append(f"additional_relations.{relation_name}")

        for i, relation_name in enumerate(self._game_data["special_relation"]):
            logger.info("relation_name:"+relation_name)
            relation_id = self._game_data["special_relation"][relation_name]
            logger.info("relation_id:"+str(relation_id))
            self.ui.special_relation_combo.addItem(relation_name, relation_id)
            special_relation[relation_id] = i
            self.special_relation_names.append(f"special_relation.{relation_name}")

        for i, seik_name in enumerate(self._game_data["seikeiken"]):
            seik_id = self._game_data["seikeiken"][seik_name]
            self.ui.current_combo.addItem(seik_name, seik_id)
            self.ui.initial_combo.addItem(seik_name, seik_id)
            cur_seikeiken[seik_id] = i
            init_seikeiken[seik_id] = i
            self.seikeiken_names.append(f"seikeiken.{seik_name}")

        for i, job_class in enumerate(self._game_data["job_class_list"]):
            self.ui.job_class_combo.addItem(job_class["name"], job_class["id"])
            job_classes[job_class["id"]] = i
            self.job_classes_names.append(f"job_class.{job_class['name']}")

        for i, yotogi_class in enumerate(self._game_data["yotogi_class_list"]):
            self.ui.yotogi_class_combo.addItem(
                yotogi_class["name"], yotogi_class["id"])
            yotogi_classes[yotogi_class["id"]] = i
            self.yotogi_classes_names.append(
                f"yotogi_class.{yotogi_class['name']}")

        self.ui.yotogi_class_combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.ui.personality_combo.blockSignals(False)
        self.ui.contract_combo.blockSignals(False)
        self.ui.relation_combo.blockSignals(False)
        self.ui.feeling_combo.blockSignals(False)
        self.ui.additional_relation_combo.blockSignals(False)
        self.ui.special_relation_combo.blockSignals(False)
        self.ui.current_combo.blockSignals(False)
        self.ui.initial_combo.blockSignals(False)
        self.ui.job_class_combo.blockSignals(False)
        self.ui.yotogi_class_combo.blockSignals(False)

    def init_events(self, event_poller):
        self.ui.first_name_edit.editingFinished.connect(
            self.commit_prop_changes("firstName"))
        self.ui.last_name_edit.editingFinished.connect(
            self.commit_prop_changes("lastName"))
        self.ui.relation_combo.currentIndexChanged.connect(
            self.commit_prop_changes("relation"))
        self.ui.feeling_combo.currentIndexChanged.connect(
            self.commit_prop_changes("feeling"))
        self.ui.additional_relation_combo.currentIndexChanged.connect(
            self.commit_prop_changes("additionalRelation"))
        self.ui.special_relation_combo.currentIndexChanged.connect(
            self.commit_prop_changes("specialRelation"))
        self.ui.employment_day_box.valueChanged.connect(
            self.commit_prop_changes("employmentDay"))
        self.ui.age_box.valueChanged.connect(
            self.commit_prop_changes("age"))
        
        self.ui.isFirstNameCallCheck.stateChanged.connect(
            self.commit_prop_changes("isFirstNameCall"))
        self.ui.leaderCheck.stateChanged.connect(
            self.commit_prop_changes("leader"))
        self.ui.mainCharaCheck.stateChanged.connect(
            self.commit_prop_changes("mainChara"))
        self.ui.nightCommuCheck.stateChanged.connect(
            self.commit_prop_changes("nightCommu"))
        self.ui.nightCommuCheck.stateChanged.connect(
            self.commit_prop_changes("nightCommu"))

        self.ui.personality_combo.currentIndexChanged.connect(
            lambda: self.core.SetPersonalActive(self.properties["personal"].value()))
        self.ui.contract_combo.currentIndexChanged.connect(
            lambda: self.core.SetContractActive(self.properties["contract"].value()))
        self.ui.current_combo.currentIndexChanged.connect(
            lambda: self.core.SetCurSeikeikenActive(self.properties["seikeiken"].value()))
        self.ui.initial_combo.currentIndexChanged.connect(
            lambda: self.core.SetInitSeikeikenActive(self.properties["initSeikeiken"].value()))
        self.ui.job_class_combo.currentIndexChanged.connect(
            lambda: self.core.SetCurrentJobClassActive(self.properties["current_job_class_id"].value()))
        self.ui.yotogi_class_combo.currentIndexChanged.connect(
            lambda: self.core.SetCurrentYotogiClassActive(self.properties["current_yotogi_class_id"].value()))

        self.maid_prop_changed_signal.connect(self.prop_changed)
        event_poller.on("maid_prop_changed", self.maid_prop_changed_signal)

    def commit_prop_changes(self, prop):
        def handler():
            self.core.SetMaidPropertyActive(
                prop, self.properties[prop].value())
        return handler

    def prop_changed(self, args):
        if args["property_name"] not in self.properties:
            return

        if args["property_name"] == "mainChara":
            self.ui.personality_combo.setEnabled(not args["value"])
        
        self.properties[args["property_name"]].set_value(args["value"])

    def on_maid_selected(self):
        if self.maid_mgr.selected_maid is None:
            return

        #Dictionary<string, object>
        maid = self.maid_mgr.selected_maid

        self.ui.personality_combo.setEnabled(not maid["properties"]["mainChara"])

        # 디버깅용
        for name, element in maid["properties"].items():
            logger.debug(f"maid.items: {name} , {element}")
            
        for name, element in self.properties.items():
            logger.debug(f"properties.items: {name} , {element}")

        for name, element in self.properties.items():
            element.set_value(maid["properties"][name])

    def translate_ui(self):
        self.ui.ui_tabs.setTabText(0, tr(self.ui.tab_maid_info))

        for group in self.ui.tab_maid_info.findChildren(QGroupBox):
            group.setTitle(tr(group))

        for label in self.ui.tab_maid_info.findChildren(QLabel):
            label.setText(tr(label))

        for label in self.ui.checks_group.findChildren(QCheckBox):
            label.setText(tr(label))

        for i, personality in enumerate(self.personality_names):
            self.ui.personality_combo.setItemText(i, tr_str(personality))

        for i, contract in enumerate(self.contracts_names):
            self.ui.contract_combo.setItemText(i, tr_str(contract))

        for i, relation in enumerate(self.relations_names):
            self.ui.relation_combo.setItemText(i, tr_str(relation))

        for i, feeling in enumerate(self.feeling_names):
            self.ui.feeling_combo.setItemText(i, tr_str(feeling))

        for i, relation in enumerate(self.additional_relations_names):
            self.ui.additional_relation_combo.setItemText(i, tr_str(relation))

        for i, relation in enumerate(self.special_relation_names):
            self.ui.special_relation_combo.setItemText(i, tr_str(relation))

        for i, seikeiken in enumerate(self.seikeiken_names):
            self.ui.current_combo.setItemText(i, tr_str(seikeiken))
            self.ui.initial_combo.setItemText(i, tr_str(seikeiken))

        for i, job_class in enumerate(self.job_classes_names):
            self.ui.job_class_combo.setItemText(i, tr_str(job_class))

        for i, yotogi_class in enumerate(self.yotogi_classes_names):
            self.ui.yotogi_class_combo.setItemText(i, tr_str(yotogi_class))
