Name:           intellij-idea-community
Version:        2017.1.5
Release:        1%{?dist}
Summary:        Intelligent Java IDE

License:        ASL 2.0
URL:            https://www.jetbrains.com/idea/
Source0:        https://download.jetbrains.com/idea/ideaIC-%{version}-no-jdk.tar.gz

BuildRequires:  pv
#Requires:

%description
Every aspect of IntelliJ IDEA is specifically designed to maximize developer
productivity. Together, powerful static code analysis and ergonomic design make
development not only productive but also an enjoyable experience.

%prep
mkdir -pv %{buildroot}/idea
cd %{buildroot}
pv -f %{SOURCE0} | tar -zx --strip-components=1 -C idea
#mkdir -pv %{buildroot}%{_javadir}/%{name}/plugins
#cp -ar idea/plugins/* %{buildroot}%{_javadir}/%{name}/plugins
#exit 1

#%install

%files
#%license idea-%{build}/LICENSE.txt
#%doc foodocs

%changelog
* Mon Jul 17 2017 Allan Lewis <allanlewis99@gmail.com>
- Initial release, 2017.1.5.
