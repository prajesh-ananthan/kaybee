from datetime import datetime
from typing import List

from kaybee.plugins.references.model_types import ReferencesType
from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


class BaseArticleModel(BaseResourceModel):
    style: str = None
    css_class: str = None
    in_nav: bool = False
    weight: int = 0
    published: datetime = None
    category: ReferencesType = []
    tag: ReferencesType = []
    excerpt: str = None
    auto_excerpt: int = 1


class BaseArticle(BaseResource):
    model = BaseArticleModel
    excerpt: str = None  # Stamped on later by the handler
    toctree: List[str] = []  # Stamped on later by the handler

    def section(self, resources):
        """ Which section is this in, if any """

        section = [p for p in self.parents(resources) if p.rtype == 'section']
        if section:
            return section[0]
        return None

    def in_navitem(self, resources, nav_href):
        """ Given  href of nav item, determine if resource is in it """

        # The navhref might end with '/index' so remove it if so
        if nav_href.endswith('/index'):
            nav_href = nav_href[:-6]

        return self.docname.startswith(nav_href)

    def is_published(self):
        """ Return true if this resource has published date in the past """

        now = datetime.now()
        published = self.props.published
        if published:
            return published < now
        return False

    def series(self, resources):
        parent = resources.get(self.parent)
        if not parent:
            return None
        results = []
        for docname in parent.toctree:
            resource = resources.get(docname)
            if resource:
                # We might have a non-resource page in the toctree,
                # so skip it if true
                excerpt = getattr(resource, 'excerpt', False)
                results.append(
                    dict(
                        docname=docname,
                        title=resource.title,
                        excerpt=excerpt,
                        current=self.docname == docname
                    )
                )
        return results

    def __json__(self, resources):
        d = super().__json__(resources)
        d['excerpt'] = self.excerpt
        d['section'] = getattr(self.section(resources), 'docname', '')
        d['toctree'] = self.toctree
        try:
            d['series'] = self.series(resources)
        except AttributeError:
            d['series'] = []

        return d