# Created by pyp2rpm-1.1.1
%global pypi_name oslotest

Name:           python-%{pypi_name}
Version:        1.10.0
Release:        1%{?dist}
Summary:        OpenStack test framework

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx >= 2.2.0

Requires: python-six
Requires: python-testrepository
Requires: python-testscenarios
Requires: python-mock
Requires: python-mox3

%description
OpenStack test framework and test fixtures.


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files

%doc html README.rst LICENSE
%{_bindir}/oslo_debug_helper
%{_bindir}/oslo_run_cross_tests
%{_bindir}/oslo_run_pre_release_tests
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 1.10.0-1
- Update to upstream 1.10.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Alan Pevec <apevec@redhat.com> - 1.1.0-2
- add dependencies

* Mon Oct 20 2014 Alan Pevec <apevec@redhat.com> - 1.1.0-1
- Initial package.
