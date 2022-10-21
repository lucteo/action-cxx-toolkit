#!/usr/bin/env python3

import os, sys, subprocess

from dataclasses import dataclass, field
from typing import Protocol

# Input variables:
#   INPUT_CHECKS
#   INPUT_DEPENDENCIES
#   INPUT_DIRECTORY
#   INPUT_CONANFILEEDIR
#   INPUT_MAKEFILEDIR
#   INPUT_BUILDDIR
#   INPUT_INSTALLDIR
#   INPUT_CC
#   INPUT_CFLAGS
#   INPUT_CXXFLAGS
#   INPUT_CONANFLAGS
#   INPUT_CMAKEFLAGS
#   INPUT_CTESTFLAGS
#   INPUT_IGNORE_CONAN
#   INPUT_IGNORE_CMAKE
#   INPUT_IGNORE_MAKE
#   INPUT_MAKEFLAGS
#   INPUT_IWYUFLAGS
#   INPUT_CPPCHECKFLAGS
#   INPUT_CLANGTIDYFLAGS
#   INPUT_CLANGFORMATDIRS
#   INPUT_PREBUILD_COMMAND
#   INPUT_BUILD_COMMAND
#   INPUT_POSTBUILD_COMMAND
#   INPUT_TEST_COMMAND

valid_checks = [
    'build',
    'warnings',
    'install',
    'test',
    'clang-format',
    'clang-tidy',
    'cppcheck',
    'iwyu',
    'sanitize',
    'coverage=codecov',
    'coverage=lcov',
]

# The source directory
srcDir = os.getcwd()
# The list of checks that need to be run here (see valid_checks above)
checks = []

class colors:
    ''' The colors to be used by this script; Unix colors '''
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    ORANGE = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    LIGHTGRAY = '\033[0;37m'
    DARKGRAY = '\033[1;30m'
    LIGHTRED = '\033[1;31m'
    LIGHTGREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    LIGHTBLUE = '\033[1;34m'
    LIGHTPURPLE = '\033[1;35m'
    LIGHTCYAN = '\033[1;36m'
    WHITE = '\033[1;37m'
    CLEAR = '\033[0m'

def error(text):
    ''' Prints an errors message and exists the script with error '''
    print(f'\n{colors.LIGHTRED}ERROR: {text}{colors.CLEAR}\n')
    sys.exit(1)

def warning(text):
    ''' Just prints directly a warning message '''
    print(f'{colors.YELLOW}WARNING: {text}{colors.CLEAR}')

def yesno(boolVal):
    return 'yes' if boolVal else 'no'

def param(name, default=None):
    ''' Gets an environment variable param, with fallback to a default value. '''
    res = os.environ.get(name)
    return res if res else default

class Callable(Protocol):
    def __call__(self):
        pass

@dataclass
class HeaderPrint:
    ''' Callable that prints a header when called '''
    text: str
    def __call__(self):
        print(f'\n{colors.LIGHTCYAN}== {self.text}{colors.CLEAR}')

@dataclass
class PropertyPrint:
    ''' Callable that prints the value of a property when called '''
    key: str
    val: str
    def __call__(self):
        print(f'{colors.WHITE}{self.key}:{colors.CLEAR} {self.val}')

@dataclass
class RegularPrint:
    ''' Callable that prints a regular text when called '''
    text: str
    def __call__(self):
        print(self.text)

@dataclass
class Command:
    ''' Callable that executes a bash command; fails if the command fails. '''
    cmd: str
    verbose: bool = True
    def __call__(self):
        if self.cmd:
            if self.verbose:
                print(f'+ {self.cmd}')
            subprocess.run(self.cmd, shell=True, check=True)

@dataclass
class ChDir:
    ''' Callable that changes the current directory '''
    dirName: str
    def __call__(self):
        print(f'+ cd {self.dirName}')
        os.chdir(self.dirName)

@dataclass
class CmdList:
    ''' A structure that keeps a list of multiple callable '''
    cmds: list
    def __call__(self):
        for cmd in self.cmds:
            if cmd:
                cmd()
    def add(self, cmd):
        if cmd:
            self.cmds.append(cmd)

