import pytest
from kaybee.plugins.references.container import ReferencesContainer


@pytest.fixture()
def sample_container():
    rc = ReferencesContainer()
    yield rc


class TestReferencesContainer:
    def test_import(self):
        assert 'ReferencesContainer' == ReferencesContainer.__name__

    def test_construction(self, sample_container):
        assert 0 == len(sample_container)

    def test_missing_reftype(self, sample_container: ReferencesContainer):
        with pytest.raises(KeyError):
            sample_container['article']['flask'] = dict(flag=9)

    def test_existing_reftype(self, sample_container: ReferencesContainer):
        sample_container['article'] = dict()
        sample_container['article']['flask'] = dict(flag=9)

    def test_add_reference(self, sample_container: ReferencesContainer):
        sample_container['category'] = dict()
        sample_container.add_reference('category', 'category1', 999)
        result = sample_container['category']['category1']
        assert 999 == result

    def test_get_reference(self, sample_container: ReferencesContainer):
        sample_container['category'] = dict()
        sample_container.add_reference('category', 'category1', 999)
        result = sample_container.get_reference('category', 'category1')
        assert 999 == result

    def test_resource_references(self, references_sphinx_app,
                                 dummy_article, dummy_category):
        references = references_sphinx_app.references
        results = references.resource_references(dummy_article)
        assert dummy_category == results['category'][0]