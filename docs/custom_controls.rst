Custom Controls
===============
If you plan on extending any of the built in controls (such as using :class:`Group<pyxbmct.addonwindow.Group>` to make
your own composite controls) then make sure you call both the __init__ and __new__ methods.

Controls can have callback methods defined that are called at various points in their lifecycle.
It is recommended that you read the docstrings of and inherit from the ControlsWith<callback name> classes if you want
to use them.

_connectCallback
----------------
:class:`ControlWithConnectCallback<pyxbmct.addoncontrols.ControlWithConnectCallback>` - Called just before an event is connected to a control.

_placedCallback
---------------
:class:`ControlWithPlacedCallback<pyxbmct.addoncontrols.ControlWithPlacedCallback>` - Called after the control has been placed in a Window or Group.

_removedCallback
----------------
:class:`ControlWithRemovedCallback<pyxbmct.addoncontrols.ControlWithRemovedCallback>` - Called just before a control is removed from the window.

_focusedCallback
----------------
:class:`ControlWithFocusedCallback<pyxbmct.addoncontrols.ControlWithFocusedCallback>` - Called when a control is focused on.
