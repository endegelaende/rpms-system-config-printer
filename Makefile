# Makefile for source rpm: system-config-printer
# $Id$
NAME := system-config-printer
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
