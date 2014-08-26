#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013  Google Inc.
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

from nose.tools import eq_, ok_
from ycmd import identifier_utils as iu


def RemoveIdentifierFreeText_CppComments_test():
  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          "foo \nbar //foo \nqux" ) )


def RemoveIdentifierFreeText_PythonComments_test():
  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          "foo \nbar #foo \nqux" ) )


def RemoveIdentifierFreeText_CstyleComments_test():
  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          "foo \nbar /* foo */\nqux" ) )

  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          "foo \nbar /* foo \n foo2 */\nqux" ) )


def RemoveIdentifierFreeText_SimpleSingleQuoteString_test():
  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          "foo \nbar 'foo'\nqux" ) )


def RemoveIdentifierFreeText_SimpleDoubleQuoteString_test():
  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          'foo \nbar "foo"\nqux' ) )


def RemoveIdentifierFreeText_EscapedQuotes_test():
  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          "foo \nbar 'fo\\'oz\\nfoo'\nqux" ) )

  eq_( "foo \nbar \nqux",
       iu.RemoveIdentifierFreeText(
          'foo \nbar "fo\\"oz\\nfoo"\nqux' ) )


def RemoveIdentifierFreeText_SlashesInStrings_test():
  eq_( "foo \nbar baz\nqux ",
       iu.RemoveIdentifierFreeText(
           'foo \nbar "fo\\\\"baz\nqux "qwe"' ) )

  eq_( "foo \nbar \nqux ",
       iu.RemoveIdentifierFreeText(
           "foo '\\\\'\nbar '\\\\'\nqux '\\\\'" ) )


def RemoveIdentifierFreeText_EscapedQuotesStartStrings_test():
  eq_( "\\\"foo\\\" zoo",
       iu.RemoveIdentifierFreeText(
           "\\\"foo\\\"'\"''bar' zoo'test'" ) )

  eq_( "\\'foo\\' zoo",
       iu.RemoveIdentifierFreeText(
           "\\'foo\\'\"'\"\"bar\" zoo\"test\"" ) )


def RemoveIdentifierFreeText_NoMultilineString_test():
  eq_( "'\nlet x = \nlet y = ",
       iu.RemoveIdentifierFreeText(
           "'\nlet x = 'foo'\nlet y = 'bar'" ) )

  eq_( "\"\nlet x = \nlet y = ",
       iu.RemoveIdentifierFreeText(
           "\"\nlet x = \"foo\"\nlet y = \"bar\"" ) )


def RemoveIdentifierFreeText_PythonMultilineString_test():
  eq_( "\nzoo",
       iu.RemoveIdentifierFreeText(
           "\"\"\"\nfoobar\n\"\"\"\nzoo" ) )

  eq_( "\nzoo",
       iu.RemoveIdentifierFreeText(
           "'''\nfoobar\n'''\nzoo" ) )


def ExtractIdentifiersFromText_test():
  eq_( [ "foo", "_bar", "BazGoo", "FOO", "_", "x", "one", "two", "moo", "qqq" ],
       iu.ExtractIdentifiersFromText(
           "foo $_bar \n&BazGoo\n FOO= !!! '-' - _ (x) one-two !moo [qqq]" ) )


def ExtractIdentifiersFromText_Css_test():
  eq_( [ "foo", "-zoo", "font-size", "px", "a99" ],
       iu.ExtractIdentifiersFromText(
           "foo -zoo {font-size: 12px;} a99", "css" ) )


def ExtractIdentifiersFromText_Html_test():
  eq_( [ "foo", "goo-foo", "zoo", "bar", "aa", "z", "b@g" ],
       iu.ExtractIdentifiersFromText(
           '<foo> <goo-foo zoo=bar aa="" z=\'\'/> b@g', "html" ) )


def IsIdentifier_generic_test():
  ok_( iu.IsIdentifier( 'foo' ) )
  ok_( iu.IsIdentifier( 'foo129' ) )
  ok_( iu.IsIdentifier( 'f12' ) )

  ok_( not iu.IsIdentifier( '1foo129' ) )
  ok_( not iu.IsIdentifier( '-foo' ) )
  ok_( not iu.IsIdentifier( 'foo-' ) )
  ok_( not iu.IsIdentifier( 'font-face' ) )
  ok_( not iu.IsIdentifier( None ) )
  ok_( not iu.IsIdentifier( '' ) )


def IsIdentifier_Css_test():
  ok_( iu.IsIdentifier( 'font-face', 'css' ) )


def StartOfLongestIdentifierEndingAtIndex_Simple_test():
  eq_( 0, iu.StartOfLongestIdentifierEndingAtIndex( 'foo', 3 ) )
  eq_( 0, iu.StartOfLongestIdentifierEndingAtIndex( 'f12', 3 ) )


def StartOfLongestIdentifierEndingAtIndex_BadInput_test():
  eq_( 0, iu.StartOfLongestIdentifierEndingAtIndex( '', 0 ) )
  eq_( 1, iu.StartOfLongestIdentifierEndingAtIndex( '', 1 ) )
  eq_( 5, iu.StartOfLongestIdentifierEndingAtIndex( None, 5 ) )
  eq_( -1, iu.StartOfLongestIdentifierEndingAtIndex( 'foo', -1 ) )
  eq_( 10, iu.StartOfLongestIdentifierEndingAtIndex( 'foo', 10 ) )


def StartOfLongestIdentifierEndingAtIndex_Punctuation_test():
  eq_( 1, iu.StartOfLongestIdentifierEndingAtIndex( '(foo', 4 ) )
  eq_( 6, iu.StartOfLongestIdentifierEndingAtIndex( '      foo', 9 ) )
  eq_( 4, iu.StartOfLongestIdentifierEndingAtIndex( 'gar;foo', 7 ) )
  eq_( 2, iu.StartOfLongestIdentifierEndingAtIndex( '...', 2 ) )


def StartOfLongestIdentifierEndingAtIndex_PunctuationWithUnicode_test():
  eq_( 1, iu.StartOfLongestIdentifierEndingAtIndex( u'(fäö', 4 ) )
  eq_( 2, iu.StartOfLongestIdentifierEndingAtIndex( u'  fäö', 5 ) )


# Not a test, but a test helper function
def LoopExpect( ident, expected, end_index ):
  eq_( expected, iu.StartOfLongestIdentifierEndingAtIndex( ident, end_index ) )


def StartOfLongestIdentifierEndingAtIndex_Entire_Simple_test():
  ident = 'foobar'
  for i in range( len( ident ) ):
    yield LoopExpect, ident, 0, i


def StartOfLongestIdentifierEndingAtIndex_Entire_AllBad_test():
  ident = '....'
  for i in range( len( ident ) ):
    yield LoopExpect, ident, i, i


def StartOfLongestIdentifierEndingAtIndex_Entire_FirstCharNotNumber_test():
  ident = 'f12341234'
  for i in range( len( ident ) ):
    yield LoopExpect, ident, 0, i


def StartOfLongestIdentifierEndingAtIndex_Entire_SubIdentifierValid_test():
  ident = 'f123f1234'
  for i in range( len( ident ) ):
    yield LoopExpect, ident, 0, i


def StartOfLongestIdentifierEndingAtIndex_Entire_Unicode_test():
  ident = u'fäöttccoö'
  for i in range( len( ident ) ):
    yield LoopExpect, ident, 0, i