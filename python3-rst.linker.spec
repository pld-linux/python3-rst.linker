#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# pytest tests (not in sdist)

Summary:	rst.linker - Python 2 Sphinx plugin to add links to the changelog
Summary(pl.UTF-8):	rst.linker - wtyczka Sphinksa dla Pythona 2 do dodawania odnośników do changeloga
Name:		python3-rst.linker
Version:	2.6.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/rst-linker/
Source0:	https://files.pythonhosted.org/packages/source/r/rst.linker/rst_linker-%{version}.tar.gz
# Source0-md5:	a105bb425ce384dc744d252c32fb6433
URL:		https://github.com/jaraco/rst.linker
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:61.2
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-dateutil
BuildRequires:	python3-jaraco.context
BuildRequires:	python3-jaraco.vcs >= 2.1
BuildRequires:	python3-path >= 13.1.0
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-subprocess
# lint only?
#BuildRequires:	python3-pytest-black >= 0.3.7
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-enabler >= 2.2
#BuildRequires:	python3-pytest-mypy >= 0.9.1
#BuildRequires:	python3-pytest-ruff >= 0.2.1
#BuildRequires:	python3-types-python-dateutil
%endif
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
#BuildRequires:	python3-sphinx-lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-Sphinx
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rst.linker is a Sphinx plugin to add links to the changelog.

%description -l pl.UTF-8
rst.linker to wtyczka Sphinksa służąca do dodawania odnośników do
changeloga.

%package apidocs
Summary:	Documentation for rst.linker module
Summary(pl.UTF-8):	Dokumentacja do modułu rst.linker
Group:		Documentation

%description apidocs
Documentation for rst.linker module.

%description apidocs -l pl.UTF-8
Dokumentacja do modułu rst.linker.

%prep
%setup -q -n rst_linker-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black,pytest_flake8" \
%{__python3} -m pytest test_all.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%dir %{py3_sitescriptdir}/rst
%{py3_sitescriptdir}/rst/linker.py
%dir %{py3_sitescriptdir}/rst/__pycache__
%{py3_sitescriptdir}/rst/__pycache__/linker.cpython-*.py[co]
%{py3_sitescriptdir}/rst_linker-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