@dataclass
class CompilerInfo:
    ''' Describes the compiler the needs to be used. '''
    # The version of the compiler to be used, short name; e.g., gcc, gcc-9, clang, clang-11, etc
    compilerVer: str
    # The path to the C compiler
    ccPath: str
    # The path to the C++ compiler
    cxxPath: str

    def compiler(self) -> str:
        """ Return the compiler name without version. E.g., gcc, clang"""
        return self.compilerVer.split('-')[0]

    def has_version(self) -> bool:
        return "-" in self.compilerVer
    
    def version(self) -> str:
        """ Return the compiler version, if we have one"""
        return self.compilerVer.split('-')[1]

    def environment_cmd(self) -> str:
        """ Returns the command that needs to be issued to set the compilers in the environment. """
        return f'export CC={self.ccPath} CXX={self.cxxPath}'
    
    def describe(self) -> Callable:
        """ Returns a callable that would describe the compiler being used. """
        return CmdList([
            PropertyPrint('C Compiler to be used', self.ccPath),
            Command(f'{self.ccPath} --version'),
            PropertyPrint('C++ Compiler to be used', self.cxxPath),
            Command(f'{self.cxxPath} --version'),
            PropertyPrint('Environment flags to be used', self.environment_cmd()),
        ])
    
    def update_alternatives(self) -> Callable:
        """ Issue a command to update the alternatives for the compiler.
            We are doing this for the tools to know which compiler to use
        """
        if "-" in self.compilerVer:
            return Command(f'update-alternatives --set {self.compiler()} {self.ccPath}')
        else:
            return CmdList([])


def configure_compiler_options() -> CompilerInfo:
    ''' Detect the compiler version we need to use. '''
    compilerVer = param('INPUT_CC', 'gcc')
    cxxVer = compilerVer.replace("gcc", "g++")
    cxxVer = cxxVer.replace("clang", "clang++")
    cc = f'/usr/bin/{compilerVer}'
    cxx = f'/usr/bin/{cxxVer}'
    return CompilerInfo(compilerVer, cc, cxx)

def configure_conan(compilerInfo) -> Callable:
    ''' Configure the build system with conan '''
    global srcDir

    # Check the flags that we need to add to the conan command, based on the compiler version
    conan_extra_flags = param('INPUT_CONANFLAGS', '')
    conan_extra_flags += f' -s compiler={compilerInfo.compiler()}'
    if compilerInfo.compilerVer == 'clang-7':
        conan_extra_flags += f' -s compiler.version=7.0'
    elif compilerInfo.has_version():
        conan_extra_flags += f' -s compiler.version={compilerInfo.version()}'
    if 'compiler.libcxx' not in conan_extra_flags:
        if compilerInfo.compiler() == 'gcc':
            conan_extra_flags += ' -s compiler.libcxx=libstdc++11'
        elif compilerInfo.compiler() == 'clang':
            conan_extra_flags += ' -s compiler.libcxx=libc++'

    # Generate the command
    conan_command = f'conan profile detect && conan install "{srcDir}" --build=missing -s build_type=Release {conan_extra_flags}'
    PropertyPrint('Conan command', conan_command)()
    return Command(conan_command)

def get_santizier_flags():
    ''' Checks if we need to add some compilation flags to support sanitizer checks '''
    sanitizers_flags = ''
    for c in checks:
        if c.startswith('sanitize='):
            sanitizers_flags += f' -f{c}'
    if sanitizers_flags:
        return f' -fno-omit-frame-pointer {sanitizers_flags}'
    else:
        return ''

