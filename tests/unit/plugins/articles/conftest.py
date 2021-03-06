from datetime import datetime

import dectate
import pytest

from kaybee.plugins.articles.actions import ToctreeAction
from kaybee.plugins.articles.base_article import BaseArticle
from kaybee.plugins.articles.base_article_reference import BaseArticleReference
from kaybee.plugins.articles.base_homepage import BaseHomepage
from kaybee.plugins.articles.base_section import BaseSection
from kaybee.plugins.articles.base_toctree import BaseToctree
from kaybee.utils.rst import rst_document


@pytest.fixture()
def articles_kb_app():
    class articles_kb_app(dectate.App):
        toctree = dectate.directive(ToctreeAction)

    yield articles_kb_app


@pytest.fixture()
def article_resources():
    f1_content = """
    template: f1_section_template
    featured_resource: f1/f2/about
    acquireds:
        article:
            template: acquired_article
            style: acquired_style
        section:
            template: f1template
        all:
            flag: 9933
        """
    f4_content = """
    acquireds:
        all:
    """
    f1_about_yaml = """
published: 2015-04-25 12:01
references:
    category: [c1,]
    """
    index = BaseHomepage('index', 'homepage', 'logo: somelogo.png')
    index.title = 'Index'
    about = BaseArticle('about', 'article', '')
    about.title = 'About'
    f1 = BaseSection('f1/index', 'section', f1_content)
    f1.title = 'F1'
    f1_about = BaseArticle('f1/about', 'article', f1_about_yaml)
    f1_about.title = 'F1 About'
    f2 = BaseSection('f1/f2/index', 'section', '')
    f2.title = 'F2 Index'
    f2_about = BaseArticle('f1/f2/about', 'article', '')
    f2_about.title = 'F2 About'
    f3 = BaseArticle('f1/f2/f3/index', 'article', 'template: f3template')
    f3.title = 'F3'
    f3.props.is_series = True
    f3_about = BaseArticle('f1/f2/f3/about', 'article', '')
    f3_about.title = 'F3 About'
    f4 = BaseArticle('f1/f2/f3/f4/index', 'article', f4_content)
    f4.title = 'F4'
    f4_about = BaseArticle('f1/f2/f3/f4/about', 'article', '')
    f4.title = 'F4 About'
    c1 = BaseArticleReference('category/c1', 'category', 'label: c1')
    c1.title = 'C1'

    yield {
        'index': index,
        'about': about,
        'f1/index': f1,
        'f1/about': f1_about,
        'f1/f2/index': f2,
        'f1/f2/about': f2_about,
        'f1/f2/f3/index': f3,
        'f1/f2/f3/about': f3_about,
        'f1/f2/f3/f4/index': f4,
        'f1/f2/f3/f4/about': f4_about,
        'category/c1': c1
    }


@pytest.fixture()
def article_references(article_resources):
    """ Make a sample implementation sphinx_env.references """
    references = dict(
        category=dict(
            c1=(article_resources['category/c1'])
        ),
        reference={}
    )
    yield references


@pytest.fixture()
def dummy_article(article_resources):
    yield article_resources['f1/f2/f3/about']


@pytest.fixture()
def dummy_image_article(article_resources):
    yaml_content = """
    images:
        - usage: icon_24
          filename: paul_headshotx24.jpeg
        - usage: icon_128
          filename: paul_headshotx128.jpeg    
    """
    article = BaseArticle('image_article', 'article', yaml_content)
    yield article


@pytest.fixture()
def dummy_section(article_resources):
    yield article_resources['f1/f2/f3/index']


@pytest.fixture()
def dummy_homepage(article_resources):
    yield article_resources['index']


@pytest.fixture()
def dummy_nodes(dummy_entries):
    class Node:
        def __init__(self):
            self.attributes = dict(
                hidden=False,
                entries=dummy_entries,
            )

        def replace_self(self, value):
            pass

    yield (Node(),)


@pytest.fixture()
def dummy_doctree(dummy_nodes):
    class Doctree:
        def __init__(self):
            self.dummy_nodes = dummy_nodes

        def traverse(self, *args):
            return self.dummy_nodes

    yield Doctree()


@pytest.fixture()
def dummy_toctree():
    yield BaseToctree('some/path/to/about')


@pytest.fixture()
def dummy_entries():
    r = [
        ('x', 'f1/about')
    ]

    yield r


@pytest.fixture()
def dummy_titles():
    class Title:
        def __init__(self, first_child):
            self.children = [first_child]

    yield {
        'about': Title('About'),
        'f1/about': Title('F1 About')
    }


@pytest.fixture()
def article_env(dummy_titles):
    class Env:
        def __init__(self):
            self.titles = dummy_titles
            self.resources = dict()

    yield Env()


@pytest.fixture()
def excerpt():
    source = """
Test
====

First *paragraph*.

Second *paragraph*.        
            """
    yield rst_document(source)


@pytest.fixture()
def noexcerpt():
    source = """
Test
====
            """
    yield rst_document(source)


@pytest.fixture()
def past_datetime() -> datetime:
    past = datetime(2012, 4, 25, 13, 26)
    yield past
