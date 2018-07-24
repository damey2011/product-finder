@echo off
set list=
set newList=%list:'=%
set newList=%newList:,=%
set newList=%newList:[=%
set newList=%newList:]=%
(for %%a in (%newList%) do (
  chrome %%a
))
