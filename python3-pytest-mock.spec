#
# Conditional build:
%bcond_without	tests	# py.test tests

Summary:	Thin-wrapper around the mock package for easier use with py.test
Summary(pl.UTF-8):	Cienka warstwa obudowująca pakiet mock, ułatwiająca używanie wraz z py.test
Name:		python3-pytest-mock
Version:	3.10.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-mock/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-mock/pytest-mock-%{version}.tar.gz
# Source0-md5:	29c685fb54fbac80aae0e551bcbaab31
Patch0:		pytest-mock-tests.patch
URL:		https://pypi.org/project/pytest-mock/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-pytest >= 5.0
BuildRequires:	python3-pytest-asyncio
# there is py3 test which relies on "mock" standalone module not being installed
BuildConflicts:	python3-mock
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.7
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

%prep
%setup -q -n pytest-mock-%{version}
%patch0 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin,pytest_mock" \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/pytest_mock
%{py3_sitescriptdir}/pytest_mock-%{version}-py*.egg-info
