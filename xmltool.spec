%{?_javapackages_macros:%_javapackages_macros}
Name:           xmltool
Version:        3.3
Release:        10.0%{?dist}
Summary:        Tool to manage XML documents through a Fluent Interface


License:        ASL 2.0
URL:            http://code.google.com/p/xmltool
### upstream only provides binaries or source without build scripts
# tar creation instructions
# svn export http://xmltool.googlecode.com/svn/tags/xmltool-3.3 xmltool
# tar cfJ xmltool-3.3.tar.xz xmltool
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-remote-resources-plugin
BuildRequires:  maven-surefire-provider-testng
BuildRequires:  apache-resource-bundles

%description
XMLTool is a very simple Java library to be able to do all sorts of common 
operations with an XML document. Java developers often end up writing the same 
code for processing XML, transforming, etc. This easy to use class puts it all 
together, using the Fluent Interface pattern to facilitate XML manipulations. 

%package javadoc
Summary:        Javadocs for %{name}


%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}

# Fix end-of-line encoding
sed -i 's/\r//' LICENSE.txt

%mvn_file : %{name}

%build
# Remove dep on maven-wagon and maven-license plugins
%pom_xpath_remove "pom:build/pom:extensions"
%pom_remove_plugin com.google.code.maven-license-plugin:maven-license-plugin

# Disable tests because they require an internet connection to run!
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Aug 29 2013 Mat Booth <fedora@matbooth.co.uk> - 3.3-10
- Update for newer guidelines, rhbz #993147

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Mat Booth <fedora@matbooth.co.uk> - 3.3-8
- Fix FTBFS rhbz #914589.
- Drop pom patch (use macros instead.)
- Include licence file in javadoc package.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.3-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 3.3-3
- Build with maven 3.
- Adapt to current guidelines.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 08 2010 Guido Grazioli <guido.grazioli@gmail.com> - 3.3-1
- Initial packaging
