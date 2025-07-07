#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests

Summary:	Thin-wrapper around the mock package for easier use with py.test
Summary(pl.UTF-8):	Cienka warstwa obudowująca pakiet mock, ułatwiająca używanie wraz z py.test
Name:		python3-pytest-mock
Version:	3.14.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-mock/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-mock/pytest_mock-%{version}.tar.gz
# Source0-md5:	f0cc01a3fdc4155b381ef73301d4776f
URL:		https://pypi.org/project/pytest-mock/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 6.2.5
BuildRequires:	python3-pytest-asyncio
# there is py3 test which relies on "mock" standalone module not being installed
BuildConflicts:	python3-mock
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
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

%package apidocs
Summary:	API documentation for Python pytest_mock module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest_mock
Group:		Documentation

%description apidocs
API documentation for Python pytest_mock module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest_mock.

%prep
%setup -q -n pytest_mock-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd)/src \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin,pytest_mock" \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst SECURITY.md
%{py3_sitescriptdir}/pytest_mock
%{py3_sitescriptdir}/pytest_mock-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
