# Copyright (c) 2000-2008, JPackage Project
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
%define gcj_support 0

%define section   free

Name:           aqute-bndlib
Version:        0.0.255
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        BND Library
License:        Apache License 2.0
Group:          Development/Java
URL:            http://www.aQute.biz/Code/Bnd
Source0:        http://www.aqute.biz/repo/biz/aQute/bndlib/%{version}/bndlib-%{version}.jar
Source1:        %{name}-build.xml
# build it with maven2-generated ant build.xml
Patch0:         aQute-bndlib-Filter.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif


%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild
BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ecj
BuildRequires:  eclipse-ecj
BuildRequires:  eclipse-platform
BuildRequires:  eclipse-rcp
BuildRequires:  eclipse-jdt

Requires(post):    jpackage-utils >= 0:1.7.3
Requires(postun):  jpackage-utils >= 0:1.7.3

%description
The bnd tool helps you create and diagnose OSGi R4 bundles.
The key functions are: 
- Show the manifest and JAR contents of a bundle 
- Wrap a JAR so that it becomes a bundle 
- Create a Bundle from a specification and a class path 
- Verify the validity of the manifest entries 
The tool is capable of acting as: 
- Command line tool 
- File format 
- Directives 
- Use of macros 

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -c
cp %{SOURCE1} build.xml
mkdir -p target/site/apidocs/
mkdir -p target/classes/
mkdir -p src/main/
mv OSGI-OPT/src src/main/java
%patch0 -b .sav0

%build
export LANG=en_US.utf8
export CLASSPATH=$(build-classpath ant)
# now for eclipse 3.2.X
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.osgi_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.osgi.services_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.jface_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.ui_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.core.jobs_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.core.runtime_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.core.resources_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.ui.workbench_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.jdt.core_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.equinox.common_*.jar)
CLASSPATH=${CLASSPATH}:$(ls %{_datadir}/eclipse/plugins/org.eclipse.equinox.registry_*.jar)

%{javac} -encoding utf8 -d target/classes $(find src/main/java -name "*.java")
%{javadoc} -encoding utf8 -d target/site/apidocs -sourcepath src/main/java aQute.lib.header aQute.lib.osgi aQute.lib.qtokens aQute.lib.filter
cp LICENSE target/classes
pushd target/classes
%{jar} cmf ../../META-INF/MANIFEST.MF ../%{name}-%{version}.jar *
popd

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%add_to_maven_depmap biz.aQute bndlib %{version} JPP %{name}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
