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
Version:	1.8.2
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/rst.linker/
Source0:	https://pypi.python.org/packages/95/a8/8efe7a856db37dd3ca95f434525741e90f6133b868ab57e61f410578607e/rst.linker-%{version}.tar.gz
# Source0-md5:	783b4591bad3449d713b5b4428fb71d6
URL:		https://bitbucket.org/jaraco/rst.linker
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python-dateutil
BuildRequires:	python-path
BuildRequires:	python-pytest >= 2.8
BuildRequires:	python-six
%endif
%{?with_doc:BuildRequires:	sphinx-pdg}
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python3-dateutil
BuildRequires:	python3-path
BuildRequires:	python3-pytest >= 2.8
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
%py_build

%{?with_tests:%{__python} -m pytest test_all.py}

%if %{with doc}
%{__python} setup.py build_sphinx
%endif
%endif

%if %{with python3}
%py3_build

%{?with_tests:%{__python3} -m pytest test_all.py}
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
%doc CHANGES.rst README.rst
%dir %{py_sitescriptdir}/rst
%{py_sitescriptdir}/rst/linker.py[co]
%{py_sitescriptdir}/rst.linker-%{version}-py*.egg-info
%{py_sitescriptdir}/rst.linker-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-rst.linker
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py3_sitescriptdir}/rst
%{py3_sitescriptdir}/rst/linker.py
%dir %{py3_sitescriptdir}/rst/__pycache__
%{py3_sitescriptdir}/rst/__pycache__/linker.cpython-*.py[co]
%{py3_sitescriptdir}/rst.linker-%{version}-py*.egg-info
%{py3_sitescriptdir}/rst.linker-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/sphinx/html/*
%endif
