#
# Copyright (c) 2016 Stefan Seefeld
# All rights reserved.
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

from SCons.Script import AddOption
import sys

variables=[] # remember 'public' variables
options=[]

def add_option(*args, **kwds):
    """Capture the help messages so we can produce a helpful usage text."""
    options.append('{:25} {}'.format(', '.join(args), kwds.get('help', '')))
    AddOption(*args, **kwds)

def add_variable(vars, var):
    variables.append(var[0])
    vars.Add(var)


def options_help(env):

    return '\n  '.join(options)

    
def variables_help(vars, env):
    """This is cloned from SCons' Variables.GenerateHelpText, to only report 'public' variables."""

    opts = [o for o in vars.options if o.key in variables]

    def format(opt):
        actual = env.subst('${%s}' % opt.key) if opt.key in env else None
        return vars.FormatVariableHelpText(env, opt.key, opt.help, opt.default, actual, opt.aliases)

    text = ''.join([f for f in map(format, opts) if f])
    lines = [f'  {l}' for l in text.split('\n')]
    return '\n'.join(lines)


    
def help(vars, env):

    return """Usage: scons [--option...] [variable=value...] [target...]

available options:

  {}

available variables:
  {}
""".format(options_help(env), variables_help(vars, env))

def pretty_output(env):

    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'blue': '\033[34m',
        'yellow': '\033[93m',
        'Red': '\033[91m',
        'Green': '\033[92m',
        'Blue': '\033[94m',
        'Purple': '\033[95m',
        'Cyan': '\033[96m',
        'end': '\033[0m',
    }
    #If the output is not a terminal, remove the colors
    if not sys.stdout.isatty():
        for key, value in colors.iteritems():
            colors[key] = ''

    compile_source_message = '{green}Compiling $TARGET{end}'.format(**colors)
    compile_shared_source_message = '{green}Compiling $TARGET{end}'.format(**colors)
    link_program_message = '{blue}Linking $TARGET{end}'.format(**colors)
    link_library_message = '{blue}Linking $TARGET{end}'.format(**colors)
    ranlib_library_message = '{blue}Ranlib $TARGET{end}'.format(**colors)
    link_shared_library_message = '{blue}Linking $TARGET{end}'.format(**colors)
    test_message = '{blue}Testing $SOURCE{end}'.format(**colors)
    testsum_message = '{Blue}Test Summary{end}'.format(**colors)

    env.Replace(CXXCOMSTR = compile_source_message,
                CCCOMSTR = compile_source_message,
                SHCCCOMSTR = compile_shared_source_message,
                SHCXXCOMSTR = compile_shared_source_message,
                ARCOMSTR = link_library_message,
                RANLIBCOMSTR = ranlib_library_message,
                SHLINKCOMSTR = link_shared_library_message,
                LINKCOMSTR = link_program_message,
                TESTCOMSTR = test_message,
                TESTSUMCOMSTR = testsum_message)
