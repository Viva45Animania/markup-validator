# RPM spec file for the W3C Markup Validator
# $Id: w3c-markup-validator.spec,v 1.1.2.12 2003-12-01 21:23:36 ville Exp $

Name:           w3c-markup-validator
Version:        0.6.5
Release:        0.beta1.2
Epoch:          0
Summary:        W3C Markup Validator

Group:          Applications/Internet
License:        W3C Software License
URL:            http://validator.w3.org/
Source0:        http://validator.w3.org:8001/dist/validator-0_6_5b1.tar.gz
Source1:        http://validator.w3.org:8001/dist/sgml-lib-0_6_5b1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl
Requires:       httpd, openjade >= 0:1.3.2, %{name}-libs = %{epoch}:%{version}
Obsoletes:      w3c-validator

%description
The W3C Markup Validator checks documents like HTML and XHTML for
conformance to W3C Recommendations and other standards.

%package        libs
Summary:        SGML and XML DTDs for the W3C Markup Validator
Group:          Applications/Text
Requires:       sgml-common
Obsoletes:      w3c-validator-libs

%description    libs
SGML and XML DTDs for the W3C Markup Validator.


%prep
%setup -q -a 1 -n validator-0.6.5b1
mv validator-0.6.5b1/htdocs/sgml-lib .

# Localize config files
perl -pi -e \
  's|\bwww-validator\@w3\.org\b|root\@localhost| ;
   s|/validator\.w3\.org/|/localhost/%{name}/| ;
   s|/usr/local/validator/htdocs/config/|%{_sysconfdir}/w3c/| ;
   s|/usr/local/validator/htdocs/|%{_datadir}/%{name}/| ;
   s|^(SGML\s+Library\s+).*|${1}%{_datadir}/sgml/%{name}|' \
  htdocs/config/validator.conf
perl -pi -e \
  's|/usr/share/w3c-markup-validator|%{_datadir}/%{name}|g' \
  httpd/conf/httpd.conf

# Cleanup of unused files
rm -rf htdocs/source htdocs/config/verbosemsg.rc

# Rename checklink
mv httpd/cgi-bin/checklink.pl httpd/cgi-bin/checklink

# Move config out of the way
mv htdocs/config __config

# Fixup permissions
find . -type d | xargs chmod 755
find . -type f | xargs chmod 644
chmod 755 httpd/cgi-bin/check*

# Point to validator.w3.org for source code
perl -pi -e \
  's|<!--\#echo var="relroot"\s*-->source/|http://validator.w3.org/source/|' \
  htdocs/header.html


%build
# Create the manual page.
pod2man --center="W3C Link Checker" httpd/cgi-bin/checklink > checklink.1


%install
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}

# Scripts
cp -p httpd/cgi-bin/check* $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -pm 755 $RPM_BUILD_ROOT%{_bindir}
ln -s %{_datadir}/%{name}/checklink $RPM_BUILD_ROOT%{_bindir}

# Config files
mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/w3c
cp -p __config/* $RPM_BUILD_ROOT%{_sysconfdir}/w3c
mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
cp -p httpd/conf/httpd.conf \
  $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

# HTML and stuff
cp -pR htdocs/* $RPM_BUILD_ROOT%{_datadir}/%{name}

# SGML library
mkdir -pm 755 $RPM_BUILD_ROOT%{_datadir}/sgml
cp -pR sgml-lib $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}
mkdir -pm 755 $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat

# Man pages
mkdir -pm 755 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p checklink.1 $RPM_BUILD_ROOT%{_mandir}/man1


%clean
rm -rf $RPM_BUILD_ROOT


%post libs
for catalog in "mathml.soc sgml.soc svg.soc xhtml.soc xml.soc"; do
  install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/$catalog >/dev/null 2>&1 || :
done

%preun libs
for catalog in "mathml.soc sgml.soc svg.soc xhtml.soc xml.soc"; do
  install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/$catalog >/dev/null 2>&1 || :
done


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/w3c
%{_datadir}/%{name}
%{_bindir}/checklink
%{_mandir}/man1/checklink.1*

%files libs
%defattr(-,root,root,-)
%ghost %config %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat
%{_datadir}/sgml/%{name}


%changelog
* Mon Dec  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.5-0.beta1.2
- Cleanups.

* Fri Aug 29 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.5-0.beta1.1
- Update to 0.6.5 beta 1.

* Sat Aug 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.2-5w3c
- Requires openjade >= 0:1.3.2 (Red Hat packages OpenSP 1.5 there).

* Wed Jul 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.2-4w3c
- Include checklink manual page.
- Some spec file cleanups.

* Thu Jul 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.2-3w3c
- Requires perl(Net::IP).

* Fri Jul  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.2-2w3c
- Use aliasing instead of hardcoded docroot in httpd configuration.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.2-1w3c
- Update to 0.6.2.
- Rename to w3c-markup-validator.
- Install our catalogs if %%{_bindir}/install-catalog is available.
- Add Epoch: 0.

* Sun Dec  1 2002 Ville Skyttä <ville.skytta at iki.fi> - 0.6.1-1w3c
- Update to 0.6.1.

* Fri Nov 29 2002 Ville Skyttä <ville.skytta at iki.fi> - 0.6.0-1w3c
- First release.
