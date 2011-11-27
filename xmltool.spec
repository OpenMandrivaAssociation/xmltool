Name:           xmltool
Version:        3.3
Release:        4
Summary:        Tool to manage XML documents through a Fluent Interface

Group:          Development/Java
License:        ASL 2.0
URL:            http://code.google.com/p/xmltool
### upstream only provides binaries or source without build scripts
# tar creation instructions
# svn export http://xmltool.googlecode.com/svn/tags/xmltool-3.3 xmltool
# tar cfJ xmltool-3.3.tar.xz xmltool
Source0:        %{name}-%{version}.tar.xz
# remove dependency on maven-license-plugin and dependencies for tests
Patch0:         001-xmltool-fixbuild.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  maven2
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-deploy
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-source
BuildRequires:  maven2-plugin-clean
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-dependency
BuildRequires:  maven2-plugin-eclipse
BuildRequires:  maven2-plugin-idea
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-plugin
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-repository
BuildRequires:  maven2-plugin-remote-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven-release-plugin
BuildRequires:  maven-plugin-jxr
BuildRequires:  apache-resource-bundles

Requires:       java 
Requires:       jpackage-utils

Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

%description
XMLTool is a very simple Java library to be able to do all sorts of common 
operations with an XML document. Java developers often end up writing the same 
code for processing XML, transforming, etc. This easy to use class puts it all 
together, using the Fluent Interface pattern to facilitate XML manipulations. 

%package javadoc
Summary:        Javadocs for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1

# Fix end-of-line encoding
sed -i 's/\r//' LICENSE.txt


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

# tests require surefire/testng, not currently available
mvn-jpp \
  -e  \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  -Dmaven.test.skip=true \
  install javadoc:javadoc


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -Dp -m 644 target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && ln -sf %{name}-%{version}.jar %{name}.jar)

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp target/site/apidocs/  \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml  \
  $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

%add_to_maven_depmap com.mycila.xmltool %{name} %{version} JPP %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*
%{_javadir}/*


%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}


%post
%update_maven_depmap

%postun
%update_maven_depmap

