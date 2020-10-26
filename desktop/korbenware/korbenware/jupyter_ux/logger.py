import ipywidgets as widgets

from korbenware.logger import PandasObserver, publisher

local_observer = PandasObserver()

publisher.addObserver(local_observer)
