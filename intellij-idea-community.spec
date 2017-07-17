# don't strip bundled binaries because intellij checks length (!!!) of binary fsnotif
# and if you strip debug stuff from it, it will complain
%global __strip /bin/true
# dont repack jars
%global __jar_repack %{nil}
# there are some python 2 and python 3 scripts so there is no way out to bytecompile them ^_^
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%if 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:          intellij-idea-community
Version:       2017.1.5
Release:       1%{?dist}
Summary:       Intelligent Python IDE
License:       ASL 2.0
URL:           https://www.jetbrains.com/idea/

Source0:       https://download.jetbrains.com/idea/ideaIC-%{version}-no-jdk.tar.gz

Source101:     intellij-idea.xml
Source102:     intellij-idea-community.desktop
Source103:     intellij-idea-community.appdata.xml

BuildRequires: desktop-file-utils
BuildRequires: /usr/bin/appstream-util
BuildRequires: python2-devel
%if %{with python3}
BuildRequires: python3-devel
%endif
Requires:      java

%description
The intelligent Python IDE with unique code assistance and analysis,
for productive Python development on all levels

%package plugins
Summary:       Plugins for intelligent Python IDE
Requires:      %{name}%{?_isa} = %{version}-%{release}

%package doc
Summary:       Documentation for intelligent Python IDE
BuildArch:     noarch

%description plugins
Intelligent Python IDE contains several plugins. This package
contains plugins like BashSupport, GoLang, Markdown, Idea Markdown
Intellij Ansible, GitLab integration plugin.

%description doc
This package contains documentation for Intelligent Python IDE.

%prep
%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_javadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/appdata
mkdir -p %{buildroot}%{_bindir}

mv idea-markdown-%{markdown_version} idea-markdown
cp -arf ./{lib,bin,help,helpers,plugins} %{buildroot}%{_javadir}/%{name}/

rm -f %{buildroot}%{_javadir}/%{name}/bin/fsnotifier{,-arm}
# this will be in docs
rm -f %{buildroot}%{_javadir}/help/*.pdf
cp -af ./bin/pycharm.png %{buildroot}%{_datadir}/pixmaps/pycharm.png
cp -af %{SOURCE101} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
cp -af %{SOURCE102} %{buildroot}%{_datadir}/intellij-idea-community.desktop
cp -a %{SOURCE103} %{buildroot}%{_datadir}/appdata
ln -s %{_javadir}/%{name}/bin/pycharm.sh %{buildroot}%{_bindir}/pycharm
desktop-file-install                          \
--add-category="Development"                  \
--delete-original                             \
--dir=%{buildroot}%{_datadir}/applications    \
%{buildroot}%{_datadir}/intellij-idea-community.desktop

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/pycharm-community.appdata.xml

%files
%{_datadir}/applications/intellij-idea-community.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/pycharm.png
%{_datadir}/appdata/intellij-idea-community.appdata.xml
%{_javadir}/%{name}
%{_bindir}/pycharm

%post
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files doc
%doc *.txt
%doc help/*.pdf
%license license/

%changelog
* Mon Jul 17 2017 Allan Lewis <allanlewis99@gmail.com> - 2017.1.5-1
- First release; based on latest upstream version, 2017.1.5.
