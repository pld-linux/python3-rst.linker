#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test tests

Summary:	rst.linker - Python 2 Sphinx plugin to add links to the changelog
Summary(pl.UTF-8):	rst.linker - wtyczka Sphinksa dla Pythona 2 do dodawania odnośników do changeloga
Name:		python3-rst.linker
Version:	2.3.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/rst.linker/
Source0:	https://files.pythonhosted.org/packages/source/r/rst.linker/rst.linker-%{version}.tar.gz
# Source0-md5:	10cd73d4200e7bbbdb621275ed15bffe
URL:		https://github.com/jaraco/rst.linker
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-dateutil
#BuildRequires:	python3-enabler >= 1.3
#BuildRequires:	python3-flake8 < 5
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
#BuildRequires:	python3-jaraco.test >= 3.2.0
BuildRequires:	python3-path >= 13.1.0
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-black >= 0.3.7
BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-enabler >= 1.0.1
BuildRequires:	python3-pytest-flake8
#BuildRequires:	python3-pytest-mypy >= 0.9.1
#BuildRequires:	python3-types-python-dateutil
%endif
%if %{with doc}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-jaraco.packaging >= 9
# needs to be already installed
BuildRequires:	python3-rst.linker >= 1.9
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-Sphinx
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
%setup -q -n rst.linker-%{version}

cat >setup.py <<EOF
from setuptools import setup
setup()
EOF

%build
%py3_build %{?with_doc:build_sphinx}

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black,pytest_flake8" \
%{__python3} -m pytest test_all.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%dir %{py3_sitescriptdir}/rst
%{py3_sitescriptdir}/rst/__init__.py
%{py3_sitescriptdir}/rst/linker.py
%dir %{py3_sitescriptdir}/rst/__pycache__
%{py3_sitescriptdir}/rst/__pycache__/__init__.cpython-*.py[co]
%{py3_sitescriptdir}/rst/__pycache__/linker.cpython-*.py[co]
%{py3_sitescriptdir}/rst.linker-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build-3/sphinx/html/{_static,*.html,*.js}
%endif
