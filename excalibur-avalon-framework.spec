# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

# If you want to build with maven insteaf of straight ant,
# give rpmbuild option '--with maven'

%define with_maven %{!?_with_maven:0}%{?_with_maven:1}
%define without_maven %{?_with_maven:0}%{!?_with_maven:1}

%define section  free
%define grname   excalibur
%define orname   avalon-framework

Name:           excalibur-avalon-framework
Version:        4.3
Release:        %mkrel 7
Epoch:          0
Summary:        Avalon Framework
License:        Apache Software License 2.0
Url:            http://excalibur.apache.org/
Group:          Development/Java
Source0:        http://www.apache.org/dist/excalibur/avalon-framework/source/avalon-framework-api-4.3-src.tar.gz
Source1:        pom-maven2jpp-depcat.xsl
Source2:        pom-maven2jpp-newdepmap.xsl
Source3:        pom-maven2jpp-mapdeps.xsl
Source4:        avalon-framework-4.3-jpp-depmap.xml
Source5:        excalibur-avalon-framework-project-common.xml
Source6:        excalibur-buildsystem.tar.gz
Source7:        http://www.apache.org/dist/excalibur/avalon-framework/source/avalon-framework-impl-4.3-src.tar.gz
Source8:        excalibur-avalon-framework-api-build.xml
Source9:        excalibur-avalon-framework-impl-build.xml
Patch0:         excalibur-avalon-framework-api-4.3-project_xml.patch
Patch1:         excalibur-avalon-framework-impl-4.3-project_xml.patch
%if %{with_maven}
BuildRequires:  maven >= 0:1.1
BuildRequires:  jmock
%else
BuildRequires:  ant >= 0:1.6
%endif
BuildRequires:  junit
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  excalibur-avalon-logkit
BuildRequires:  jakarta-commons-logging
BuildRequires:  log4j
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis

Requires:       excalibur-avalon-logkit
Requires:       jakarta-commons-logging
Requires:       log4j
Requires:       xalan-j2
Requires:       xerces-j2
Requires:       xml-commons-apis
Obsoletes:      avalon-framework
Provides:       avalon-framework
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:  %{_tmppath}/%{name}-%{version}-buildroot
%if %{gcj_support}
BuildRequires:    gnu-crypto
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description
The Avalon Framework consists of interfaces that define 
relationships between commonly used application components, 
best-of-practice pattern enforcements, and several lightweight 
convenience implementations of the generic components

%package api
Summary:  Avalon Framework API
Group:    Development/Java
Requires: excalibur-avalon-logkit

%description api
%{summary}.

%package impl
Summary:  Avalon Framework Implementation
Group:    Development/Java
Requires:       excalibur-avalon-framework-api
Requires:       excalibur-avalon-logkit
Requires:       jakarta-commons-logging
Requires:       log4j
Requires:       xalan-j2
Requires:       xerces-j2
Requires:       xml-commons-apis

%description impl
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Obsoletes:      avalon-framework-javadoc
Provides:       avalon-framework-javadoc
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
%{summary}.

%package api-javadoc
Summary:        Javadoc for %{name} API
Group:          Development/Java
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description api-javadoc
%{summary}.

%package impl-javadoc
Summary:        Javadoc for %{name} Implementation
Group:          Development/Java
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description impl-javadoc
%{summary}.

%prep
%setup -q -c -n %{name}-%{version}
gzip -dc %{SOURCE7} | tar xf -
# remove all binary libs
#find . -name "*.jar" -exec rm -f {} \;
for j in $(find . -name "*.jar"); do
      mv $j $j.no
done
pushd %{orname}-api-%{version}
cp %{SOURCE5} project-common.xml
gzip -dc %{SOURCE6} | tar xf -
cp %{SOURCE8} build.xml
%patch0 -b .sav
popd
pushd %{orname}-impl-%{version}
cp %{SOURCE5} project-common.xml
gzip -dc %{SOURCE6} | tar xf -
cp %{SOURCE9} build.xml
%patch1 -b .sav
popd


%build
%if %{with_maven}
export DEPCAT=$(pwd)/avalon-framework-4.3-depcat.new.xml
echo '<?xml version="1.0" standalone="yes"?>' > $DEPCAT
echo '<depset>' >> $DEPCAT
for p in $(find . -name project.xml); do
    pushd $(dirname $p)
    /usr/bin/saxon project.xml %{SOURCE1} >> $DEPCAT
    popd
