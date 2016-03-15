#
# Conditional build:
%bcond_without	doc	# documentation (uses python2, needs repository metadata)
%bcond_with	tests	# "make test" (pytest-runner doesn't support \--build-base)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%if %{without python2}
%undefine	with_doc
%endif
Summary:	rst.linker - Python 2 Sphinx plugin to add links to the changelog
Summary(pl.UTF-8):	rst.linker - wtyczka Sphinksa dla Pythona 2 do dodawania odnośników do changeloga
Name:		python-rst.linker
Version:	1.5
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/rst.linker/
Source0:	https://pypi.python.org/packages/source/r/rst.linker/rst.linker-%{version}.tar.gz
# Source0-md5:	b9751f3b38448248ae77188fd96f65c8
URL:		https://bitbucket.org/jaraco/rst.linker
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pytest >= 2.8
BuildRequires:	python-pytest-runner
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.9
BuildRequires:	python-six
%{?with_doc:BuildRequires:	sphinx-pdg}
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-pytest >= 2.8
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.9
BuildRequires:	python3-six
%endif
Requires:	python-Sphinx
Requires:	python-dateutil
Requires:	python-six
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
Requires:	python3-dateutil
Requires:	python3-six

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
%{__python} setup.py \
	build --build-base build-2 %{?with_tests:test}

%if %{with doc}
%{__python} setup.py build_sphinx
%endif
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 %{?with_tests:test}
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
%doc CHANGES.rst
%dir %{py_sitescriptdir}/rst
%{py_sitescriptdir}/rst/linker.py[co]
%{py_sitescriptdir}/rst.linker-%{version}-py*.egg-info
%{py_sitescriptdir}/rst.linker-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-rst.linker
%defattr(644,root,root,755)
%doc CHANGES.rst
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
