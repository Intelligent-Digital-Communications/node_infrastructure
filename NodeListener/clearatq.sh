#!/bin/bash
atq | awk '{print $1}'
for i in `atq | awk '{print $1}'`; do atrm $i; done
