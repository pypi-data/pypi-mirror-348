import os

from setuptools import find_packages, setup


def read(fname):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...

    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def build_media_pattern(base_folder, file_extension):
    return ["%s/%s*.%s" % (base_folder, "*/"*x, file_extension) for x in range(10)]


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


template_patterns = (
    build_media_pattern("templates", "html") +
    build_media_pattern("static", "js") +
    build_media_pattern("static", "css") +
    build_media_pattern("static", "png") +
    build_media_pattern("static", "jpeg") +
    build_media_pattern("static", "gif")
)

packages = find_packages()

package_data = {
    package_name: template_patterns
    for package_name in packages
}

setup(
    name="openedx-django-wiki",
    version="3.1.1",
    author="Benjamin Bach",
    author_email="benjamin@overtag.dk",
    long_description_content_type='text/markdown',
    description="A wiki system written for the Django framework.",
    url="https://github.com/openedx/django-wiki",
    license="GPLv3",
    keywords="django wiki markdown",
    packages=find_packages(exclude=["testproject", "testproject.*"]),
    long_description=read('README.md'),
    zip_safe=False,
    install_requires=load_requirements('requirements/base.in'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
    package_data=package_data,
)