done
echo >> $DEPCAT
echo '</depset>' >> $DEPCAT
/usr/bin/saxon $DEPCAT %{SOURCE2} > avalon-framework-4.3-depmap.new.xml
for p in $(find . -name project.xml); do
    pushd $(dirname $p)
    cp project.xml project.xml.orig
    /usr/bin/saxon -o project.xml project.xml.orig %{SOURCE3} map=%{SOURCE4}
    popd
done

export MAVEN_HOME_LOCAL=$(pwd)/.maven

pushd %{orname}-api-%{version}
maven \
        -Dmaven.repo.remote=file:/usr/share/maven/repository \
        -Dmaven.home.local=$MAVEN_HOME_LOCAL \
        jar:install javadoc
popd
pushd %{orname}-impl-%{version}
maven \
        -Dmaven.repo.remote=file:/usr/share/maven/repository \
        -Dmaven.home.local=$MAVEN_HOME_LOCAL \
        jar javadoc
popd
%else
pushd %{orname}-api-%{version}
export CLASSPATH=$(build-classpath excalibur/avalon-logkit):target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd %{orname}-impl-%{version}
CLASSPATH=../%{orname}-api-%{version}/target/%{orname}-api-%{version}.jar:$CLASSPATH
ant -Dbuild.sysclasspath=only jar javadoc
popd
%endif
mkdir target
pushd target
jar xf ../%{orname}-impl-%{version}/target/%{orname}-impl-%{version}.jar
jar xf ../%{orname}-api-%{version}/target/%{orname}-api-%{version}.jar
jar cf %{orname}-%{version}.jar *
popd


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{grname}
install -m 644 \
        target/%{orname}-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{orname}-%{version}.jar
install -m 644 \
        %{orname}-api-%{version}/target/%{orname}-api-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{grname}/%{orname}-api-%{version}.jar
install -m 644 \
        %{orname}-impl-%{version}/target/%{orname}-impl-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{grname}/%{orname}-impl-%{version}.jar

# create unversioned symlinks
(cd $RPM_BUILD_ROOT%{_javadir}/ && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
(cd $RPM_BUILD_ROOT%{_javadir}/%{grname} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api-%{version}
%if %{with_maven}
cp -pr %{orname}-api-%{version}/target/docs/apidocs/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api-%{version}
%else
cp -pr %{orname}-api-%{version}/dist/docs/api/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api-%{version}
%endif
ln -s %{name}-api-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api # ghost symlink
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
%if %{with_maven}
cp -pr %{orname}-impl-%{version}/target/docs/apidocs/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
%else
cp -pr %{orname}-impl-%{version}/dist/docs/api/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
%endif
ln -s %{name}-impl-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl # ghost symlink

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
%if %{with_maven}
cp -pr %{orname}-api-%{version}/target/docs/apidocs/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
%else
cp -pr %{orname}-api-%{version}/dist/docs/api/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
%endif
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/impl
%if %{with_maven}
cp -pr %{orname}-impl-%{version}/target/docs/apidocs/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/impl
%else
cp -pr %{orname}-impl-%{version}/dist/docs/api/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/impl
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp %{orname}-api-%{version}/LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%if %{gcj_support}
export CLASSPATH=$(build-classpath gnu-crypto)
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%post api-javadoc
rm -f %{_javadocdir}/%{name}-api
ln -s %{name}-api-%{version} %{_javadocdir}/%{name}-api

%post impl-javadoc
rm -f %{_javadocdir}/%{name}-impl
ln -s %{name}-impl-%{version} %{_javadocdir}/%{name}-impl

%postun javadoc
if [ "$1" = "0" ]; then
  rm -f %{_javadocdir}/%{name}
fi

%postun api-javadoc
if [ "$1" = "0" ]; then
  rm -f %{_javadocdir}/%{name}-api
fi

%postun impl-javadoc
if [ "$1" = "0" ]; then
  rm -f %{_javadocdir}/%{name}-impl
fi

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files 
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/*.jar
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{orname}-%{version}.jar.*
%endif

%files api
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{grname}/%{orname}-api*.jar

%files impl
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{grname}/%{orname}-impl*.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files api-javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-api-%{version}
%ghost %{_javadocdir}/%{name}-api

%files impl-javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-impl-%{version}
%ghost %{_javadocdir}/%{name}-impl

