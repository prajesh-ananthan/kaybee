import pytest

from kaybee.plugins.widgets.directive import WidgetDirective


class Dummy:
    pass


@pytest.fixture()
def dummy_props():
    class DummyProps:
        template = 'foo'
        label = 'somelabel'

    yield DummyProps


@pytest.fixture()
def dummy_widget_class(dummy_props):
    class DummyWidget:

        def __init__(self, docname, rtype, content):
            self.docname = docname
            self.rtype = rtype
            self.content = content
            self.props = dummy_props()

    yield DummyWidget


@pytest.fixture()
def dummy_directive_class():
    class DummyDirective(WidgetDirective):
        name = 'dummy_directive'

    yield DummyDirective


@pytest.fixture()
def dummy_directive(dummy_directive_class):
    bd = dummy_directive_class(
        dummy_directive_class.name, [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.docname = 'somedoc'
    bd.state.document.settings.env.app = Dummy()
    bd.state.document.settings.env.app.widgets = dict()

    yield bd