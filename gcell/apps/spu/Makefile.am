#
# Copyright 2008 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#


include $(top_srcdir)/Makefile.common.spu

AM_CPPFLAGS = $(GCELL_SPU_INCLUDES)

# SPU executables

noinst_PROGRAMS = \
	benchmark_procs

benchmark_procs_SOURCES = benchmark_procs.c
benchmark_procs_LDADD = $(GCELL_SPU_LA)
benchmark_procs_DEPENDENCIES = $(GCELL_SPU_LA)