def configure_cmake_build(envSetCmd, buildDir):
    ''' Configures the cmake build. Returns a command object to be run to build with cmake '''
    global srcDir
    global checks

    buildCmds = CmdList([])

    cmake_flags = param('INPUT_CMAKEFLAGS', '')
    if cmake_flags:
        PropertyPrint('CMake flags', cmake_flags)()

    # Handle the checks that apply at the build step
    other_cmake_flags = ''
    cmake_cc_flags = ''
    if 'install' in checks:
        installDir = param('INPUT_INSTALLDIR', '/tmp/install')
        PropertyPrint('Install directory', installDir)()
        buildCmds.add(Command(f'mkdir -p {installDir}'))
        other_cmake_flags += f' -DCMAKE_INSTALL_PREFIX={installDir}'
    if 'warnings' in checks:
        cmake_cc_flags += ' -Wall -Werror'
    cmake_cc_flags += get_santizier_flags()

    if 'clang-tidy' in checks or 'cppcheck' in checks or 'iwyu' in checks:
        other_cmake_flags += ' -DCMAKE_EXPORT_COMPILE_COMMANDS=1'

    if 'coverage=codecov' in checks or 'coverage=lcov' in checks:
        cmake_cc_flags += ' --coverage'

    # Add the C and C++ flags
    cflags = param('INPUT_CFLAGS', '') + ' ' + cmake_cc_flags
    if cflags:
        other_cmake_flags += f' -DCMAKE_C_FLAGS="{cflags}"'
    cxxflags = param('INPUT_CXXFLAGS', '') + ' ' + cmake_cc_flags
    if cxxflags:
        other_cmake_flags += f' -DCMAKE_CXX_FLAGS="{cxxflags}"'

    # Generate the actual commands to be run based on the above flags
    cmake_command = f'{envSetCmd} && cmake {cmake_flags} {other_cmake_flags} "{srcDir}"'
    make_params = param('INPUT_MAKEFLAGS', '')
    make_command = f'cmake --build . -v {make_params}'

    PropertyPrint('Configure command', cmake_command)()
    PropertyPrint('Build command', make_command)()
    buildCmds.add(Command(cmake_command))
    if 'build' in checks:
        buildCmds.add(Command(make_command))

    if 'install' in checks:
        install_command = f'cmake --install .'
        PropertyPrint('CMake install command', install_command)()
        buildCmds.add(HeaderPrint('Installing'))
        buildCmds.add(Command(install_command))

    if 'iwyu' in checks:
        PropertyPrint('Running iwyu', yesno(True))()
        flags = param('INPUT_IWYUFLAGS', '')
        buildCmds.add(Command(f'iwyu_tool -p . -- {flags} | tee iwyu_results.txt'))
        buildCmds.add(Command('! grep -e "- #include" iwyu_results.txt'))

    if 'cppcheck' in checks:
        PropertyPrint('Running cppcheck', yesno(True))()
        flags = param('INPUT_CPPCHECKFLAGS', '--enable=style,performance,portability')
        flags += " --template='CPPCHECK_REPORT: {file}:{line},{severity},{id},{message}'"
        buildCmds.add(Command(f'cppcheck --project=compile_commands.json {flags} 2>&1 | tee cppcheck_results.txt'))
        buildCmds.add(Command('! grep -e "CPPCHECK_REPORT:" cppcheck_results.txt'))

    if 'clang-tidy' in checks:
        PropertyPrint('Running clang-tidy', yesno(True))()
        flags = param('INPUT_CLANGTIDYFLAGS', '')
        buildCmds.add(Command(f'if [ -f "{srcDir}/.clang-tidy" ]; then cp --verbose "{srcDir}/.clang-tidy" {buildDir}; fi'))
        buildCmds.add(Command(f'/usr/lib/llvm-13/bin/run-clang-tidy -p . {flags}'))

    # Generate a test command to be used later
    ctest_flags = param('INPUT_CTESTFLAGS', '')
    testCmd = Command(f'ctest --verbose {ctest_flags} {srcDir}')

    return (buildCmds, testCmd)

def configure_make_build():
    ''' Configures the make build. Returns a command object to be run to build with make '''
    global checks

    buildCmds = CmdList([])

    # Depending on checks, check if we can add C or C++ flags
    make_cc_flags = ''
    if 'warnings' in checks:
        make_cc_flags += ' -Wall -Werror'
    make_cc_flags += get_santizier_flags()

    # Add the C and C++ flags
    make_params = param('INPUT_MAKEFLAGS', '')
    cflags = param('INPUT_CFLAGS', '') + ' ' + make_cc_flags
    if cflags:
        make_params += f' CFLAGS="{cflags}"'
    cxxflags = param('INPUT_CXXFLAGS', '') + ' ' + make_cc_flags
    if cxxflags:
        make_params += f' CXXFLAGS="{cxxflags}"'


    make_command = f'make {make_params}'
    PropertyPrint('Build command', make_command)()
    buildCmds.add(Command(make_command))

    if 'install' in checks:
        install_command = f'make install'
        PropertyPrint('Install command', install_command)()
        buildCmds.add(HeaderPrint('Installing'))
        buildCmds.add(Command(install_command))

    # Generate a test command to be used later
    testCmd = Command(f'make test')

    return (buildCmds, testCmd)

