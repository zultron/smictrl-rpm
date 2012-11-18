Name:           smictrl
Url:            http://www.rts.uni-hannover.de
License:        GPLv2+
Group:          Applications/System
Summary:        SMI Tool
Version:        0.1.2006
Release:        1
Source0:        %{name}.tar.bz2

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
%setup  -n smictrl


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
* Fri Nov 16 2012 John Morris <john@zultron.com> - 0.1.2006-1
- Initial package

