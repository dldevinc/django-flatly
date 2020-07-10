import pytest
from django.template.exceptions import TemplateDoesNotExist
from flatly.helpers import get_template_by_name


class TestTemplates:
    def test_index(self):
        template = get_template_by_name('')
        assert template.origin.name.endswith('tests/templates/index.html')

    def test_index_by_name(self):
        # unique template in /templates/ folder
        template = get_template_by_name('index')
        assert template.origin.name.endswith('tests/templates/index.html')

    def test_app_template(self):
        # unique template in application folder
        template = get_template_by_name('app/index')
        assert template.origin.name.endswith('tests/app/templates/app/index.html')

    def test_default_loaders_priority(self):
        # template in /templates/ overrides an application template with the same name
        template = get_template_by_name('app/section')
        assert template.origin.name.endswith('tests/templates/app/section.html')

    def test_subfolder_index(self):
        # "index.html" template in subfolder
        template = get_template_by_name('about')
        assert template.origin.name.endswith('tests/templates/about/index.html')

    def test_subfolder_template(self):
        # custom template in subfolder
        template = get_template_by_name('about/staff')
        assert template.origin.name.endswith('tests/templates/about/staff.html')

    def test_priority(self):
        # "page.html" have higher priority than "page/index.html"
        template = get_template_by_name('blog')
        assert template.origin.name.endswith('tests/templates/blog.html')

    def test_missing_templates(self):
        with pytest.raises(TemplateDoesNotExist):
            get_template_by_name('about/contact')
