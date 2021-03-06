import pytest

pytestmark = pytest.mark.sphinx('html', testroot='articles')


def get_strings(page, class_):
    return [
        i.string
        for i in page.find_all(class_=class_)
    ]


@pytest.mark.parametrize('page', ['articles/article1.html', ], indirect=True)
class TestArticles1:

    def test_article1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Article 1' == h1

        # Author listing
        authors = page.find(id='kb-author-listing').find_all('li')
        assert 2 == len(authors)
        author1 = authors[0].find('a').contents[0].strip()
        assert 'Author 1' == author1

        # Categories listing
        categories = page.find(id='kb-category-listing').find_all('li')
        assert 2 == len(categories)
        category1 = categories[0].find('a').contents[0].strip()
        assert 'Category 2' == category1


@pytest.mark.parametrize('page', ['authors/author1.html', ],
                         indirect=True)
class TestAuthor1:

    def test_author1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Author 1' == h1

        items = [i.contents[0].strip()
                 for i in page.find_all(class_='kb-reference-item')]
        assert 2 == len(items)
        assert 'Article 1' in items

        # Headshot
        img = page.find(class_='kb-author-headshot')
        src = img.attrs['src']
        assert 'paul_headshotx128.jpeg' == src

@pytest.mark.parametrize('page', ['categories/category2.html', ],
                         indirect=True)
class TestCategories2:

    def test_article2(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Category 2' == h1

        items = [i.contents[0].strip()
                 for i in page.find_all(class_='kb-reference-item')]
        assert 2 == len(items)
        assert 'Article 1' in items


@pytest.mark.parametrize('page', ['navpage1.html', ],
                         indirect=True)
class TestNavpage1:

    def test_navpage1(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Navpage 1' == h1

        # Get the first level menu entries
        docnames = get_strings(page, 'kb-menuentry-docname')
        labels = get_strings(page, 'kb-menuentry-label')
        subheadings = get_strings(page, 'kb-menuentry-subheading')
        accents = get_strings(page, 'kb-menuentry-accent')
        icons = get_strings(page, 'kb-menuentry-icon')

        # docnames
        assert 3 == len(docnames)
        assert 'articles/index' == docnames[0]

        # You can specify a label in the navpage entry, if not, the resource
        # title will be used.
        assert 3 == len(labels)
        assert 'Articles' == labels[0]
        assert 'Authors' == labels[1]
        assert 'Categories With Label' == labels[2]

        # Subheadings can come from the entry or the resource subheading
        assert 3 == len(subheadings)
        assert 'This subheading from articles resource' == subheadings[0]
        assert 'Do not use authors subheading' == subheadings[1]
        assert None is subheadings[2]

        # Accent and icons
        assert 3 == len(accents)
        assert 3 == len(icons)
        assert 'info' == accents[0]
        assert 'primary' == accents[1]
        assert 'fas booboo' == icons[0]
        assert 'fas fa-eye' == icons[1]

        # Now results
        result_docnames = get_strings(page, 'kb-menuresult-docname')
        result_authors = get_strings(page, 'kb-menuresult-author')

        # Result docnames
        assert 4 == len(result_docnames)
        assert 4 == len(result_authors)

@pytest.mark.parametrize('page', ['articles/article2.html', ],
                         indirect=True)
class TestQuerylist:

    def test_querylist(self, page):
        h1 = page.find('h1').contents[0].strip()
        assert 'Article 2' == h1

        labels = [
            result.contents[0].strip()
            for result in page.find_all(class_='kb-querylist-label')]
        items = [
            result.contents[0].strip()
            for result in page.find_all(class_='kb-querylist-item')]
        assert 2 == len(labels)
        assert 'Recent Blog Posts' in labels
        assert 8 == len(items)
        assert 'Section 1' in items


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticles1Debug:

    def test_settings(self, json_page):
        resources = json_page['resources']
        assert 'config' in resources

        # article/section/homepage is in the registered handlers
        resources_config = resources['config']
        assert 'article' in resources_config
        assert 'homepage' in resources_config
        assert 'section' in resources_config

        # Test some values
        resource_values = resources['values']

        # homepage
        homepage = resource_values['index']
        assert 'index' == homepage['docname']
        assert 'Hello World' == homepage['title']
        assert 'section' not in homepage
        assert 'articles/index' in homepage['toctree']
        assert None is homepage['series']

        # articles
        articles = resource_values['articles/index']
        assert 'articles/index' == articles['docname']
        assert 'Articles' == articles['title']
        assert 'section' not in homepage
        assert None is articles['series']

        # article1
        article1 = resource_values['articles/article1']
        assert 'articles/article1' == article1['docname']
        assert 'Article 1' == article1['title']
        assert 'articles/index' == article1['section']
        assert 'toctree' not in article1
        assert 3 == len(article1['series'])

        # section1
        section1 = resource_values['section1/index']
        assert 'section1/index' == section1['docname']
        assert 'Section 1' == section1['title']
        assert 'section' not in homepage
        assert ['section1/article2'] == section1['toctree']
        assert 'section1/article2' == section1['get_featured_resource']


@pytest.mark.parametrize('json_page', ['catalog.json', ], indirect=True)
class TestJsoncatalog:

    def test_testjsoncatalog(self, json_page):
        resources = json_page['resources']
        references = json_page['references']

        # Basic assertion
        assert 15 == len(resources.keys())
        assert 3 == len(references.keys())
