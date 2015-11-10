%global pypi_name oslotest

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        1.11.0
Release:        2%{?dist}
Summary:        OpenStack test framework

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
OpenStack test framework and test fixtures.

%package -n python2-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx >= 2.2.0

# test requires
BuildRequires:  python-hacking
BuildRequires:  python-six
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-mock
BuildRequires:  python-mox3


Requires: python-six
Requires: python-testrepository
Requires: python-testscenarios
Requires: python-mock
Requires: python-mox3

%description -n python2-%{pypi_name}
OpenStack test framework and test fixtures.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx >= 2.2.0

# test requires
BuildRequires:  python3-hacking
BuildRequires:  python3-six
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-mock
BuildRequires:  python3-mox3

Requires: python3-six
Requires: python3-testrepository
Requires: python3-testscenarios
Requires: python3-mock
Requires: python3-mox3

%description -n python3-%{pypi_name}
OpenStack test framework and test fixtures.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# let RPM handle deps
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

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
%doc html README.rst
%license LICENSE
%{_bindir}/oslo_run_cross_tests
%{_bindir}/oslo_run_pre_release_tests
%{_bindir}/oslo_debug_helper
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc html README.rst
%license LICENSE
%{_bindir}/python3-oslo_run_cross_tests
%{_bindir}/python3-oslo_run_pre_release_tests
%{_bindir}/python3-oslo_debug_helper
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep 18 2015 Alan Pevec <alan.pevec@redhat.com> 1.11.0-1
- Update to upstream 1.11.0

* Fri Sep 04 2015 Lukas Bezdicka <lbezdick@redhat.com> - 1.10.0-2
- change spec according to new python3 guidelines

* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 1.10.0-1
- Update to upstream 1.10.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Alan Pevec <apevec@redhat.com> - 1.1.0-2
- add dependencies

* Mon Oct 20 2014 Alan Pevec <apevec@redhat.com> - 1.1.0-1
- Initial package.
