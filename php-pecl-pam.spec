%define		modname	pam
%define		status	stable
Summary:	%{modname} - PAM integration
Summary(pl.UTF-8):	%{modname} - integracja z PAM-em
Name:		php-pecl-%{modname}
Version:	1.0.3
Release:	5
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	2dfd378a76021245050333cd4d49ed96
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

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to zapewnia integrację z systemem PAM (Pluggable
Authentication Modules). PAM to system bibliotek obsługujących proces
uwierzytelniania aplikacji i usług. Biblioteka dostarcza stabilne API
umożliwiające aplikacjom obsłużenie zadań uwierzytelniania.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
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
%doc CREDITS README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
