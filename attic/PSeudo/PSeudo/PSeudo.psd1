# Copyright 2021 Josh Holbrook
#
# The companies, organizations and individuals on this list; and subsidiaries of said
# companies, organizations or individuals; do not have a license to use this sofware:
#
# - Google and Alphabet - This is for many reasons, up to and including the
#   gutting of the Ethical AI team at Google, including the firings of
#   Timnit Gebru and Meg Mitchell
# - Facebook, for their irresponsible handling of false information and right
#   wing extremism on their platform especially following the 2016 presidential
#   election
# - GitHub, for their contracts with ICE
#
# This list overrides any license that may be granted by other portions of this
# software's licensing, excepting for when copyright disallows it.
#
#
# MIT License (Expat)
#
# Copyright (c) 2020 Josh Holbrook
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

@{
  RootModule = 'PSeudo.psm1'
  ModuleVersion = '2.0.1'
  GUID = 'd540a6db-930e-4b14-bd04-4ed21eeed8c3'
  Author = 'Josh Holbrook'
  CompanyName = 'Josh Holbrook'
  Copyright = 'Copyright 2021 Josh Holbrook. Copyright (c) 2014 msumimz. Licensed under an MIT/Expat license with additional restrictions.'
  Description = 'Execute PowerShell commands as Administrator in Windows 10 "like sudo"'

  PowerShellVersion = '5.1'

  FunctionsToExport = 'Invoke-AsAdministrator'
  FileList = @('PSeudo.psd1','PSeudo.psm1','LICENSE','en-US\about_PSeudo.help.txt','en-US\about_PSeudo_Administrator_Scope.help.txt')

  PrivateData = @{
    PSData = @{
      Tags = @('Invoke-AsAdministrator','Admin','Administrator','Administration','Elevate','Elevated','Privileges','sudo','UAC')
      LicenseUri = 'https://github.com/jfhbrook/PSeudo/blob/master/PSeudo/LICENSE'
      ProjectUri = 'https://github.com/jfhbrook/PSeudo'
    }
  }
}
