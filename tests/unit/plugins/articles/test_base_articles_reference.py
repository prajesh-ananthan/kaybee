from kaybee.plugins.articles.base_article_reference import BaseArticleReference


class TestBaseArticleReference:
    def test_import(self):
        assert 'BaseArticleReference' == BaseArticleReference.__name__

    def test_construction(self):
        yaml = """
label: reference1
        """
        bar = BaseArticleReference('reference1', 'somereference', yaml)
        assert 'reference1' == bar.props.label

    def test_articles_resources(self, article_resources):
        c1 = article_resources['category/c1']
        assert 'c1' == c1.props.label

    def test_get_sources(self, article_resources):
        f1_about = article_resources['f1/about']
        c1 = article_resources['category/c1']
        targets = c1.get_sources(article_resources)
        assert 'f1/about' == targets[0].docname
