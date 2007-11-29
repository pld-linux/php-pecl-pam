%define		modname	pam
%define		_status		stable
Summary:	%{modname} - PAM integration
Summary(pl.UTF-8):	%{modname} - intergracja z PAM-em
Name:		php-pecl-%{modname}
Version:	1.0.2
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	5ea92fe39ef2ba45366ee194fcd86734
URL:		http://pecl.php.net/package/PAM/
BuildRequires:	pam-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides PAM (Pluggable Authentication Modules)
integration. PAM is a system of libraries that handle the
authentication tasks of applications and services. The library
provides a stable API for applications to defer to for authentication
tasks.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie to dostarcza wsparcia dla PAM (Pluggable Authentitcation
Modules). PAM to system bibliotek obsługujących proces autentykacji
aplikacji i usług. Biblioteka dostarcza stabilnego API umożliwiającego
aplikacjom obsłużenie zadań autentykacji.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{modname}-%{version}/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
