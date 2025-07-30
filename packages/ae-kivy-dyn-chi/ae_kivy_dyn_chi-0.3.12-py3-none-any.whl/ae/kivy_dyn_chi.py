"""
dynamic children mix-in for kivy container widgets
==================================================

this ae portion is providing the mixin class :class:`DynamicChildrenBehavior` to add children widgets dynamically
and data-driven to your kivy popup widget (like DropDowns, Popups, Menus, Selectors).
"""
from collections import Counter
from typing import Any, Callable, Union

from kivy.factory import Factory                                                            # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import ListProperty                                                    # type: ignore # noqa: E0611
from kivy.uix.popup import Popup                                                            # type: ignore
from kivy.uix.widget import Widget                                                          # type: ignore

from ae.base import UNSET                                                                   # type: ignore
from ae.deep import deep_replace, deep_update, key_path_object                              # type: ignore


__version__ = '0.3.12'


AttrMapType = dict[str, Any]                    #: child attribute (value of the 'kwargs' and 'attributes' keys)
DataItemValueType = Union[str, AttrMapType]     #: item dict value (str for 'cls' key, dict for 'kwargs'/'attributes')
DataItemType = dict[str, DataItemValueType]     #: :attr:`DynamicChildrenBehavior.child_data_maps` item type
ChildrenDataType = list[DataItemType]           #: :attr:`DynamicChildrenBehavior.child_data_maps` type


def _child_data_dict(child_data: DataItemType, cls: str, key: str, defaults: dict[str, dict[str, AttrMapType]]
                     ) -> AttrMapType:
    """ determine child data dict values and put children default values for the keys not specified in child data. """
    val = defaults.get('', {}).get(key, {}).copy()          # copy the defaults for all classes
    deep_update(val, defaults.get(cls, {}).get(key, {}))    # merge/update with the defaults for the specified class
    deep_update(val, child_data.get(key, {}))               # finally overwrite defaults with child data
    return val


class DynamicChildrenBehavior:
    """ mixin class for the dynamic creation/refresh of child widgets from a data map.

    at least one of the classes that is mixing in this class has to inherit from Widget (or EventDispatcher) to get the
    :attr:`~DynamicChildrenBehavior.child_data_maps` attribute correctly initialized and firing on change.
    """
    child_data_defaults: ChildrenDataType = ListProperty()
    """ child data default values for all the children with the same `cls` key that are specified via the
    :attr:`ae.kivy_dyn_chi.DynamicChildrenBehavior.child_data_maps` property. if the `cls` key is missing or its
    item value is empty then the defaults in the other item values will be used for all children.

    :attr:`child_data_defaults` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    """

    child_data_maps: ChildrenDataType = ListProperty()
    """ list of child data dicts to instantiate the children of the inheriting layout/widget.

    each child data dict is defining its own widget with the following keys:

    * `cls`: either the class name or the class/type object of the widget to be created dynamically.
    * `kwargs`: dict of keyword arguments that will be passed to the constructor method of the widget.
      all values in this dict with the magic string `'replace_with_data_map_popup'` will be
      replaced with the instance of the container before it gets passed to the `__init__` method
      of the child (see :func:`~ae.deep.deep_replace`).
    * `attributes`: dict of attributes where the key is specifying the attribute name/path and the
      value the finally assigned attribute value.
      the attribute name (the key of this dict) can be a deep/combined attribute/index path
      which allows to update deeper objects within the child object (via :func:`~ae.deep.key_path_object`).
      all values in this dict with the magic string `'replace_with_data_map_popup'` will be
      replaced with the instance of the container before the child attributes get updated.
      all values in this dict with the magic string `'replace_with_data_map_child'` will be
      replaced with the instance of the child before they get applied to it (via :func:`~ae.deep.deep_replace`).

    :attr:`child_data_maps` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    """

    bind: Callable
    container: Widget
    _container: Widget

    def __init__(self, **kwargs):
        """ add dynamic creation and refresh of children to this layout (Popup/Dropdown/...) widget. """
        super().__init__(**kwargs)
        self._is_popup = isinstance(self, Popup)    # True if inherits from :class:`~kivy.uix.popup.Popup`
        self._map_children = []
        self.bind(child_data_defaults=self.refresh_child_data_widgets, child_data_maps=self.refresh_child_data_widgets)
        self.refresh_child_data_widgets(self, **kwargs)

    def refresh_child_data_widgets(self, *_args, **init_kwargs):
        """ recreate dynamic children of the passed widget.

        :param _args:           not needed extra args (only passed if this function get called as event handler).
        :param init_kwargs:     container kwargs (passed from :meth:`~DynamicChildrenBehavior.__init__` method).
        """
        def self_replace(_p, _k, v):
            return self if v == 'replace_with_data_map_popup' else UNSET

        def child_replace(_p, _k, v):
            return child if v == 'replace_with_data_map_child' else UNSET

        if self._is_popup:
            children_container = init_kwargs.get('content', self._container)   # self._container is self.ids.container
        else:
            children_container = init_kwargs.get('container', getattr(self, 'container', self))

        if not hasattr(super(), 'container'):
            self.container = children_container

        for chi in self._map_children:
            children_container.remove_widget(chi)
        self._map_children.clear()

        child_data_defaults = self.child_data_defaults
        assert not [_c for _c, cnt in Counter(_.get('cls', '') for _ in child_data_defaults).items() if cnt > 1], \
            "duplicate 'cls' entries in child_data_defaults are not allowed/supported"
        default_class = next((_.get('cls', '') for _ in child_data_defaults if _.get('cls', '')), 'FlowButton')
        class_defaults = {defaults.get('cls', ''): {key: attr for key, attr in defaults.items() if key != 'cls'}
                          for defaults in child_data_defaults}
        for child_index, child_data in enumerate(self.child_data_maps):
            cls = child_data.get('cls', default_class)
            if isinstance(cls, str):
                nam = cls
                cls = Factory.get(nam)
            else:
                nam = cls.__name__

            init_child_kwargs = _child_data_dict(child_data, nam, 'kwargs', class_defaults)
            deep_replace(init_child_kwargs, self_replace)
            child = cls(**init_child_kwargs)

            child.child_index = child_index

            attributes = _child_data_dict(child_data, nam, 'attributes', class_defaults)
            if attributes:
                deep_replace(attributes, self_replace)
                deep_replace(attributes, child_replace)
                for attr_name, attr_value in attributes.items():
                    # setattr(child, attr_name, attr_value) does not support composed/deep keys/attributes
                    key_path_object(child, attr_name, new_value=attr_value)

            bind_props = _child_data_dict(child_data, nam, 'binds', class_defaults)
            if bind_props:
                child.bind(**bind_props)

            children_container.add_widget(child)
            self._map_children.append(child)


Factory.register('DynamicChildrenBehavior', cls=DynamicChildrenBehavior)
