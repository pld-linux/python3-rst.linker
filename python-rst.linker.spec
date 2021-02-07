#
# Conditional build:
%bcond_without	doc	# documentation (uses python2, needs repository metadata)
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%if %{without python2}
%undefine	with_doc
%endif
Summary:	rst.linker - Python 2 Sphinx plugin to add links to the changelog
Summary(pl.UTF-8):	rst.linker - wtyczka Sphinksa dla Pythona 2 do dodawania odnośników do changeloga
Name:		python-rst.linker
Version:	1.11
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/rst.linker/
Source0:	https://files.pythonhosted.org/packages/source/r/rst.linker/rst.linker-%{version}.tar.gz
# Source0-md5:	9541a7debee1c5b4ac54350696082664
URL:		https://github.com/jaraco/rst.linker
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:31.0.1
BuildRequires:	python-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python-dateutil
BuildRequires:	python-importlib_metadata
BuildRequires:	python-path
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-black-multipy
BuildRequires:	python-pytest-flake8
BuildRequires:	python-six
%endif
%if %{with doc}
BuildRequires:	python-Sphinx
BuildRequires:	python-jaraco.packaging >= 3.2
# needs to be already installed
BuildRequires:	python-rst.linker >= 1.9
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python3-dateutil
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-path
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-black-multipy
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-Sphinx
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rst.linker is a Sphinx plugin to add links to the changelog.

%description -l pl.UTF-8
rst.linker to wtyczka Sphinksa służąca do dodawania odnośników do
changeloga.

%package -n python3-rst.linker
Summary:	rst.linker - Python 3 Sphinx plugin to add links to the changelog
Summary(pl.UTF-8):	rst.linker - wtyczka Sphinksa dla Pythona 3 do dodawania odnośników do changeloga
Group:		Libraries/Python
Requires:	python3-Sphinx

%description -n python3-rst.linker
rst.linker is a Sphinx plugin to add links to the changelog.

%description -n python3-rst.linker -l pl.UTF-8
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

%build
%if %{with python2}
%py_build %{?with_doc:build_sphinx}

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black_multipy,pytest_flake8" \
%{__python} -m pytest test_all.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_black,pytest_black_multipy,pytest_flake8" \
%{__python3} -m pytest test_all.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%dir %{py_sitescriptdir}/rst
%{py_sitescriptdir}/rst/__init__.py[co]
%{py_sitescriptdir}/rst/linker.py[co]
%{py_sitescriptdir}/rst.linker-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-rst.linker
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%dir %{py3_sitescriptdir}/rst
%{py3_sitescriptdir}/rst/__init__.py
%{py3_sitescriptdir}/rst/linker.py
%dir %{py3_sitescriptdir}/rst/__pycache__
%{py3_sitescriptdir}/rst/__pycache__/__init__.cpython-*.py[co]
%{py3_sitescriptdir}/rst/__pycache__/linker.cpython-*.py[co]
%{py3_sitescriptdir}/rst.linker-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build-2/sphinx/html/{_static,*.html,*.js}
%endif
