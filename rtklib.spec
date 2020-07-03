%global gitcommit_full c6e6c03143c5b397a9217fae2f6423ccf9c03fb7
%global gitcommit %(c=%{gitcommit_full}; echo ${c:0:7})

%global tools_build convbin pos2kml str2str rnx2rtkp rtkrcv

Name:           rtklib
Version:        2.4.3.b33
Release:        1%{?dist}
Summary:        Program Package for GNSS Positioning

License:        BSD
URL:            http://www.rtklib.com
Source0:        https://github.com/tomojitakasu/RTKLIB/tarball/%{gitcommit_full}
# Full readme from master branch
Source1:        https://raw.githubusercontent.com/tomojitakasu/RTKLIB/master/readme.txt
# https://github.com/JensReimann/RTKLIB/tree/rtklib_2.4.3
# ceb8106d53afa44cad6c45ae7873ba85ca458dc5
Patch0:         rtklib-qt.patch

BuildRequires:  gcc
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtserialport-devel
BuildRequires:  lapack-devel
BuildRequires:  chrpath


%description
RTKLIB is an open source program package for standard and precise
positioning with GNSS (global navigation satellite system). RTKLIB
consists of a portable program library and several APs (application
programs) utilizing the library.

%package        devel
Summary:        Include files and mandatory libraries for development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development.

%package        qt
Summary:        RTKLIB GUI tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    qt
GUI part of RTKLIB tools.

%package        doc
Summary:        RTKLIB manual
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    doc
Manual for RTKLIB tools.

%prep
%setup -n tomojitakasu-RTKLIB-%{gitcommit}
cp %{SOURCE1} readme_orig.txt
%patch0 -p1

sed -e "s|target.path = /usr/lib|target.path = %{buildroot}%{_libdir}|" \
    -e "s|staticlib|sharedlib|" -i src/src.pro
sed -i "s|LDLIBS  = ../../../lib/iers/gcc/iers.a|LDLIBS  = ../../../lib/libiers.a|" app/rnx2rtkp/gcc/makefile
# Correct CLI tools build flags
for i in %{tools_build}; do
    pushd app/$i/gcc
        sed -i "s|-O3|%{optflags}|" makefile
    popd
done


%build
# Build GUI tools
%{qmake_qt5}
%make_build
# Build lib
pushd lib
    %{qmake_qt5}
    %make_build
popd
# Build cli tools
for i in %{tools_build}; do
    pushd app/$i/gcc
        %make_build
    popd
done

%install
%make_install
mkdir -p %{buildroot}/%{_bindir}
install -m 755 app/rtknavi_qt/rtknavi_qt %{buildroot}%{_bindir}
install -m 755 app/rtkget_qt/rtkget_qt %{buildroot}%{_bindir}
install -m 755 app/rtkplot_qt/rtkplot_qt %{buildroot}%{_bindir}
install -m 755 app/rtkpost_qt/rtkpost_qt %{buildroot}%{_bindir}
install -m 755 app/rtklaunch_qt/rtklaunch_qt %{buildroot}%{_bindir}
install -m 755 app/srctblbrows_qt/srctblbrows_qt %{buildroot}%{_bindir}
install -m 755 app/strsvr_qt/strsvr_qt %{buildroot}%{_bindir}
install -m 755 app/rtkconv_qt/rtkconv_qt %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m 755 app/convbin/gcc/convbin %{buildroot}%{_bindir}
install -m 755 app/pos2kml/gcc/pos2kml %{buildroot}%{_bindir}
install -m 755 app/str2str/gcc/str2str %{buildroot}%{_bindir}
install -m 755 app/rnx2rtkp/gcc/rnx2rtkp %{buildroot}%{_bindir}
install -m 755 app/rtkrcv/gcc/rtkrcv %{buildroot}%{_bindir}
install -m 755 app/rtkrcv/gcc/rtk*.sh %{buildroot}%{_bindir}
install -m 644 data/* %{buildroot}%{_datadir}/%{name}

chrpath --delete %{buildroot}%{_bindir}/*_qt


%files
# %license add-license-file-here
%doc readme.txt readme_orig.txt
%{_bindir}/convbin
%{_bindir}/pos2kml
%{_bindir}/str2str
%{_bindir}/rnx2rtkp
%{_bindir}/rtkrcv
%{_bindir}/rtkstart.sh
%{_bindir}/rtkshut.sh
%{_libdir}/libRTKLib.so.1*
%{_datadir}/%{name}/

%files qt
%{_bindir}/rtknavi_qt
%{_bindir}/rtkget_qt
%{_bindir}/rtkplot_qt
%{_bindir}/rtkpost_qt
%{_bindir}/rtklaunch_qt
%{_bindir}/srctblbrows_qt
%{_bindir}/strsvr_qt
%{_bindir}/rtkconv_qt

%files doc
%doc doc

%files devel
%{_libdir}/libRTKLib.so


%changelog
* Wed Jul  1 2020 Vasiliy Glazov <vascom2@gmail.com> - 2.4.3.b33-1
- Initial packaging
