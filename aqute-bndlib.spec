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

Name:           aqute-bndlib
Version:        0.0.363
Release:        4
Summary:        BND Library
License:        ASL 2.0
Group:          Development/Java
URL:            http://www.aQute.biz/Code/Bnd
Source0:        http://www.aqute.biz/repo/biz/aQute/bnd/%{version}/bnd-%{version}.jar
Source1:        http://www.aqute.biz/repo/biz/aQute/bnd/%{version}/bnd-%{version}.pom
Source2:        aqute-service.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  eclipse-ecj
BuildRequires:  eclipse-jdt

Requires:  java >= 0:1.5.0
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

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
mkdir -p target/site/apidocs/
mkdir -p target/classes/
mkdir -p src/main/
mv OSGI-OPT/src src/main/java
pushd src/main/java
tar xfs %{SOURCE2}
popd
sed -i "s|import aQute.lib.filter.*;||g" src/main/java/aQute/bnd/make/ComponentDef.java
sed -i "s|import aQute.lib.filter.*;||g" src/main/java/aQute/bnd/make/ServiceComponent.java

%build
export LANG=en_US.utf8
export OPT_JAR_LIST=:
export CLASSPATH=$(build-classpath ant)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.osgi_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.osgi.services_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.jface_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.jface.databinding_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.jface.text_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.ui_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.ui.ide_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.core.commands_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.core.jobs_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.core.runtime_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.core.resources_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.debug.core_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.debug.ui_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.text_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.ui.console_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.ui.editors_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.ui.workbench_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.ui.workbench.texteditor_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/dropins/jdt/plugins/org.eclipse.jdt.core_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/dropins/jdt/plugins/org.eclipse.jdt.debug.ui_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/dropins/jdt/plugins/org.eclipse.jdt.launching_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/dropins/jdt/plugins/org.eclipse.jdt.junit_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/dropins/jdt/plugins/org.eclipse.jdt.junit.core_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/dropins/jdt/plugins/org.eclipse.jdt.ui_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.equinox.common_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.equinox.registry_*.jar)
CLASSPATH=${CLASSPATH}:$(ls /usr/lib*/eclipse/plugins/org.eclipse.swt.*.jar)

%{javac} -d target/classes -target 1.5 -source 1.5 $(find src/main/java -type f -name "*.java")
%{javadoc} -d target/site/apidocs -sourcepath src/main/java aQute.lib.header aQute.lib.osgi aQute.lib.qtokens aQute.lib.filter
cp -p LICENSE maven-dependencies.txt plugin.xml pom.xml target/classes
for f in $(find aQute/ -type f -not -name "*.class"); do
    cp -p $f target/classes/$f
done
pushd target/classes
%{jar} cmf ../../META-INF/MANIFEST.MF ../%{name}-%{version}.jar *
popd

sed -i "s|\r||g" LICENSE

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%add_to_maven_depmap biz.aQute bndlib %{version} JPP %{name}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_datadir}/maven2/poms/JPP-aqute-bndlib.pom
%{_mavendepmapfragdir}/aqute-bndlib

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

