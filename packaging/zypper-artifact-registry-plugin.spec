# Copyright 2023 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Don't build debuginfo packages.
%define debug_package %{nil}

Name: zypper-artifact-registry-plugin
Epoch:   1
Version: %{_version}
Release: g1%{?dist}
Summary: Zypper plugin for Artifact Registry
License: ASL 2.0
Url: https://cloud.google.com/artifact-registry
Source0: %{name}_%{version}.orig.tar.gz
BuildArch: %{_arch}

BuildRequires: go >= 1.17
BuildRequires: golang-packaging

Requires: python3-zypp-plugin

%description
Contains a Zypper plugin for authenticated access to Artifact Registry repositories.

%prep
%autosetup

%build
pushd cmd/ar-token
CGO_ENABLED=0 go build -ldflags="-s -w" -mod=readonly -buildvcs=false
popd

%install
install -d %{buildroot}/usr/libexec
install -p -m 0755 cmd/ar-token/ar-token %{buildroot}/usr/libexec/
install -d %{buildroot}/usr/lib/zypp/plugins/urlresolver
install -p -m 0755 zypper/artifact-registry %{buildroot}/usr/lib/zypp/plugins/urlresolver/artifact-registry

%files
%defattr(0755,root,root,-)
/usr/libexec/ar-token
/usr/lib/zypp/plugins/urlresolver/artifact-registry
%license LICENSE
