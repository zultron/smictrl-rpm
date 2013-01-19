# pre-release settings
%global _gitrel    20110913git39e9845
#%%global _pre       0
%global _prerel %{?_pre:.pre%{_pre}}%{?_rc:.rc%{_rc}}%{?_gitrel:.%{_gitrel}}
# e.g. 'pre3', 'rc1'  (use in tarball filename)
%global _pre_or_rc  %{?_pre:pre%{_pre}}%{?_rc:rc%{_rc}}

Name:           smictrl
Url:            http://git.kiszka.org/?p=smictrl.git
License:        GPLv2+
Group:          Applications/System
Summary:        SMI enable register manipulation tool
Version:        0.1
Release:        0.0%{?_prerel}%{?dist}
# git://git.kiszka.org/smictrl.git master branch
Source0:        %{name}-%{version}%{?_gitrel:.%{_gitrel}}.tar.bz2

BuildRequires:  kernel-devel
BuildRequires:  pciutils-devel
BuildRequires:  zlib-devel

%define kversion %(rpm -q --qf='%%{version}-%%{release}\\n' \\\
	--whatprovides kernel-devel | \\\
	sed 's/^.* not installed$/42/' | tail -1)
%global kernelinclude %{_usrsrc}/kernels/%{kversion}.%{_target_cpu}/include


%description

smictrl can work around SMI interrupts that can cause pauses of
hundreds of microseconds, unacceptable on realtime systems.


%prep
if test %{kversion} = "42"; then
   echo "Error:  Cannot find kernel-devel version" 1>&2
   exit 1
fi
%setup


%build
gcc -O2 -Wall -I%{kernelinclude} -lz -lpci  -o smictrl smictrl.c


%install
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 755 smictrl $RPM_BUILD_ROOT%{_sbindir}


%files
%defattr(-,root,root)
%{_sbindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Jan 19 2013 John Morris <john@zultron.com> - 0.1-0.0.20110913git39e9845
- Initial package based on 20110913git39e9845