def auto_build_phase():
    ''' Configures and runs the build phase (automatic mode). '''
    global checks

    if 'build' not in checks and 'clang-tidy' not in checks and 'cppcheck' not in checks and 'iwyu' not in checks:
        return (None, None)

    HeaderPrint('Auto-determining build commands')()
    conanfileDir = param('INPUT_CONANFILEEDIR', srcDir)
    makefileDir = param('INPUT_MAKEFILEDIR', srcDir) 
    hasConan = (param('INPUT_IGNORE_CONAN', 'false') == 'false') and os.path.isfile(f'{conanfileDir}/conanfile.txt') or os.path.isfile(f'{conanfileDir}/conanfile.py')
    hasCmake = (param('INPUT_IGNORE_CMAKE', 'false') == 'false') and os.path.isfile(f'{makefileDir}/CMakeLists.txt')
    hasMake = (param('INPUT_IGNORE_MAKE', 'false') == 'false') and os.path.isfile(f'{makefileDir}/Makefile')
    PropertyPrint('Has Conan', yesno(hasConan))()
    PropertyPrint('Has Cmake', yesno(hasCmake))()
    PropertyPrint('Has Make', yesno(hasMake))()

    # Print version for conan, cmake & make
    if hasConan:
        Command(f'conan --version')()
    if hasCmake:
        Command(f'cmake --version')()
    if hasMake:
        Command(f'make --version')()

    if not hasCmake and not hasMake:
        error('Cannot autodetect build system. Provide the build command manually')

    # Determine the compiler
    compilerInfo = configure_compiler_options()
    compilerInfo.describe()()

    buildCmds = CmdList([])
    buildCmds.add(HeaderPrint('Building the software'))
    buildCmds.add(compilerInfo.update_alternatives())

    # If we have conan, add a conan command first
    if hasConan:
        buildCmds.add(configure_conan(compilerInfo))

    # Setup build and install directories
    defaultBuildDir = '/tmp/build' if hasCmake else ''
    buildDir = param('INPUT_BUILDDIR', defaultBuildDir)
    if buildDir:
        PropertyPrint('Build directory', buildDir)()
        buildCmds.add(Command(f'mkdir -p {buildDir}'))
        buildCmds.add(ChDir(buildDir))

    (buildCmd, testCmd) = (None, None)
    if hasCmake:
        (buildCmd, testCmd) = configure_cmake_build(compilerInfo.environment_cmd(), buildDir)
        buildCmds.add(buildCmd)
    elif hasMake:
        (buildCmd, testCmd) = configure_make_build()
        buildCmds.add(buildCmd)

    return (buildCmds, testCmd)

def auto_test_phase(autoTestCmd):
    ''' Configures and runs the test phase (automatic mode). '''
    global srcDir
    global checks

    toRun = CmdList([])
    if 'test' in checks:
        toRun.add(HeaderPrint('Running tests'))
        toRun.add(autoTestCmd)

        # Post-test actions?
        if 'coverage=codecov' in checks or 'coverage=lcov' in checks:
            toRun.add(HeaderPrint('Gathering test coverage info'))

            if 'coverage=codecov' in checks:
                toRun.add(Command(f'bash -c "bash <(curl -s https://codecov.io/bash) -R {srcDir}"'))
            if 'coverage=lcov' in checks:
                toRun.add(Command('lcov -c -d . -o lcov.info'))
                toRun.add(Command(f'cp lcov.info {srcDir}/'))

    if 'clang-format' in checks:
        dirs = param('INPUT_CLANGFORMATDIRS', '.').split()
        dirs = map(lambda d: f'"{srcDir}/{d}"', dirs)
        dirsStr = ' '.join(dirs)
        toRun.add(Command(f'find {dirsStr} \\( -name "*.[ch]" -o -name "*.cc" -o -name "*.cpp" -o -name "*.hpp" \\) -exec clang-format --Werror --dry-run {{}} +'))

    return toRun

