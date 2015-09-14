#
# Conditional build:
%bcond_with	doc	# documentation (uses python2, needs repository metadata)
%bcond_with	tests	# "make test" (broken with \--build-base)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%if %{without python2}
%undefine	with_doc
%endif
Summary:	rst.linker - Python 2 Sphinx plugin to add links to the changelog
Summary(pl.UTF-8):	rst.linker - wtyczka Sphinksa dla Pythona 2 do dodawania odnośników do changeloga
Name:		python-rst.linker
Version:	1.1
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/pypi/rst.linker
Source0:	https://pypi.python.org/packages/source/r/rst.linker/rst.linker-%{version}.zip
# Source0-md5:	71f120eabb4c53277df78f3b15036d3d
URL:		https://bitbucket.org/jaraco/rst.linker
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.616
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-hgtools
BuildRequires:	python-modules
BuildRequires:	python-pytest
%{?with_doc:BuildRequires:	sphinx-pdg}
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-hgtools
BuildRequires:	python3-pytest
BuildRequires:	python3-modules
%endif
Requires:	python-Sphinx
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
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt
%dir %{py_sitescriptdir}/rst
%{py_sitescriptdir}/rst/__init__.py[co]
%{py_sitescriptdir}/rst/linker.py[co]
%{py_sitescriptdir}/rst.linker-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-rst.linker
%defattr(644,root,root,755)
%doc CHANGES.txt
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
%doc build/sphinx/html/*
%endif
