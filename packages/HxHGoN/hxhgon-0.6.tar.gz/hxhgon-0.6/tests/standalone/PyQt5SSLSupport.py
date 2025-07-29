#     Copyright 2025, GONHXH, @T_T_Z_T find license text at end of file


# Gon-skip-unless-imports: PyQt5.QtGui

# Gon-project: --mode=standalone
# Gon-project: --enable-plugin=pyqt5

# Gon-project-if: {OS} == "Darwin":
#   Gon-project: --mode=app

from PyQt5.QtNetwork import QSslSocket

print("SSL support: %r" % (QSslSocket.supportsSsl(),))

#     Python test originally created or extracted from other peoples work. The
#     parts from me are licensed as below. It is at least Free Software where
#     it's copied from other people. In these cases, that will normally be
#     indicated.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
