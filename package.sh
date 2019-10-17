#!/bin/bash

eval "rm -rf dist/*"

zipCmd="git archive HEAD -o dist/salesGenerator_sourceCode.zip"
eval $zipCmd

eval "pyinstaller sales_generator.spec "
eval "cp -r sql ./dist"
eval "mv dist sales_generator"

eval "zip -r salesGenerator.zip sales_generator"
eval "mv salesGenerator.zip sales_generator/"
eval "mv sales_generator dist"
