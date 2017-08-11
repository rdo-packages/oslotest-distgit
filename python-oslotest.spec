%global pypi_name oslotest
%global repo_bootstrap 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?repo_bootstrap} == 0
%global with_doc 1
%else
%global with_doc 0
%endif

Name:           python-%{pypi_name}
Version:        2.17.0
Release:        1%{?dist}
Summary:        OpenStack test framework

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
OpenStack test framework and test fixtures.

%package -n python2-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  git
# doc requires
%if 0%{?with_doc}
BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-os-client-config
BuildRequires:  python-oslo-config
%endif

# test requires
BuildRequires:  python-six
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-mock
BuildRequires:  python-mox3
BuildRequires:  python-debtcollector

Requires: python-debtcollector >= 1.2.0
Requires: python-fixtures
# os-client-config is a dependency but it's circular dependency making it
# imposible to bootstrap the repo.
#Requires: python-os-client-config
Requires: python-six
Requires: python-subunit
Requires: python-testrepository
Requires: python-testscenarios
Requires: python-testtools
Requires: python-mock
Requires: python-mox3 >= 0.7.0


%description -n python2-%{pypi_name}
OpenStack test framework and test fixtures.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr

# test requires
BuildRequires:  python3-six
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-mock
BuildRequires:  python3-mox3
BuildRequires:  python3-debtcollector

Requires: python3-debtcollector >= 1.2.0
Requires: python3-fixtures
#Requires: python3-os-client-config
Requires: python3-six
Requires: python3-subunit
Requires: python3-testrepository
Requires: python3-testscenarios
Requires: python3-testtools
Requires: python3-mock
Requires: python3-mox3 >= 0.7.0

%description -n python3-%{pypi_name}
OpenStack test framework and test fixtures.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# let RPM handle deps
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/oslo_run_cross_tests \
   %{buildroot}%{_bindir}/python3-oslo_run_cross_tests
mv %{buildroot}%{_bindir}/oslo_run_pre_release_tests \
   %{buildroot}%{_bindir}/python3-oslo_run_pre_release_tests
mv %{buildroot}%{_bindir}/oslo_debug_helper \
   %{buildroot}%{_bindir}/python3-oslo_debug_helper
%endif
%{__python2} setup.py install --skip-build --root %{buildroot}

%check
%{__python2} setup.py test
%if 0%{?with_python3}
# cleanup testrepository before running again
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%if 0%{?with_doc}
%doc doc/build/html README.rst
%endif
%license LICENSE
%{_bindir}/oslo_run_cross_tests
%{_bindir}/oslo_run_pre_release_tests
%{_bindir}/oslo_debug_helper
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%if 0%{?with_doc}
%doc doc/build/html README.rst
%endif
%license LICENSE
%{_bindir}/python3-oslo_run_cross_tests
%{_bindir}/python3-oslo_run_pre_release_tests
%{_bindir}/python3-oslo_debug_helper
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.egg-info
%endif

%changelog
* Fri Aug 11 2017 Alfredo Moralejo <amoralej@redhat.com> 2.17.0-1
- Update to 2.17.0

