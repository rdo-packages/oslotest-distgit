%global pypi_name oslotest

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?repo_bootstrap} == 0
%global with_doc 1
%else
%global with_doc 0
%endif

%global common_desc OpenStack test framework and test fixtures.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack test framework

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools


# test requires
BuildRequires:  python2-six
BuildRequires:  python2-mock
BuildRequires:  python2-mox3
BuildRequires:  python2-debtcollector
BuildRequires:  python2-stestr
%if 0%{?repo_bootstrap} == 0
BuildRequires:  python2-os-client-config
BuildRequires:  python2-oslo-config
%endif

Requires: python2-debtcollector >= 1.2.0
Requires: python2-fixtures
# os-client-config is a dependency but it's circular dependency making it
# imposible to bootstrap the repo.
%if 0%{?repo_bootstrap} == 0
Requires: python2-os-client-config
%endif
Requires: python2-six
Requires: python2-subunit
Requires: python2-testtools
Requires: python2-mock
Requires: python2-mox3 >= 0.7.0
Requires: python2-stestr


%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

# test requires
BuildRequires:  python3-six
BuildRequires:  python3-stestr
BuildRequires:  python3-mock
BuildRequires:  python3-mox3
BuildRequires:  python3-debtcollector
%if 0%{?repo_bootstrap} == 0
BuildRequires:  python3-os-client-config
BuildRequires:  python3-oslo-config
%endif

Requires: python3-debtcollector >= 1.2.0
Requires: python3-fixtures
%if 0%{?repo_bootstrap} == 0
Requires: python3-os-client-config
%endif
Requires: python3-six
Requires: python3-subunit
Requires: python3-stestr
Requires: python3-testtools
Requires: python3-mock
Requires: python3-mox3 >= 0.7.0

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for the OpenStack test framework

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{pypi_name}-doc
%{common_desc} Documentation
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
%{__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%{_bindir}/oslo_run_cross_tests
%{_bindir}/oslo_run_pre_release_tests
%{_bindir}/oslo_debug_helper
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%{_bindir}/python3-oslo_run_cross_tests
%{_bindir}/python3-oslo_run_pre_release_tests
%{_bindir}/python3-oslo_debug_helper
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%doc README.rst
%endif

%changelog