def configure_dependencies():
    deps = param('INPUT_DEPENDENCIES')
    if deps:
        return CmdList([
            PropertyPrint('Packages to install', deps),
            Command(f'apt-get -y update ; apt-get install --no-install-recommends -y {deps}'),
            RegularPrint(''),
        ])
    return None

def configure_changedir():
    global srcDir
    targetdir = param('INPUT_DIRECTORY')
    if targetdir:
        srcDir = targetdir
        return CmdList([
            PropertyPrint('Target directory', targetdir),
            ChDir(targetdir),
        ])
    return None

def check_custom_phase(paramName, printText):
    customCmd = param(paramName)
    if customCmd:
        return CmdList([
            HeaderPrint(printText),
            Command(customCmd),
        ])
    else:
        return None

def check_override_phase(paramName, printText, defaultCmd = None):
    customCmd = param(paramName)
    if customCmd:
        return CmdList([
            HeaderPrint(printText),
            Command(customCmd),
        ])
    return defaultCmd

def get_checks():
    ''' Parses and verifies the list of checks we need to apply. '''
    checks = param('INPUT_CHECKS', '').split()
    PropertyPrint('Given checks', checks)()
    for c in checks:
        if c not in valid_checks and not c.startswith('sanitize='):
            warning(f"Check '{c}' is not valid; ignored")
    if not checks:
        checks += ['build', 'test']
        PropertyPrint('Implicitly adding default checks', checks)()
    # Do we need to add extra checks?
    extra_checks = []
    if 'build' not in checks:
        needs_build = ['install', 'test', 'warnings', 'coverage=codecov', 'coverage=lcov']
        for c in checks:
            if c in needs_build or c.startswith('sanitize='):
                extra_checks.append('build')
                break
    if 'test' not in checks:
        needs_test = ['coverage=codecov', 'coverage=lcov']
        for c in checks:
            if c in needs_test or c.startswith('sanitize='):
                extra_checks.append('test')
                break
    if 'coverage=codecov' in checks:
        if not param('GITHUB_SHA'):
            warning('Could not find GITHUB_SHA environment variable. Is the environment set correctly? (expected env vars: GITHUB_ACTION, GITHUB_REF, GITHUB_REPOSITORY, GITHUB_HEAD_REF, GITHUB_SHA, GITHUB_RUN_ID)')
    if extra_checks:
        PropertyPrint('Adding implicit checks', extra_checks)()
        checks += extra_checks

    return checks

def read_file_content(filename):
    return open(filename, 'r').read()


def main():
    HeaderPrint('action-cxx-toolkit')()
    PropertyPrint('Version', read_file_content("/usr/local/etc/action-cxx-toolkit/version"))()
    PropertyPrint('Build date', read_file_content("/usr/local/etc/action-cxx-toolkit/version_date"))()

    # Configure and build the phases with what we need to run
    HeaderPrint('Configuring')()
    global checks
    checks = get_checks()

    try:
        phases = CmdList([])
        phases.add(configure_dependencies())
        phases.add(configure_changedir())

        # Pre-build phase
        phases.add(check_custom_phase('INPUT_PREBUILD_COMMAND', 'Running custom pre-build command'))

        # Build phase
        autoTestCmd = None
        buildCmd = check_custom_phase('INPUT_BUILD_COMMAND', 'Running custom build command')
        if not buildCmd:
            (buildCmd, autoTestCmd) = auto_build_phase()
        phases.add(buildCmd)

        # Post-build phase
        phases.add(check_custom_phase('INPUT_POSTBUILD_COMMAND', 'Running custom post-build command'))

        # Test phase
        testCmd = check_custom_phase('INPUT_TEST_COMMAND', 'Running custom test command')
        if not testCmd:
            testCmd = auto_test_phase(autoTestCmd)
        phases.add(testCmd)

        # Actually run everything
        phases()
    except subprocess.CalledProcessError as e:
        print(e)    # Don't print the whole stack
        sys.exit(1)

if __name__ == '__main__':
    main()