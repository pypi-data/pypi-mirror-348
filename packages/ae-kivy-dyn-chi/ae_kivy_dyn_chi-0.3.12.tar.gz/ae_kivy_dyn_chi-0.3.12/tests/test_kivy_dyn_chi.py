""" test ae.kivy_dyn_chi portion. """
from conftest import skip_gitlab_ci
from unittest.mock import MagicMock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

# noinspection PyProtectedMember
from ae.kivy_dyn_chi import _child_data_dict, DynamicChildrenBehavior


class DynBoxTest(DynamicChildrenBehavior, BoxLayout):
    """ test class with BoxLayout """
    def get_super(self):
        """ test super() """
        return super()


class DynDropTest(DynamicChildrenBehavior, DropDown):
    """ test class with DropDown """
    def get_super(self):
        """ test super() """
        return super()


class DynPopTest(DynamicChildrenBehavior, Popup):
    """ test class with Popup """
    def get_super(self):
        """ test super() """
        return super()


def test_declaration():
    """ test if class exists """
    assert DynamicChildrenBehavior


class TestHelpers:
    def test_child_data_dict_empty_args(self):
        assert _child_data_dict({}, '', '', {}) == {}
        assert _child_data_dict({'kwargs': {}, 'attributes': {}}, 'FlowButton', 'kwargs',
                                {'': {'kwargs': {}, 'attributes': {}}}) == {}

    def test_child_data_dict_empty_data_children_value(self):
        assert _child_data_dict({}, 'FlowButton', 'kwargs',
                                {'': {'kwargs': {'prop': 'chi_default'}}}) == {'prop': 'chi_default'}

    def test_child_data_dict_empty_data_class_value(self):
        assert _child_data_dict({}, 'FlowButton', 'kwargs',
                                {'': {'kwargs': {'prop': 'chi_default'}},
                                 'FlowButton': {'kwargs': {'prop': 'cls_default'}}}) == {'prop': 'cls_default'}

    def test_child_data_dict_child_value_override_children_value(self):
        assert _child_data_dict({'kwargs': {'prop': 'chi_value'}}, 'FlowButton', 'kwargs',
                                {'': {'kwargs': {'prop': 'chi_default'}}}) == {'prop': 'chi_value'}

    def test_child_data_dict_class_value_override_children_and_class_value(self):
        assert _child_data_dict({'kwargs': {'prop': 'chi_value'}}, 'FlowButton', 'kwargs',
                                {'': {'kwargs': {'prop': 'chi_default'}},
                                 'FlowButton': {'kwargs': {'prop': 'cls_default'}}}) == {'prop': 'chi_value'}

    def test_child_data_dict_(self):
        assert _child_data_dict({'kwargs': {'prop': 'chi_value'}}, 'FlowButton', 'kwargs',
                                {'': {'kwargs': {'prop': 'chi_default'}},
                                 'FlowButton': {'kwargs': {'prop': 'cls_default'}}}) == {'prop': 'chi_value'}


@skip_gitlab_ci
class TestContainerProperty:
    def test_init_box(self):
        con = DynBoxTest()
        s = con.get_super()
        print(s)
        print("DynBox:  self has container", hasattr(con, 'container'))
        print("DynBox: super has container", hasattr(s, 'container'))

    def test_init_drop(self):
        con = DynDropTest()
        s = con.get_super()
        print(s)
        print("DynDrop:  self has container", hasattr(con, 'container'))
        print("DynDrop: super has container", hasattr(s, 'container'))

    def test_init_pop(self):
        con = DynPopTest()
        s = con.get_super()
        print(s)
        print("DynPop:  self has container", hasattr(con, 'container'))
        print("DynPop: super has container", hasattr(s, 'container'))


@skip_gitlab_ci
class TestRefresh:
    def test_mocked_refresh(self):
        con = DynBoxTest()
        con.child_data_maps = [dict(cls=Widget, attributes=dict(test_attr='tst_att_val')),
                               dict(cls='Widget')]

        con.refresh_child_data_widgets()

        assert con._map_children
        assert con.container.children

        child = con._map_children[0]
        assert child in con.container.children
        assert child.child_index == 0
        assert child.test_attr == 'tst_att_val'

    def test_remove_children(self):
        con = DynBoxTest()
        con._map_children = [MagicMock()]
        con.refresh_child_data_widgets()
        assert not con._map_children
