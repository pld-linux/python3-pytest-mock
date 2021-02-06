#
# Conditional build:
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Thin-wrapper around the mock package for easier use with py.test
Summary(pl.UTF-8):	Cienka warstwa obudowująca pakiet mock, ułatwiająca używanie wraz z py.test
Name:		python-pytest-mock
# keep 2.x here for python2 support
Version:	2.0.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-mock/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-mock/pytest-mock-%{version}.tar.gz
# Source0-md5:	b6bcfb98b922b666d9a0db21a38f9d8a
URL:		https://pypi.org/project/pytest-mock/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 2.7
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-pytest >= 2.7
# there is py3 test which relies on "mock" standalone module not being installed
BuildConflicts:	python3-mock
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin installs a mocker fixture which is a thin-wrapper around
the patching API provided by the mock package, but with the benefit of
not having to worry about undoing patches at the end of a test.

%description -l pl.UTF-8
Ta wtyczka instaluje osprzęt (fixture) do tworzenia atrap, będący
cienką warstwą ponad API dostarczane przez pakiet mock, ale
pozwalający nie martwić się o wycofywanie łat na końcu testu.

%package -n python3-pytest-mock
Summary:	Thin-wrapper around the mock package for easier use with py.test
Summary(pl.UTF-8):	Cienka warstwa obudowująca pakiet mock, ułatwiająca używanie wraz z py.test
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-pytest-mock
This plugin installs a mocker fixture which is a thin-wrapper around
the patching API provided by the mock package, but with the benefit of
not having to worry about undoing patches at the end of a test.

%description -n python3-pytest-mock -l pl.UTF-8
Ta wtyczka instaluje osprzęt (fixture) do tworzenia atrap, będący
cienką warstwą ponad API dostarczane przez pakiet mock, ale
pozwalający nie martwić się o wycofywanie łat na końcu testu.

%prep
%setup -q -n pytest-mock-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_mock" \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_mock" \
%{__python3} -m pytest tests
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
%doc CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/pytest_mock
%{py_sitescriptdir}/pytest_mock-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest-mock
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_mock
%{py3_sitescriptdir}/pytest_mock-%{version}-py*.egg-info
%endif
